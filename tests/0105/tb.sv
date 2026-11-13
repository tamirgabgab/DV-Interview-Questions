//@flags --timing
// Question 0105: the page's SystemVerilog. distinct_exact, mix64, rank and one_register on the
// page's streams (the ranks of the growing streams, a stream with repeats); the hll class
// against the estimates the Python tests compute (the growing streams, the small range, the
// repeats, the union of two monitors); and the hll_update module: the page's per-clock table
// (16 registers, with and without forwarding), directed pairs of addresses in one register at
// every distance from 1 to 4 (bubbles or other registers between them) and chains of three,
// random streams with a hot set of addresses and bubbles into 16 and 1,024 registers, every
// register read back and compared bit for bit with the hll class, and 100,000 addresses whose
// registers, read out by the "software", give the page's estimate. FORWARD = 0 must fail at
// distance 1 and only there; coverage counters for the distances of the hazard.
//@page function automatic int distinct_exact
//@page function automatic logic [63:0] mix64
//@page class hll
//@page module hll_update

// the t-th address of the page's stream of distinct addresses: 64 * (t * 2654435761 mod 2^26)
function automatic logic [63:0] distinct_addr(longint t);
  return 64'd64 * ((64'(t) * 64'd2654435761) % 64'd67108864);
endfunction

function automatic bit near(real a, real b);
  real d = a - b;
  if (d < 0) d = -d;
  return d <= 1e-9 * (b < 0 ? -b : b) + 1e-12;
endfunction

module tb;
  logic clk = 0;
  always #5 clk = ~clk;
  int errors = 0;

  task automatic fail(string what);
    errors++;
    if (errors < 30) $display("%s", what);
  endtask

  // three update units on the same inputs: 16 registers, 16 without forwarding, 1,024
  logic        rst_n = 0, in_valid = 0;
  logic [63:0] in_addr = 0;
  logic [3:0]  rd4 = 0;
  logic [9:0]  rd10 = 0;
  logic [5:0]  val4, valb, val10;
  logic        busy4, busyb, busy10;
  hll_update #(.P(4)) u4 (.clk, .rst_n, .in_valid, .in_addr, .rd_idx(rd4), .rd_val(val4), .busy(busy4));
  hll_update #(.P(4), .FORWARD(0)) ub (.clk, .rst_n, .in_valid, .in_addr, .rd_idx(rd4), .rd_val(valb), .busy(busyb));
  hll_update #(.P(10)) u10 (.clk, .rst_n, .in_valid, .in_addr, .rd_idx(rd10), .rd_val(val10), .busy(busy10));

  // coverage of the hazard in the 16-register unit: the same register in stage 3 at distance
  // 1 (and the forwarded value changed the write), 2 and 3
  int cov_d1 = 0, cov_d1_fwd = 0, cov_d2 = 0, cov_d3 = 0;
  logic       hv[3];
  logic [3:0] hj[3];
  initial foreach (hv[i]) hv[i] = 0;
  always @(negedge clk) if (rst_n) begin
    if (u4.v2) begin
      if (hv[0] && hj[0] == u4.j2) begin
        cov_d1++;
        if ((u4.r2 > u4.q2 ? u4.r2 : u4.q2) != u4.nv) cov_d1_fwd++;
      end else if (hv[1] && hj[1] == u4.j2) cov_d2++;
      else if (hv[2] && hj[2] == u4.j2) cov_d3++;
    end
    hv[2] = hv[1]; hj[2] = hj[1];
    hv[1] = hv[0]; hj[1] = hj[0];
    hv[0] = u4.v2; hj[0] = u4.j2;
  end

  task automatic restart();                 // a reset: the units clear their registers
    in_valid = 0;
    rst_n = 0;
    @(negedge clk);
    rst_n = 1;
    @(negedge clk);
    if (!busy4 || !busy10) fail("busy is low right after reset");
    while (busy4 || busyb || busy10) @(negedge clk);
  endtask

  task automatic send(logic [63:0] a, bit v);
    in_valid = v;
    in_addr = v ? a : 64'($urandom());      // the address of a bubble is anything at all
    @(negedge clk);
  endtask

  task automatic flush();
    in_valid = 0;
    repeat (4) @(negedge clk);
  endtask

  // the registers of the 16-register units against the reference; bad: how many differ without forwarding
  task automatic read16(hll ref4, string what, output int bad);
    bad = 0;
    for (int j = 0; j < 16; j++) begin
      rd4 = 4'(j);
      #1;
      if (val4 != 6'(ref4.regs[j])) fail($sformatf("%s: register %0d is %0d, want %0d", what, j, val4, ref4.regs[j]));
      if (valb != 6'(ref4.regs[j])) bad++;
    end
  endtask

  task automatic read1024(hll ref10, string what);
    for (int j = 0; j < 1024; j++) begin
      rd10 = 10'(j);
      #1;
      if (val10 != 6'(ref10.regs[j])) fail($sformatf("%s: register %0d of 1,024 is %0d, want %0d", what, j, val10, ref10.regs[j]));
    end
  endtask

  // the page's per-clock table: v1 v2 wv R[12] R[12] without forwarding, after every clock
  string want_trace[6] = '{"1 0 0 0 0", "1 1 0 0 0", "0 1 1 4 4", "1 0 1 4 1", "0 1 0 4 1", "0 0 1 4 2"};
  longint pipe_in[4] = '{1984, 1280, -1, 1472};

  initial begin
    logic [63:0] s[$], t2[$], pool[$], others[$];
    int grow[6] = '{10, 100, 1000, 10000, 100000, 1000000};
    int grow_r[6] = '{5, 7, 10, 13, 20, 20};
    real grow_e[6] = '{10.049148363084463, 98.59811271900311, 1025.9278461025879, 10353.072409734536, 106785.73516707939, 992010.5557394959};
    hll h, h2, ref4, ref10;
    int n, bad, j, runs_bad;
    string got;
    logic [63:0] a;

    // part b: the hash and the rank
    if (mix64(0) != 64'he220a8397b1dcdaf || mix64(1) != 64'h910a2dec89025cc1 || mix64('1) != 64'he4d971771b652c20)
      fail("mix64 of 0, 1 and all ones");
    if (mix64(877363008) != 64'h11f95a03534da7c1 || distinct_addr(13) != 877363008) fail("the example address");
    if (rank(64'h11f95a03534da7c1, 64) != 4 || rank(64'h11f95a03534da7c1, 60) != 4) fail("the ranks of the example");
    if (rank(0, 64) != 65 || rank(1, 64) != 64 || rank(64'h8000_0000_0000_0000, 64) != 1 || rank(64'hF000_0000_0000_0001, 60) != 60)
      fail("rank at its edges");

    // part a and part b on the growing streams; part c's estimates on them
    h = new(10);
    n = 0;
    foreach (grow[g]) begin
      while (n < grow[g]) begin
        n++;
        s.push_back(distinct_addr(n));
        h.add(distinct_addr(n));
      end
      if (one_register(s) != grow_r[g]) fail($sformatf("one_register of %0d addresses: %0d", grow[g], one_register(s)));
      if (!near(h.estimate(), grow_e[g])) fail($sformatf("hll estimate of %0d addresses: %f", grow[g], h.estimate()));
      if (grow[g] <= 10000 && distinct_exact(s) != grow[g]) fail("distinct_exact of distinct addresses");
    end

    // repeats: 15,000 transactions over 5,000 addresses count as the 5,000 alone
    h = new(10); h2 = new(10);
    s.delete();
    for (longint t = 1; t <= 15000; t++) begin
      a = distinct_addr(1 + (t * 64'd2654435761) % 67108864 % 5000);
      s.push_back(a);
      h.add(a);
    end
    for (int t = 1; t <= 5000; t++) h2.add(distinct_addr(t));
    if (distinct_exact(s) != 5000) fail($sformatf("distinct_exact with repeats: %0d", distinct_exact(s)));
    if (h.regs != h2.regs || !near(h.estimate(), 5115.386732632992)) fail($sformatf("repeats: %f", h.estimate()));

    // the small range: 100 addresses in 1,024 registers, 930 of them empty
    h = new(10);
    for (int t = 1; t <= 100; t++) h.add(distinct_addr(t));
    n = 0;
    foreach (h.regs[i]) if (h.regs[i] == 0) n++;
    if (n != 930 || !near(h.estimate(), 98.59811271900311)) fail($sformatf("small range: %0d empty, %f", n, h.estimate()));

    // two monitors and their union
    h = new(10); h2 = new(10); ref10 = new(10);
    for (int t = 1; t <= 60000; t++) begin h.add(distinct_addr(t)); ref10.add(distinct_addr(t)); end
    for (int t = 30001; t <= 90000; t++) begin h2.add(distinct_addr(t)); ref10.add(distinct_addr(t)); end
    if (!near(h.estimate(), 62701.794499131574) || !near(h2.estimate(), 63233.825570112895)) fail("the two monitors");
    h.merge(h2);
    if (h.regs != ref10.regs || !near(h.estimate(), 96381.93670982184)) fail($sformatf("the union: %f", h.estimate()));

    // part d: the page's per-clock table
    restart();
    foreach (pipe_in[c]) begin
      send(64'(pipe_in[c]), pipe_in[c] >= 0);
      rd4 = 4'd12;
      #1;
      got = $sformatf("%0d %0d %0d %0d %0d", u4.v1, u4.v2, u4.wv, val4, valb);
      if (got != want_trace[c]) fail($sformatf("clock %0d: %s, want %s", c + 1, got, want_trace[c]));
    end
    for (int c = 4; c < 6; c++) begin
      send(0, 0);
      rd4 = 4'd12;
      #1;
      got = $sformatf("%0d %0d %0d %0d %0d", u4.v1, u4.v2, u4.wv, val4, valb);
      if (got != want_trace[c]) fail($sformatf("clock %0d: %s, want %s", c + 1, got, want_trace[c]));
    end

    // addresses of register 12 and of other registers, for the directed streams
    for (int x = 1; pool.size() < 12 || others.size() < 12; x++) begin
      a = 64'(64 * x);
      j = int'(mix64(a) >> 60);
      if (j == 12 && pool.size() < 12) pool.push_back(a);
      else if (j != 12 && others.size() < 12) others.push_back(a);
    end

    // a high rank, then a low rank in the same register, d clocks apart
    for (int d = 1; d <= 4; d++)
      for (int filler = 0; filler < 2; filler++) begin
        restart();
        ref4 = new(4);
        send(1984, 1); ref4.add(1984);                         // rank 4
        for (int i = 1; i < d; i++)
          if (filler) begin send(others[i], 1); ref4.add(others[i]); end
          else send(0, 0);
        send(1280, 1); ref4.add(1280);                         // rank 1
        flush();
        read16(ref4, $sformatf("distance %0d", d), bad);
        if ((bad != 0) != (d == 1))
          fail($sformatf("without forwarding, distance %0d, %s: %0d registers differ", d, filler ? "other registers" : "bubbles", bad));
      end

    // chains of three to one register, back to back, in every order of the ranks 4, 1, 2
    for (int perm = 0; perm < 6; perm++) begin
      longint order[6][3] = '{'{1984, 1280, 1472}, '{1984, 1472, 1280}, '{1280, 1984, 1472},
                              '{1280, 1472, 1984}, '{1472, 1984, 1280}, '{1472, 1280, 1984}};
      restart();
      ref4 = new(4);
      foreach (order[perm][i]) begin send(64'(order[perm][i]), 1); ref4.add(64'(order[perm][i])); end
      flush();
      read16(ref4, $sformatf("chain %0d", perm), bad);
    end

    // random streams with a hot set and bubbles, into 16 and 1,024 registers at once
    runs_bad = 0;
    for (int run = 0; run < 30; run++) begin
      restart();
      ref4 = new(4); ref10 = new(10);
      t2.delete();
      for (int i = 0; i < 8; i++) t2.push_back($urandom_range(1) ? pool[$urandom_range(11)] : {$urandom(), $urandom()});
      repeat (2000) begin
        if ($urandom_range(4) == 0) send(0, 0);
        else begin
          a = $urandom_range(1) ? t2[$urandom_range(7)] : {$urandom(), $urandom()};
          send(a, 1);
          ref4.add(a); ref10.add(a);
        end
      end
      flush();
      read16(ref4, $sformatf("random run %0d", run), bad);
      if (bad) runs_bad++;
      read1024(ref10, $sformatf("random run %0d", run));
    end
    if (runs_bad == 0) fail("without forwarding, no random run differs");

    // 100,000 addresses one a clock into 1,024 registers: the software reads them out and
    // computes the page's estimate
    restart();
    ref10 = new(10);
    for (int t = 1; t <= 100000; t++) begin send(distinct_addr(t), 1); ref10.add(distinct_addr(t)); end
    flush();
    read1024(ref10, "100,000 addresses");
    h = new(10);
    for (int i = 0; i < 1024; i++) begin rd10 = 10'(i); #1; h.regs[i] = byte'(val10); end
    if (!near(h.estimate(), 106785.73516707939)) fail($sformatf("the estimate from the unit's registers: %f", h.estimate()));

    if (cov_d1 == 0 || cov_d1_fwd == 0 || cov_d2 == 0 || cov_d3 == 0)
      fail($sformatf("coverage: distance 1 %0d (forward changed the write %0d), 2 %0d, 3 %0d", cov_d1, cov_d1_fwd, cov_d2, cov_d3));
    $display("hazards: distance 1 %0d (forward changed the write %0d), 2 %0d, 3 %0d; random runs that fail without forwarding: %0d of 30",
             cov_d1, cov_d1_fwd, cov_d2, cov_d3, runs_bad);
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
