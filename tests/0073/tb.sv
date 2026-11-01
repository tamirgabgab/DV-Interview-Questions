// Question 0073: the page's shuffles_to_return against shuffling a deck until it is back
// (every n up to 80, both kinds), and interleave against the definition on every even
// length up to 100.
module tb;
  //@page function automatic int shuffles_to_return
  //@page function automatic void interleave

  int errors = 0;

  // one perfect shuffle of 0..n-1, as the question defines it
  function automatic void shuffle_once(ref int d[], input bit is_out);
    int n = d.size();
    int h = is_out ? (n + 1) / 2 : n / 2;
    int r[], k = 0;
    r = new[n];
    for (int i = 0; i < n; i++) begin
      if (is_out) begin
        if (i < h) r[k++] = d[i];
        if (i < n - h) r[k++] = d[h + i];
      end else begin
        if (i < n - h) r[k++] = d[h + i];
        if (i < h) r[k++] = d[i];
      end
    end
    d = r;
  endfunction

  function automatic int by_shuffling(int n, bit is_out);
    int d[];
    bit back;
    d = new[n];
    foreach (d[i]) d[i] = i;
    for (int t = 1; t < 1000; t++) begin
      shuffle_once(d, is_out);
      back = 1;
      foreach (d[i]) if (d[i] != i) back = 0;
      if (back) return t;
    end
    return -1;
  endfunction

  initial begin
    int a[];
    for (int n = 2; n <= 80; n++)
      for (int o = 0; o <= 1; o++)
        if (shuffles_to_return(n, o[0]) != by_shuffling(n, o[0])) begin
          errors++; $display("n=%0d out=%0d: %0d vs %0d", n, o, shuffles_to_return(n, o[0]), by_shuffling(n, o[0]));
        end
    if (shuffles_to_return(52) != 8 || shuffles_to_return(52, 0) != 52) begin errors++; $display("52"); end
    for (int n = 0; n <= 100; n += 2) begin
      a = new[n];
      foreach (a[i]) a[i] = i;
      interleave(a);
      foreach (a[i]) if (a[i] != (i % 2 == 0 ? i / 2 : n / 2 + i / 2)) begin errors++; $display("interleave n=%0d at %0d", n, i); break; end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
