// Question 0064: the page's one_pan, two_pans, placement and balances on every load each
// mode weighs (and the load just above it refused), checked by the sum of the digits times
// the weights, and on random large loads.
module tb;
  //@page function automatic bit one_pan
  //@page function automatic bit two_pans
  //@page function automatic bit placement

  int errors = 0;

  // the load the digits weigh, sum d_i * base^i
  function automatic longint value(int digits[$], int base);
    longint v = 0, w = 1;
    foreach (digits[i]) begin v += digits[i] * w; w *= base; end
    return v;
  endfunction

  function automatic int bound(int k, int c, bit two);
    int b = two ? 2 * c + 1 : c + 1, p = 1;
    repeat (k) p *= b;
    return two ? (p - 1) / 2 : p - 1;
  endfunction

  initial begin
    int d[$], e[$], top, n, k, c, base;
    bit two, ok;
    // the page's examples
    void'(one_pan(40, 6, d));
    if (d != '{0, 0, 0, 1, 0, 1}) begin errors++; $display("one_pan(40) = %p", d); end
    void'(two_pans(25, 4, d));
    if (d != '{1, -1, 0, 1}) begin errors++; $display("two_pans(25) = %p", d); end
    void'(placement(40, 3, 2, 1, d));
    if (d != '{0, -2, 2} || !balances(40, 2, 1, d)) begin errors++; $display("placement(40, c = 2) = %p", d); end
    if (two_pans(41, 4, d) || one_pan(64, 6, d)) begin errors++; $display("a load above the bound was accepted"); end
    d = '{0, -3, 2};
    if (balances(40, 2, 1, d)) begin errors++; $display("three copies accepted with c = 2"); end
    d = '{-1, 2};
    if (balances(5, 1, 0, d)) begin errors++; $display("a weight beside the load on one pan"); end
    // every load of every mode
    for (c = 1; c <= 4; c++)
      for (int t = 0; t < 2; t++)
        for (k = 1; k <= (c == 1 ? 5 : 3); k++) begin
          two = t; base = two ? 2 * c + 1 : c + 1; top = bound(k, c, two);
          for (n = 0; n <= top; n++) begin
            ok = placement(n, k, c, two, d);
            if (!ok || d.size() != k || value(d, base) != n || !balances(n, c, two, d)) begin
              errors++; $display("placement(%0d, k = %0d, c = %0d, two = %0d) = %p", n, k, c, two, d);
            end
            if (c == 1) begin
              if (two) void'(two_pans(n, k, e)); else void'(one_pan(n, k, e));
              if (e != d) begin errors++; $display("c = 1, n = %0d: %p vs %p", n, e, d); end
            end
          end
          if (placement(top + 1, k, c, two, d)) begin errors++; $display("load %0d above the bound accepted", top + 1); end
        end
    // random large loads
    for (int t = 0; t < 2000; t++) begin
      c = $urandom_range(1, 4); two = $urandom_range(0, 1); k = $urandom_range(1, 10);
      base = two ? 2 * c + 1 : c + 1;
      while (bound(k, c, two) > 1000000000 || bound(k, c, two) < 0) k--;
      n = $urandom_range(0, bound(k, c, two));
      ok = placement(n, k, c, two, d);
      if (!ok || value(d, base) != n || !balances(n, c, two, d)) begin errors++; $display("random %0d k = %0d c = %0d: %p", n, k, c, d); end
    end
    for (int t = 0; t < 500; t++) begin
      n = $urandom_range(0, (1 << 30) - 1);
      ok = two_pans(n, 20, d);                   // (3^20 - 1) / 2 is above 2^30
      if (!ok || value(d, 3) != n) begin errors++; $display("two_pans(%0d, 20) = %p", n, d); end
      ok = one_pan(n, 30, d);
      if (!ok || value(d, 2) != n) begin errors++; $display("one_pan(%0d, 30) = %p", n, d); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
