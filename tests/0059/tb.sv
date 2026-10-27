// Question 0059: the page's next_same / prev_same against a search number by number (every
// number of 10 bits, and random 32-bit numbers next to the top), rank_same against a count
// and unrank_same as its inverse; the page's numbers (99, 80, 24).
module tb;
  //@page function automatic logic [31:0] next_same
  //@page function automatic logic [31:0] prev_same
  //@page function automatic longint unsigned binom

  int errors = 0;

  function automatic logic [31:0] search_next(logic [31:0] x, int w);
    for (longint y = longint'(x) + 1; y < (64'd1 << w); y++)
      if ($countones(32'(y)) == $countones(x)) return 32'(y);
    return '0;
  endfunction

  initial begin
    logic [31:0] x, y, z;
    longint unsigned count[33];
    if (next_same(92) != 99 || prev_same(96) != 80 || rank_same(92) != 24 || rank_same(99) != 25) begin
      errors++; $display("page numbers: %0d %0d %0d", next_same(92), prev_same(96), rank_same(92));
    end
    if (next_same(0) != 0 || prev_same(0) != 0 || next_same(32'hF000_0000) != 0) begin errors++; $display("edges"); end
    // every number of 10 bits in order: next is the search, rank counts, unrank inverts
    foreach (count[k]) count[k] = 0;
    for (int v = 1; v < 1024; v++) begin
      x = 32'(v);
      z = search_next(x, 10);
      y = next_same(x);
      if (z != 0 && y != z) begin errors++; $display("next %0d: %0d vs %0d", v, y, z); end
      if (z != 0 && prev_same(z) != x) begin errors++; $display("prev %0d", z); end
      if (rank_same(x) != count[$countones(x)]) begin errors++; $display("rank %0d: %0d vs %0d", v, rank_same(x), count[$countones(x)]); end
      if (unrank_same(rank_same(x), $countones(x)) != x) begin errors++; $display("unrank %0d", v); end
      count[$countones(x)]++;
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
