//@flags --assert --timing
// Question 0054: the page's rr_arbiter and wrr_arbiter against plain-loop references, and
// the page's arb_checker on four lanes of random traffic that keeps a waiting request: the
// correct arbiter (no assertion fails) and three buggy copies (the pointer stuck, moved onto
// the winner, two grants), each failing its own rule; the checker's counters must equal a
// procedural count of the same rules on the same samples. The weighted arbiter is checked
// for its shares and its bound under full load.
//@page module rr_arbiter
//@page module arb_checker
//@page module wrr_arbiter

// the round robin with one of three bugs: 1 the pointer never moves, 2 it moves onto the
// winner, 3 the lowest requester is granted too
module rr_bug #(parameter int N = 4, parameter int BUG = 1) (
  input logic clk, rst_n, input logic [N-1:0] req, output logic [N-1:0] gnt
);
  logic [N-1:0] pri;
  logic [2*N-1:0] dbl, sel;
  always_comb begin
    dbl = {req, req};
    sel = dbl & ~(dbl - {{N{1'b0}}, pri});
    gnt = sel[N-1:0] | sel[2*N-1:N];
    if (BUG == 3) gnt = gnt | (req & (~req + 1'b1));
  end
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) pri <= N'(1);
    else if (|gnt && BUG != 1) pri <= (BUG == 2) ? gnt : {gnt[N-2:0], gnt[N-1]};
endmodule

module tb;
  localparam int N = 4, T = 600;
  //@page function automatic logic [N-1:0] fixed_priority

  logic clk = 0, rst_n = 0;
  logic [N-1:0] req[4], gnt[4];
  int errors = 0;
  always #5 clk = ~clk;

  rr_arbiter #(.N(N)) dut0 (.clk, .rst_n, .req(req[0]), .gnt(gnt[0]));
  rr_bug #(.N(N), .BUG(1)) dut1 (.clk, .rst_n, .req(req[1]), .gnt(gnt[1]));
  rr_bug #(.N(N), .BUG(2)) dut2 (.clk, .rst_n, .req(req[2]), .gnt(gnt[2]));
  rr_bug #(.N(N), .BUG(3)) dut3 (.clk, .rst_n, .req(req[3]), .gnt(gnt[3]));
  arb_checker #(.N(N)) chk0 (.clk, .rst_n, .req(req[0]), .gnt(gnt[0]));
  arb_checker #(.N(N)) chk1 (.clk, .rst_n, .req(req[1]), .gnt(gnt[1]));
  arb_checker #(.N(N)) chk2 (.clk, .rst_n, .req(req[2]), .gnt(gnt[2]));
  arb_checker #(.N(N)) chk3 (.clk, .rst_n, .req(req[3]), .gnt(gnt[3]));

  logic [N-1:0] wreq;
  logic [N-1:0] wgnt;
  logic [3:0] weight [N] = '{4'd1, 4'd2, 4'd3, 4'd4};
  wrr_arbiter #(.N(N), .WB(4)) wdut (.clk, .rst_n, .req(wreq), .gnt(wgnt), .weight(weight));

  // the samples of every cycle: taken a moment after the inputs change on the falling edge,
  // so they are what the assertions sample at the next rising edge (at the rising edge
  // itself the pointer may already have moved)
  logic [N-1:0] hr[4][$], hg[4][$], wh[$];

  // the rules counted on the samples, as the assertions count them
  function automatic void count(int l, output int oh, sp, ho, fa);
    int n = hr[l].size();
    bit got;
    oh = 0; sp = 0; ho = 0; fa = 0;
    for (int t = 0; t < n; t++) begin
      if (!$onehot0(hg[l][t])) oh++;
      if ((hg[l][t] & ~hr[l][t]) != 0) sp++;
      for (int i = 0; i < N; i++) begin
        if (t + 1 < n && hr[l][t][i] && !hg[l][t][i] && !hr[l][t + 1][i]) ho++;
        if (hr[l][t][i] && t + N - 1 < n) begin
          got = 0;
          for (int u = t; u <= t + N - 1; u++) if (hg[l][u][i]) got = 1;
          if (!got) fa++;
        end
      end
    end
  endfunction

  // the round robin as a loop from the pointer, on lane 0's samples
  function automatic void reference_rr();
    int ptr = 0, win;
    for (int t = 0; t < hr[0].size(); t++) begin
      logic [N-1:0] want = '0;
      win = -1;
      for (int k = 0; k < N; k++) if (win < 0 && hr[0][t][(ptr + k) % N]) win = (ptr + k) % N;
      if (win >= 0) begin want[win] = 1'b1; ptr = (win + 1) % N; end
      if (hg[0][t] !== want) begin errors++; $display("rr cycle %0d: gnt %b, expected %b", t, hg[0][t], want); end
    end
  endfunction

  initial begin
    int oh, sp, ho, fa, run, best, cnt;
    foreach (req[l]) req[l] = '0;
    wreq = '0;
    void'($urandom(54));
    repeat (2) @(negedge clk);
    rst_n = 1;
    for (int c = 0; c < T; c++) begin
      @(negedge clk);
      for (int l = 0; l < 4; l++)
        for (int i = 0; i < N; i++)
          if (!(c > 0 && hr[l][c - 1][i] && !hg[l][c - 1][i])) req[l][i] = ($urandom_range(99) < 70);   // a waiting request stays
      wreq = '1;                                              // the weighted arbiter under full load
      #1;
      for (int l = 0; l < 4; l++) begin hr[l].push_back(req[l]); hg[l].push_back(gnt[l]); end
      wh.push_back(wgnt);
    end
    @(negedge clk);
    reference_rr();
    begin
      int c0[4], c1[4];
      int k1, k2, k3, k4;
      for (int l = 0; l < 4; l++) begin
        count(l, oh, sp, ho, fa);
        case (l)
          0: begin k1 = chk0.fails_onehot; k2 = chk0.fails_spurious; k3 = chk0.fails_hold; k4 = chk0.fails_fair; end
          1: begin k1 = chk1.fails_onehot; k2 = chk1.fails_spurious; k3 = chk1.fails_hold; k4 = chk1.fails_fair; end
          2: begin k1 = chk2.fails_onehot; k2 = chk2.fails_spurious; k3 = chk2.fails_hold; k4 = chk2.fails_fair; end
          default: begin k1 = chk3.fails_onehot; k2 = chk3.fails_spurious; k3 = chk3.fails_hold; k4 = chk3.fails_fair; end
        endcase
        if (k1 != oh || k2 != sp || k3 != ho || k4 != fa) begin
          errors++; $display("lane %0d: checker %0d %0d %0d %0d, reference %0d %0d %0d %0d", l, k1, k2, k3, k4, oh, sp, ho, fa);
        end
        if (l == 0 && (oh || sp || ho || fa)) begin errors++; $display("the correct arbiter failed a rule"); end
        if ((l == 1 || l == 2) && fa == 0) begin errors++; $display("lane %0d: fairness never failed", l); end
        if (l == 3 && oh == 0) begin errors++; $display("lane 3: one-hot never failed"); end
        if (ho) begin errors++; $display("lane %0d: the traffic broke the hold rule", l); end
      end
    end
    // the weighted arbiter, full load: requester i gets w_i of every 10 grants and waits at most 10 - w_i
    for (int i = 0; i < N; i++) begin
      cnt = 0; run = 0; best = 0;
      for (int t = 0; t < 400; t++) begin
        if (wh[t][i]) begin cnt++; run = 0; end else begin run++; if (run > best) best = run; end
      end
      if (cnt != 40 * weight[i]) begin errors++; $display("wrr share %0d: %0d of 400", i, cnt); end
      if (best != 10 - weight[i]) begin errors++; $display("wrr wait %0d: %0d", i, best); end
    end
    if (fixed_priority(4'b1011) != 4'b0001 || fixed_priority(4'b0000) != 4'b0000) begin errors++; $display("fixed_priority"); end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
