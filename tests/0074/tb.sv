// Question 0074: the page's rotate90 against new(i, j) = old(n-1-j, i) on every n up to 12,
// and transpose / transpose_no_marks against the definition on every m, n up to 12.
module tb;
  //@page function automatic void rotate90
  //@page function automatic void transpose(
  //@page function automatic void transpose_no_marks

  int errors = 0;

  initial begin
    int a[], b[], c[];
    for (int n = 0; n <= 12; n++) begin
      a = new[n * n];
      foreach (a[i]) a[i] = i;
      b = a;
      rotate90(b, n);
      for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
          if (b[i*n + j] != a[(n - 1 - j)*n + i]) begin errors++; $display("rotate90 n=%0d (%0d,%0d)", n, i, j); end
    end
    for (int m = 1; m <= 12; m++)
      for (int n = 1; n <= 12; n++) begin
        a = new[m * n];
        foreach (a[i]) a[i] = 1000 + i;
        b = a; c = a;
        transpose(b, m, n);
        transpose_no_marks(c, m, n);
        for (int i = 0; i < m; i++)
          for (int j = 0; j < n; j++)
            if (b[j*m + i] != a[i*n + j] || c[j*m + i] != a[i*n + j]) begin errors++; $display("transpose %0dx%0d (%0d,%0d)", m, n, i, j); end
      end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
