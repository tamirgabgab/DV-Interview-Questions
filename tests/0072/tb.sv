// Question 0072: the page's rotate_reversals, rotate_cycles and linearize against the
// definition a[i] = old[(i + k) mod n] on every n up to 20 and every k up to 2n, and the
// number of memory accesses of linearize (2n).
module tb;
  //@page function automatic void reverse_range
  //@page function automatic int gcd_of
  //@page class Ram;

  int errors = 0;

  function automatic bit same_as_rotation(int a[], int b[], int k);
    int n = a.size();
    for (int i = 0; i < n; i++) if (b[i] != a[(i + k) % n]) return 0;
    return 1;
  endfunction

  initial begin
    int a[], b[], c[];
    Ram ram;
    for (int n = 0; n <= 20; n++)
      for (int k = 0; k <= 2 * n; k++) begin
        a = new[n];
        foreach (a[i]) a[i] = 100 + i;
        b = a; c = a;
        rotate_reversals(b, k);
        rotate_cycles(c, k);
        if (n > 0 && (!same_as_rotation(a, b, k) || !same_as_rotation(a, c, k))) begin
          errors++; $display("n=%0d k=%0d", n, k);
        end
      end
    for (int n = 1; n <= 20; n++)
      for (int h = 0; h < n; h++) begin
        a = new[n];
        foreach (a[i]) a[i] = (i - h + n) % n;            // the oldest, 0, sits at h
        ram = new(a);
        linearize(ram, h);
        foreach (ram.mem[i]) if (ram.mem[i] != i) begin errors++; $display("linearize n=%0d h=%0d", n, h); break; end
        if (ram.cycles != (h == 0 ? 0 : 2 * n)) begin errors++; $display("cycles n=%0d h=%0d: %0d", n, h, ram.cycles); end
      end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
