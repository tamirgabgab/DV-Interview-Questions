// Question 0060: the page's next_same / prev_same against a search number by number (every
// number of 10 bits, and random 32-bit numbers), next_zeros / prev_zeros against a search
// over lengths; the page's numbers (99, 80, 143).
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
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
