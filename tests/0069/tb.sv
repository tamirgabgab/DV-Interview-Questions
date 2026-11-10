// Question 0069: the page's Fenwick tree, passed, passed_merge, overtook, inversions,
// disorder, arrival_order and live_overtakes on the page's example, the extra examples,
// fixed arrays whose answers were computed by the page's Python (written here), and
// random arrays with and without ties against an O(n^2) count of every pair. The RTL monitor
// of the follow-up, ooo_monitor: the per-clock table of the page on 4 requests, random
// permutations with idle cycles and a reset in the middle against the count of every pair
// on 12 requests (no assertion fails, every coverage bin hit once the shaped traces ran,
// not before), and a copy with MAX_REORDER = 1 on a reversed trace (a_depth fails).
//@flags --assert --timing
//@page module ooo_monitor

module tb;
  //@page class Fenwick
  //@page function automatic idxq_t sort_count
  //@page function automatic void overtook
  //@page function automatic int inversions

  int errors = 0;

  function automatic void brute(input int done[], output int p[], output int o[]);
    int n = done.size();
    p = new[n]; o = new[n];
    for (int i = 0; i < n; i++) begin
      p[i] = 0; o[i] = 0;
      for (int j = i + 1; j < n; j++) if (done[j] < done[i]) p[i]++;
      for (int j = 0; j < i; j++) if (done[j] > done[i]) o[i]++;
    end
  endfunction

  function automatic bit same(int a[], int b[]);
    if (a.size() != b.size()) return 0;
    foreach (a[i]) if (a[i] != b[i]) return 0;
    return 1;
  endfunction

  function automatic void check(string name, input int done[], input int want_p[], input int want_o[]);
    int p[], pm[], o[], order[$], live[$], total = 0, inv;
    passed(done, p);
    passed_merge(done, pm);
    overtook(done, o);
    inv = inversions(done);
    arrival_order(done, order);
    live_overtakes(order, done.size(), live);
    if (!same(p, want_p)) begin errors++; $display("%s: passed %p, expected %p", name, p, want_p); end
    if (!same(pm, want_p)) begin errors++; $display("%s: passed_merge %p, expected %p", name, pm, want_p); end
    if (!same(o, want_o)) begin errors++; $display("%s: overtook %p, expected %p", name, o, want_o); end
    foreach (want_p[i]) total += want_p[i];
    if (inv != total) begin errors++; $display("%s: inversions %0d, expected %0d", name, inv, total); end
    total = 0;
    foreach (want_o[i]) total += want_o[i];
    if (inv != total) begin errors++; $display("%s: sum of overtook %0d differs", name, total); end
    if (live.size() != done.size()) begin errors++; $display("%s: live size", name); end
    foreach (order[k]) begin
      if (live[k] != want_p[order[k]]) begin errors++; $display("%s: live[%0d] = %0d, passed[%0d] = %0d", name, k, live[k], order[k], want_p[order[k]]); end
      if (k > 0 && done[order[k - 1]] > done[order[k]]) begin errors++; $display("%s: arrival order", name); end
      if (k > 0 && done[order[k - 1]] == done[order[k]] && order[k - 1] > order[k]) begin errors++; $display("%s: ties out of send order", name); end
    end
    if (done.size() >= 2) begin
      real d = disorder(done);
      real want = real'(inv) / (done.size() * (done.size() - 1) / 2);
      if (d < want - 1e-9 || d > want + 1e-9) begin errors++; $display("%s: disorder %f, expected %f", name, d, want); end
    end else if (disorder(done) != 0.0) begin errors++; $display("%s: disorder of a short array", name); end
  endfunction

  // --- the RTL monitor ----------------------------------------------------------------
  logic clk = 0, rst_n = 0, v4 = 0, v12 = 0, v6 = 0;
  always #5 clk = ~clk;
  logic [1:0] s4;
  logic [3:0] s12;
  logic [2:0] s6;
  logic [2:0] p4, m4;
  logic [4:0] p12, m12;
  logic [3:0] p6, m6;
  logic [31:0] t4, t12, t6;
  // (a second instance of one parameterization trips a Verilator covergroup bug: three sizes)
  ooo_monitor #(.N(4)) mon4(.clk, .rst_n, .rsp_valid(v4), .rsp_seq(s4), .passed(p4), .max_passed(m4), .total(t4));
  ooo_monitor #(.N(12)) mon12(.clk, .rst_n, .rsp_valid(v12), .rsp_seq(s12), .passed(p12), .max_passed(m12), .total(t12));
  ooo_monitor #(.N(6), .MAX_REORDER(1)) mon6(.clk, .rst_n, .rsp_valid(v6), .rsp_seq(s6), .passed(p6), .max_passed(m6), .total(t6));

  task automatic reset();
    @(negedge clk); rst_n = 0; v4 = 0; v12 = 0; v6 = 0;
    @(negedge clk); rst_n = 1;
  endtask

  // one trace of 12 requests through mon12: the responses in the order of `order`, with
  // `idle` empty clocks between them; passed of every response against every pair
  task automatic run12(input int order[$], input int idle);
    int done[] = new[12], p[], o[];
    foreach (order[k]) done[order[k]] = k;
    brute(done, p, o);
    reset();
    foreach (order[k]) begin
      repeat (idle) @(negedge clk);
      v12 = 1; s12 = 4'(order[k]);
      #1 if (int'(p12) != p[order[k]]) begin errors++; $display("mon12: passed %0d for request %0d, expected %0d", p12, order[k], p[order[k]]); end
      @(negedge clk); v12 = 0;
    end
    begin
      int mx = 0, tot = 0;
      foreach (p[i]) begin tot += p[i]; if (p[i] > mx) mx = p[i]; end
      if (int'(m12) != mx || int'(t12) != tot) begin errors++; $display("mon12: max %0d total %0d, expected %0d %0d", m12, t12, mx, tot); end
    end
    @(negedge clk);
  endtask

  initial begin
    int done[], p[], o[];
    Fenwick ft;
    // the Fenwick tree itself: the example of the idea on 8 cells
    ft = new(8);
    ft.add(3);
    if (ft.tree[3] != 1 || ft.tree[4] != 1 || ft.tree[8] != 1 || ft.tree[1] != 0 || ft.tree[2] != 0) begin errors++; $display("add(3)"); end
    ft.add(5); ft.add(7);
    if (ft.prefix(7) != 3 || ft.prefix(4) != 1 || ft.prefix(2) != 0 || ft.prefix(8) != 3 || ft.prefix(0) != 0) begin errors++; $display("prefix"); end
    if ((12 & -12) != 4 || (6 & -6) != 2 || (8 & -8) != 8 || (7 & -7) != 1) begin errors++; $display("lowest set bit"); end
    // the page's example and the extra examples
    done = '{5, 2, 6, 1};
    check("example", done, '{2, 1, 1, 0}, '{0, 1, 0, 3});
    if (inversions(done) != 4) begin errors++; $display("example: inversions"); end
    done = '{7, 3, 9, 2, 8};
    check("extra example", done, '{2, 1, 2, 0, 0}, '{0, 1, 0, 3, 1});
    if (inversions(done) != 5) begin errors++; $display("extra example: inversions"); end
    // answers written by the page's Python (tests/0069/test_0069_code.py checks the same code)
    done = '{5, 5, 5};
    check("all equal", done, '{0, 0, 0}, '{0, 0, 0});
    done = '{9, 8, 7, 6, 5, 4};
    check("reversed", done, '{5, 4, 3, 2, 1, 0}, '{0, 1, 2, 3, 4, 5});
    if (disorder(done) != 1.0) begin errors++; $display("reversed: disorder"); end
    done = '{1, 2, 3, 4};
    check("in order", done, '{0, 0, 0, 0}, '{0, 0, 0, 0});
    if (disorder(done) != 0.0) begin errors++; $display("in order: disorder"); end
    done = '{12, 7, 7, 30, 1, 7, 12};
    check("ties", done, '{4, 1, 1, 3, 0, 0, 0}, '{0, 1, 1, 0, 4, 2, 1});
    done = '{1000000, 3, 1000000, 999999, 3};
    check("large times", done, '{3, 0, 2, 1, 0}, '{0, 1, 0, 2, 3});
    done = new[0];
    check("empty", done, done, done);
    done = '{42};
    check("one", done, '{0}, '{0});
    // random arrays: distinct-ish, many ties, long
    for (int r = 0; r < 3000; r++) begin
      int n = $urandom_range(0, r < 2000 ? 14 : 60);
      done = new[n];
      foreach (done[i]) done[i] = (r % 3 == 0) ? $urandom_range(0, 3) : (r % 3 == 1) ? $urandom_range(0, 99) : $urandom_range(0, 1000000);
      brute(done, p, o);
      check($sformatf("run %0d", r), done, p, o);
    end
    // --- the monitor: the page's table, clock by clock (the times 5 2 6 1 are the clocks)
    begin
      int seq_at[7] = '{-1, 3, 1, -1, -1, 0, 2};          // the request answered at clocks 1..6
      int want_p[7] = '{0, 0, 1, 0, 0, 2, 1}, want_m[7] = '{0, 0, 1, 1, 1, 2, 2}, want_t[7] = '{0, 0, 1, 1, 1, 3, 4};
      logic [3:0] want_a[7] = '{4'b0000, 4'b1000, 4'b1010, 4'b1010, 4'b1010, 4'b1011, 4'b1111};
      reset();
      for (int c = 1; c <= 6; c++) begin
        v4 = seq_at[c] >= 0; s4 = 2'(seq_at[c] >= 0 ? seq_at[c] : 0);
        #1 if (v4 && int'(p4) != want_p[c]) begin errors++; $display("mon4 clock %0d: passed %0d", c, p4); end
        @(negedge clk);
        if (mon4.answered !== want_a[c] || int'(m4) != want_m[c] || int'(t4) != want_t[c]) begin
          errors++; $display("mon4 clock %0d: answered %b max %0d total %0d", c, mon4.answered, m4, t4);
        end
      end
      v4 = 0;
    end
    // random permutations of 12 requests, with idle clocks; a reset in the middle of one
    begin
      int order[$];
      for (int r = 0; r < 300; r++) begin
        order = {};
        for (int i = 0; i < 12; i++) order.push_back(i);
        order.shuffle();
        run12(order, r % 3);
      end
      if (mon12.cov.get_inst_coverage() > 99.999) begin errors++; $display("random traces alone closed the coverage"); end
      // a reset in the middle: the bits, the maximum and the sum start again
      reset();
      v12 = 1; s12 = 4'd11; @(negedge clk); s12 = 4'd10; @(negedge clk); v12 = 0;
      if (int'(t12) != 1) begin errors++; $display("mon12 before the reset: total %0d", t12); end
      rst_n = 0; @(negedge clk);
      if (mon12.answered !== '0 || m12 != 0 || t12 != 0) begin errors++; $display("mon12 in reset"); end
      // the shaped traces of the coverage: in order (0%), one overtake (1-10%), a few (11-30%)
      order = '{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; run12(order, 0);
      order = '{1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; run12(order, 1);
      order = '{4, 3, 2, 1, 0, 5, 6, 7, 8, 9, 10, 11}; run12(order, 0);
      order = '{11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}; run12(order, 2);
      if (mon12.cov.get_inst_coverage() < 99.999) begin errors++; $display("mon12 coverage %f", mon12.cov.get_inst_coverage()); end
      if (mon12.fails != 0 || mon4.fails != 0) begin errors++; $display("assertions failed: %0d %0d", mon12.fails, mon4.fails); end
    end
    // MAX_REORDER = 1 on a reversed trace: the third response already has 2 overtakes;
    // and a second response to one request trips a_once
    begin
      reset();
      for (int i = 5; i >= 0; i--) begin v6 = 1; s6 = 3'(i); @(negedge clk); end
      v6 = 0;
      if (mon6.fails != 4) begin errors++; $display("mon6: %0d depth failures, expected 4", mon6.fails); end
      if (int'(m6) != 5 || int'(t6) != 15) begin errors++; $display("mon6: max %0d total %0d", m6, t6); end
      v6 = 1; s6 = 3'd5; @(negedge clk); v6 = 0;
      if (mon6.fails != 5) begin errors++; $display("mon6: a repeated response was not caught (%0d)", mon6.fails); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
