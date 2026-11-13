// Question 0108: the page's min_flips_naive, min_flips, min_flips_inplace, min_flips_2d_naive and
// min_flips_2d on the page's examples, on every array of up to 10 bits against a brute force over
// every set of window starts, on random fixable and random arrays, and on random grids.
module tb;
  //@page function automatic int min_flips_naive
  //@page function automatic int min_flips_2d_naive

  int errors = 0;

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; if (errors < 20) $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // the brute force: every set of starts, the fewest that makes every bit 1 (-1 if none)
  function automatic int brute(bit a[], int k);
    int n = a.size(), m = n - k + 1, best = -1, cnt;
    bit b[];
    if (m < 0) m = 0;
    for (int mask = 0; mask < (1 << m); mask++) begin
      b = a;
      cnt = 0;
      for (int p = 0; p < m; p++)
        if (mask[p]) begin
          cnt++;
          for (int j = p; j < p + k; j++) b[j] = ~b[j];
        end
      if (b.and() == 1'b1) begin
        if (best >= 0) begin errors++; $display("two solutions for one array"); end
        best = cnt;
      end
    end
    return best;
  endfunction

  // all three row functions; the in-place one must give the array back
  function automatic void row(string what, bit a[], int k, int want);
    int v[];
    v = new[a.size()];
    foreach (a[i]) v[i] = a[i];
    check({what, " naive"}, min_flips_naive(a, k), want);
    check({what, " queue"}, min_flips(a, k), want);
    check({what, " in place"}, min_flips_inplace(v, k), want);
    foreach (a[i]) if (v[i] != a[i]) begin errors++; $display("%s: the array changed", what); break; end
  endfunction

  function automatic void grid(string what, bit g[][], int k, int want);
    check({what, " naive"}, min_flips_2d_naive(g, k), want);
    check({what, " fast"}, min_flips_2d(g, k), want);
  endfunction

  initial begin
    bit a[];
    bit g[][];
    int n, k, R, C, want;
    // the page's examples
    a = '{0, 0, 0, 1, 0, 1, 1, 0};  row("example", a, 3, 3);
    a = '{0, 1, 0};                 row("010", a, 1, 2);
    a = '{1, 1, 0};                 row("110", a, 2, -1);
    g = new[4];
    foreach (g[r]) g[r] = new[5];
    g[0] = '{1, 0, 0, 1, 1}; g[1] = '{1, 0, 1, 0, 1}; g[2] = '{0, 0, 0, 1, 0}; g[3] = '{0, 0, 1, 0, 0};
    grid("grid", g, 2, 4);
    g[3][4] = 1;
    grid("grid, the corner flipped", g, 2, -1);
    // every array of up to 10 bits, every k
    for (n = 1; n <= 10; n++)
      for (int m = 0; m < (1 << n); m++) begin
        a = new[n];
        foreach (a[i]) a[i] = m[i];
        for (k = 1; k <= n + 1; k++) row($sformatf("n %0d, a %0d, k %0d", n, m, k), a, k, brute(a, k));
      end
    // random arrays of up to 200 bits: half of them fixable by construction
    for (int r = 0; r < 2000; r++) begin
      n = $urandom_range(200, 1);
      k = $urandom_range(n, 1);
      a = new[n];
      if (r % 2 == 0) begin
        foreach (a[i]) a[i] = 1;
        want = 0;
        for (int p = 0; p + k <= n; p++)
          if ($urandom_range(2, 0) == 0) begin
            want++;
            for (int j = p; j < p + k; j++) a[j] = ~a[j];
          end
      end else begin
        foreach (a[i]) a[i] = $urandom_range(1, 0);
        want = min_flips_naive(a, k);
      end
      row($sformatf("random %0d", r), a, k, want);
    end
    // random grids, fixable by construction or not
    for (int r = 0; r < 1500; r++) begin
      R = $urandom_range(10, 1); C = $urandom_range(10, 1);
      k = $urandom_range(R < C ? R : C, 1);
      g = new[R];
      foreach (g[i]) begin g[i] = new[C]; foreach (g[i][j]) g[i][j] = 1; end
      want = 0;
      for (int pr = 0; pr + k <= R; pr++)
        for (int pc = 0; pc + k <= C; pc++)
          if ($urandom_range(2, 0) == 0) begin
            want++;
            for (int i = pr; i < pr + k; i++) for (int j = pc; j < pc + k; j++) g[i][j] = ~g[i][j];
          end
      if (r % 3 == 2) begin                       // one cell flipped: compared with the naive scan
        g[$urandom_range(R - 1, 0)][$urandom_range(C - 1, 0)] ^= 1;
        want = min_flips_2d_naive(g, k);
      end
      grid($sformatf("grid %0d", r), g, k, want);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
