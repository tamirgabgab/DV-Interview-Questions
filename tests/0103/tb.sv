//@flags --timing
// Question 0103: the page's SystemVerilog. lpm_naive on the page's example (the dotted quads,
// the normalized prefix, the /0 mask and the shift traps); the trie class and the mtrie class
// (strides 1, 2, 4 and 8) against lpm_naive on random tables of 8, 16 and 32 bits, the trie with
// removals in a random order; the numbers of the page (37 nodes, the table of strides); and the
// lpm_pipe module: the page's per-clock table on 8 bits by 2, then three pipelines (8 by 2,
// 8 by 1, 16 by 4) loaded from random mtrie tables and fed one lookup a clock with random
// bubbles, every output checked in order against lpm_naive, with counters that the lookups
// covered an answer from /0, from a prefix of length W, nested prefixes and no match.
//@page function automatic int lpm_naive
//@page class trie
//@page class mtrie
//@page module lpm_pipe

// A random table of w-bit rows, some nested under an earlier row, the values not normalized
function automatic void random_table(int w, int n, bit with_default, ref route_t rt[$]);
  int k, j;
  logic [31:0] v;
  route_t r;
  rt.delete();
  for (int i = 0; i < n; i++) begin
    case ($urandom_range(3))
      0: k = 0;
      1: k = w;
      default: k = $urandom_range(w, 1);
    endcase
    v = 32'($urandom()) & prefix_mask(w, w);
    if (rt.size() > 0 && $urandom_range(9) < 4) begin
      j = $urandom_range(rt.size() - 1);
      k = $urandom_range(w, rt[j].len);
      v = (rt[j].value & prefix_mask(rt[j].len, w)) | (v & ~prefix_mask(rt[j].len, w));
    end
    r.value = v; r.len = k; r.hop = $urandom_range(7);
    rt.push_back(r);
  end
  if (with_default) begin
    r.value = 32'($urandom()) & prefix_mask(w, w); r.len = 0; r.hop = 9;
    rt.push_back(r);
  end
endfunction

// The length of the longest matching row (-1: none) and how many rows match
function automatic void match_count(route_t rt[$], logic [31:0] addr, int w, output int longest, output int count);
  longest = -1; count = 0;
  foreach (rt[i])
    if (((addr ^ rt[i].value) & prefix_mask(rt[i].len, w)) == 0) begin
      count++;
      if (rt[i].len > longest) longest = rt[i].len;
    end
endfunction

// Addresses to try: random ones, and the first and last address of every row and their neighbours
function automatic void probes(route_t rt[$], int w, int n, ref logic [31:0] out[$]);
  logic [31:0] lo, hi, all;
  all = prefix_mask(w, w);
  out.delete();
  repeat (n) out.push_back(32'($urandom()) & all);
  foreach (rt[i]) begin
    lo = rt[i].value & prefix_mask(rt[i].len, w);
    hi = lo | (all & ~prefix_mask(rt[i].len, w));
    out.push_back(lo); out.push_back(hi); out.push_back((lo - 1) & all); out.push_back((hi + 1) & all);
  end
endfunction

// One pipeline on random tables: load the memories from an mtrie, send lookups one a clock with
// random bubbles, and check every output in order against lpm_naive
module harness #(parameter int W = 8, S = 2, N = 16, TABLES = 150)
  (input logic clk, output int errors, output bit done, output int cov_default, cov_full, cov_nested, cov_none);
  localparam int L = W / S, F = 1 << S, HW = 4, PW = $clog2(N);
  logic          rst_n = 0, in_valid = 0, wr_en = 0, wr_hop_ok = 0, wr_child_ok = 0;
  logic [W-1:0]  in_addr = '0;
  int            wr_level = 0, wr_index = 0;
  logic [HW-1:0] wr_hop = '0;
  logic [PW-1:0] wr_child = '0;
  logic          out_valid, out_hit;
  logic [HW-1:0] out_hop;
  int            want[$], sent = 0, seen = 0;
  logic [W-1:0]  sent_addr[$];

  lpm_pipe #(.W(W), .S(S), .HW(HW), .N(N)) dut (.*);

  task automatic fail(string what);
    errors++;
    if (errors < 10) $display("W=%0d S=%0d: %s", W, S, what);
  endtask

  // the monitor: every valid output against the head of the scoreboard's queue
  always @(negedge clk) if (rst_n && out_valid) begin
    if (want.size() == 0) fail("an output with no lookup sent");
    else begin
      if (out_hit != (want[0] >= 0) || (out_hit && out_hop != HW'(want[0])))
        fail($sformatf("addr %0d: hit %0d hop %0d, want %0d", sent_addr[0], out_hit, out_hop, want[0]));
      void'(want.pop_front()); void'(sent_addr.pop_front());
      seen++;
    end
  end

  task automatic load(mtrie t);
    mentry_t e;
    for (int d = 0; d < L; d++) begin
      if (t.lv[d].size() > N * F) fail($sformatf("level %0d needs %0d nodes", d, t.lv[d].size() / F));
      for (int i = 0; i < N * F; i++) begin
        wr_en = 1; wr_level = d; wr_index = i;
        if (i < t.lv[d].size()) begin            // the fields an entry does not use get random bits
          e = t.lv[d][i];
          wr_hop_ok = e.hop >= 0; wr_hop = e.hop >= 0 ? HW'(e.hop) : HW'($urandom());
          wr_child_ok = e.child >= 0; wr_child = e.child >= 0 ? PW'(e.child) : PW'($urandom());
        end else begin                           // a node no lookup reaches: anything at all
          wr_hop_ok = 1'($urandom()); wr_hop = HW'($urandom());
          wr_child_ok = 1'($urandom()); wr_child = PW'($urandom());
        end
        @(negedge clk);
      end
    end
    wr_en = 0;
  endtask

  initial begin
    route_t rt[$];
    logic [31:0] addrs[$];
    mtrie t;
    int longest, count, ans;
    errors = 0; done = 0; cov_default = 0; cov_full = 0; cov_nested = 0; cov_none = 0;
    repeat (2) @(negedge clk);
    rst_n = 1;
    for (int n = 0; n < TABLES; n++) begin
      random_table(W, $urandom_range(10), $urandom_range(1), rt);
      t = new(W, S);
      foreach (rt[i]) t.insert(rt[i].value, rt[i].len, rt[i].hop);
      load(t);
      probes(rt, W, 20, addrs);
      foreach (addrs[i]) begin
        while ($urandom_range(4) == 0) begin in_valid = 0; @(negedge clk); end   // a bubble
        ans = lpm_naive(rt, addrs[i], W);
        if (t.lookup(addrs[i]) != ans) fail($sformatf("mtrie lookup %0d", addrs[i]));
        match_count(rt, addrs[i], W, longest, count);
        if (longest == 0) cov_default++;
        if (longest == W) cov_full++;
        if (count >= 2) cov_nested++;
        if (ans < 0) cov_none++;
        in_valid = 1; in_addr = W'(addrs[i]);
        want.push_back(ans); sent_addr.push_back(W'(addrs[i])); sent++;
        @(negedge clk);
      end
      in_valid = 0;
      repeat (L + 1) @(negedge clk);
      if (want.size() != 0) fail($sformatf("%0d lookups never came out", want.size()));
      want.delete(); sent_addr.delete();
    end
    if (seen != sent) fail($sformatf("%0d outputs for %0d lookups", seen, sent));
    done = 1;
  end
endmodule

module tb;
  logic clk = 0;
  always #5 clk = ~clk;
  int errors = 0;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // the per-clock table of the page: 8 bits by 2, the pipe8 table, five lookups and one bubble
  logic       rst_n = 0, in_valid = 0, wr_en = 0, wr_hop_ok = 0, wr_child_ok = 0;
  logic [7:0] in_addr = 0;
  int         wr_level = 0, wr_index = 0;
  logic [3:0] wr_hop = 0;
  logic [2:0] wr_child = 0;
  logic       out_valid, out_hit;
  logic [3:0] out_hop;
  lpm_pipe #(.W(8), .S(2), .HW(4), .N(8)) pipe8 (.*);

  string want_trace[8] = '{"185:A . . .", "182:A 185:B . .", ". 182:B 185:B .", "64:E . 182:C 185:B", "3:D 64:E . 182:C", ". 3:D 64:E .", ". . 3:D 64:E", ". . . 3:D"};

  function automatic string slot(logic v, logic [7:0] a, logic hit, logic [3:0] hop);
    string names = "ABCDE";
    if (!v) return ".";
    return $sformatf("%0d:%s", a, hit ? names.substr(hop, hop) : "-");
  endfunction

  function automatic string stages();
    return {slot(pipe8.st[0].v, pipe8.st[0].a, pipe8.st[0].hit, pipe8.st[0].hop), " ",
            slot(pipe8.st[1].v, pipe8.st[1].a, pipe8.st[1].hit, pipe8.st[1].hop), " ",
            slot(pipe8.st[2].v, pipe8.st[2].a, pipe8.st[2].hit, pipe8.st[2].hop), " ",
            slot(pipe8.st[3].v, pipe8.st[3].a, pipe8.st[3].hit, pipe8.st[3].hop)};
  endfunction

  int e1, e2, e3;
  bit d1, d2, d3;
  int c[3][4];
  harness #(.W(8), .S(2), .N(16)) h1 (.clk, .errors(e1), .done(d1), .cov_default(c[0][0]), .cov_full(c[0][1]), .cov_nested(c[0][2]), .cov_none(c[0][3]));
  harness #(.W(8), .S(1), .N(16)) h2 (.clk, .errors(e2), .done(d2), .cov_default(c[1][0]), .cov_full(c[1][1]), .cov_nested(c[1][2]), .cov_none(c[1][3]));
  harness #(.W(16), .S(4), .N(16)) h3 (.clk, .errors(e3), .done(d3), .cov_default(c[2][0]), .cov_full(c[2][1]), .cov_nested(c[2][2]), .cov_none(c[2][3]));

  initial begin
    route_t ex[$], rt[$], left[$];
    logic [31:0] addrs[$], q[6];
    int want[6] = '{2, 1, 0, 4, 3, 3};       // C, B, A, E, D, D
    int ins[5] = '{185, 182, -1, 64, 3};
    int st_nodes[4] = '{35, 17, 8, 4}, st_entries[4] = '{70, 68, 128, 1024}, strides[4] = '{1, 2, 4, 8};
    int ws[3] = '{8, 16, 32};
    int sh, n, k, longest, count;
    logic [4:0] sh5;
    trie t;
    mtrie m;
    route_t r;

    // part a: the example of the page, A = 0, B = 1, C = 2, D = 3, E = 4
    ex.push_back(make_route({8'd10, 8'd0, 8'd0, 8'd0}, 8, 0));
    ex.push_back(make_route({8'd10, 8'd1, 8'd0, 8'd0}, 16, 1));
    ex.push_back(make_route({8'd10, 8'd1, 8'd2, 8'd0}, 24, 2));
    ex.push_back(make_route({8'd172, 8'd16, 8'd0, 8'd0}, 12, 4));
    ex.push_back(make_route({8'd0, 8'd0, 8'd0, 8'd0}, 0, 3));
    q = '{{8'd10, 8'd1, 8'd2, 8'd3}, {8'd10, 8'd1, 8'd3, 8'd4}, {8'd10, 8'd200, 8'd0, 8'd1},
          {8'd172, 8'd20, 8'd1, 8'd1}, {8'd172, 8'd32, 8'd0, 8'd1}, {8'd8, 8'd8, 8'd8, 8'd8}};
    if (q[0] != 32'd167838211) fail("10.1.2.3 is not 167838211");
    r = make_route({8'd10, 8'd1, 8'd2, 8'd3}, 16, 1);
    if (r.value != {8'd10, 8'd1, 8'd0, 8'd0}) fail("10.1.2.3/16 is not normalized to 10.1.0.0/16");
    if (prefix_mask(0) != 0 || prefix_mask(32) != 32'hffffffff || prefix_mask(8) != 32'hff000000) fail("prefix_mask");
    if (prefix_mask(3, 8) != 32'he0) fail("prefix_mask(3, 8)");
    // the trap: a shift by 32 is 0 in SystemVerilog, but 32 - k in a 5-bit field wraps to 0
    sh = 32;
    if ((32'hffffffff << sh) != 0) fail("a shift by 32 is not 0");
    sh5 = 5'(32 - 0);
    if ((32'hffffffff << sh5) != 32'hffffffff) fail("a 5-bit shift amount does not wrap");
    t = new();
    foreach (ex[i]) t.insert(ex[i].value, ex[i].len, ex[i].hop);
    if (t.nodes != 37) fail($sformatf("the example trie has %0d nodes, want 37", t.nodes));
    foreach (q[i]) begin
      if (lpm_naive(ex, q[i]) != want[i]) fail($sformatf("lpm_naive lookup %0d", i));
      if (t.lookup(q[i]) != want[i]) fail($sformatf("trie lookup %0d", i));
    end
    left = ex; left.pop_back();
    if (lpm_naive(left, q[5]) != -1) fail("8.8.8.8 without a default");
    foreach (strides[i]) begin
      m = new(32, strides[i]);
      foreach (ex[j]) m.insert(ex[j].value, ex[j].len, ex[j].hop);
      n = 0;
      foreach (m.lv[d]) n += m.lv[d].size() / m.f;
      if (n != st_nodes[i] || m.entries() != st_entries[i])
        fail($sformatf("s = %0d: %0d nodes %0d entries", strides[i], n, m.entries()));
      foreach (q[j]) if (m.lookup(q[j]) != want[j]) fail($sformatf("s = %0d lookup %0d", strides[i], j));
    end
    void'(t.remove({8'd10, 8'd0, 8'd0, 8'd0}, 8));
    if (t.nodes != 37 || t.lookup(q[2]) != 3 || t.lookup(q[0]) != 2) fail("removing 10.0.0.0/8");

    // the classes on random tables: the trie with removals, the mtrie at every stride
    foreach (ws[wi]) for (int n2 = 0; n2 < 200; n2++) begin
      random_table(ws[wi], $urandom_range(10), $urandom_range(1), rt);
      t = new(ws[wi]);
      foreach (rt[i]) t.insert(rt[i].value, rt[i].len, rt[i].hop);
      probes(rt, ws[wi], 10, addrs);
      foreach (addrs[i]) if (t.lookup(addrs[i]) != lpm_naive(rt, addrs[i], ws[wi]))
        fail($sformatf("w = %0d: trie lookup %0d", ws[wi], addrs[i]));
      foreach (strides[si]) begin
        m = new(ws[wi], strides[si]);
        left = rt;
        left.shuffle();                        // any order: a longer prefix keeps its entries
        foreach (left[i]) m.insert(left[i].value, left[i].len, left[i].hop);
        foreach (addrs[i]) if (m.lookup(addrs[i]) != lpm_naive(left, addrs[i], ws[wi]))
          fail($sformatf("w = %0d s = %0d: mtrie lookup %0d", ws[wi], strides[si], addrs[i]));
      end
      // remove the rows from the last one: a prefix given twice keeps its later hop until then
      left = rt;
      while (left.size() > 0) begin
        r = left.pop_back();
        k = -1;
        foreach (left[i]) if (left[i].len == r.len && ((left[i].value ^ r.value) & prefix_mask(r.len, ws[wi])) == 0) k = i;
        if (k >= 0) t.insert(left[k].value, left[k].len, left[k].hop);   // the same prefix earlier: its hop again
        else if (!t.remove(r.value, r.len)) fail("remove did not find a prefix");
        foreach (addrs[i]) if (t.lookup(addrs[i]) != lpm_naive(left, addrs[i], ws[wi]))
          fail($sformatf("w = %0d: trie lookup %0d after a removal", ws[wi], addrs[i]));
      end
      if (t.nodes != 1) fail($sformatf("%0d nodes left after removing every row", t.nodes));
    end

    // the page's per-clock table
    m = new(8, 2);
    m.insert(0, 0, 3); m.insert(8'd128, 1, 0); m.insert(8'd160, 3, 1); m.insert(8'd176, 5, 2); m.insert(8'd64, 2, 4);
    repeat (2) @(negedge clk);
    rst_n = 1;
    for (int d = 0; d < 4; d++)
      for (int i = 0; i < 8 * 4; i++) begin
        wr_en = 1; wr_level = d; wr_index = i;
        if (i < m.lv[d].size()) begin
          wr_hop_ok = m.lv[d][i].hop >= 0; wr_hop = 4'(m.lv[d][i].hop);
          wr_child_ok = m.lv[d][i].child >= 0; wr_child = 3'(m.lv[d][i].child);
        end else begin
          wr_hop_ok = 0; wr_child_ok = 0;
        end
        @(negedge clk);
      end
    wr_en = 0;
    for (int c2 = 0; c2 < 8; c2++) begin
      in_valid = c2 < 5 && ins[c2] >= 0;
      in_addr = c2 < 5 ? 8'(ins[c2]) : 8'd0;
      @(negedge clk);
      if (stages() != want_trace[c2]) fail($sformatf("clock %0d: %s, want %s", c2 + 1, stages(), want_trace[c2]));
    end
    in_valid = 0;

    wait (d1 && d2 && d3);
    errors += e1 + e2 + e3;
    foreach (c[i, j]) if (c[i][j] == 0) fail($sformatf("pipeline %0d: coverage counter %0d is 0", i + 1, j));
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
