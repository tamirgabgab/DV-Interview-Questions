//@flags --assert --timing
// Question 0060: the page's next_same / prev_same against a search number by number (every
// number of 10 bits, and random 32-bit numbers), next_zeros / prev_zeros against a search
// over lengths; the page's numbers (99, 80, 143). The follow-ups' hardware: next_same_1c
// against the search on every 12-bit number and against next_same on random 32-bit ones;
// next_same_sva bound to it (no assertion fails, every coverage bin hit on the 12-bit sweep,
// some bins missed by random 32-bit numbers alone) and to a copy without the overflow check
// (its assertions fail).
//@page module next_same_1c
//@page module next_same_sva

// next_same_1c without the overflow check: a block at the top gives a small number
module next_same_bug #(parameter int W = 32) (input logic [W-1:0] x, output logic [W-1:0] nxt, output logic none);
  logic [W-1:0] c, r;
  always_comb begin
    c = x & -x;
    r = x + c;
    none = (x == '0);
    nxt = none ? '0 : r | ((x ^ r) >> 2) / c;
  end
endmodule

module tb;
  //@page function automatic logic [31:0] next_same
  //@page function automatic logic [31:0] prev_same
  //@page function automatic logic [31:0] next_zeros

  int errors = 0;

  function automatic logic [31:0] search_next(logic [31:0] x, int w);
    for (longint y = longint'(x) + 1; y < (64'd1 << w); y++)
      if ($countones(32'(y)) == $countones(x)) return 32'(y);
    return '0;
  endfunction

  function automatic int zeros_of(longint unsigned v);
    int L = 0;
    for (int p = 0; p < 64; p++) if (v[p]) L = p + 1;
    return L - $countones(v);
  endfunction

  logic clk = 0;
  always #5 clk = ~clk;
  logic [11:0] hx, hn;
  logic [9:0] bn;
  logic hnone, bnone;
  logic [31:0] wx, wn;
  logic wnone;
  next_same_1c #(12) dut12(.x(hx), .nxt(hn), .none(hnone));
  next_same_sva #(12) chk12(.clk, .x(hx), .nxt(hn), .none(hnone));
  // a second instance of one width trips a Verilator covergroup bug: the bad copy is 10 bits wide
  next_same_bug #(10) bug10(.x(hx[9:0]), .nxt(bn), .none(bnone));
  next_same_sva #(10) chkbug(.clk, .x(hx[9:0]), .nxt(bn), .none(bnone));
  next_same_1c #(32) dut32(.x(wx), .nxt(wn), .none(wnone));
  next_same_sva #(32) chk32(.clk, .x(wx), .nxt(wn), .none(wnone));

  initial begin
    logic [31:0] x, y, z;
    longint unsigned v2, want;
    if (next_same(92) != 99 || prev_same(96) != 80 || next_zeros(120) != 143 || prev_zeros(143) != 120) begin
      errors++; $display("page numbers: %0d %0d %0d", next_same(92), prev_same(96), next_zeros(120));
    end
    if (next_same(0) != 0 || prev_same(0) != 0 || next_same(32'hF000_0000) != 0) begin errors++; $display("edges"); end
    // every number of 10 bits: next is the search, prev inverts it; the zeros by a search
    for (int v = 1; v < 1024; v++) begin
      x = 32'(v);
      z = search_next(x, 10);
      y = next_same(x);
      if (z != 0 && y != z) begin errors++; $display("next %0d: %0d vs %0d", v, y, z); end
      if (z != 0 && prev_same(z) != x) begin errors++; $display("prev %0d", z); end
      want = 0;
      for (v2 = longint'(v) + 1; want == 0; v2++) if (zeros_of(v2) == zeros_of(v)) want = v2;
      if (next_zeros(x) != 32'(want)) begin errors++; $display("next_zeros %0d: %0d vs %0d", v, next_zeros(x), want); end
      want = 0;
      for (v2 = longint'(v) - 1; v2 > 0 && want == 0; v2--) if (zeros_of(v2) == zeros_of(v)) want = v2;
      if (prev_zeros(x) != 32'(want)) begin errors++; $display("prev_zeros %0d: %0d vs %0d", v, prev_zeros(x), want); end
    end
    // random 32-bit numbers: a neighbour with as many ones, and back
    for (int r = 0; r < 2000; r++) begin
      x = $urandom;
      y = next_same(x);
      if (y != 0 && (y <= x || $countones(y) != $countones(x) || prev_same(y) != x)) begin errors++; $display("rand %h -> %h", x, y); end
    end
    // the one-cycle module: every 12-bit number against the search, one per clock under the checker
    wx = 32'd1;
    for (int v = 0; v < 4096; v++) begin
      hx = 12'(v);
      #1;
      z = search_next(32'(v), 12);
      if (v == 0) z = 0;
      if (32'(hn) != z || hnone != (z == 0)) begin errors++; $display("next_same_1c %0d: %0d vs %0d", v, hn, z); end
      @(negedge clk);
    end
    // random 32-bit numbers against the page's next_same
    for (int r = 0; r < 300; r++) begin
      wx = $urandom;
      #1;
      if (wn != next_same(wx) || wnone != (next_same(wx) == 0)) begin errors++; $display("next_same_1c %h", wx); end
      @(negedge clk);
    end
    if (chk12.fails != 0 || chk32.fails != 0) begin errors++; $display("assertions failed: %0d %0d", chk12.fails, chk32.fails); end
    if (chkbug.fails == 0) begin errors++; $display("the copy without the overflow check passed"); end
    if (chk12.cov.get_inst_coverage() < 99.999) begin errors++; $display("12-bit coverage %f", chk12.cov.get_inst_coverage()); end
    if (chk32.cov.get_inst_coverage() > 99.999) begin errors++; $display("random 32-bit numbers alone closed the coverage"); end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
