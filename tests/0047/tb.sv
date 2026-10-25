// Question 0047: the page's trap and trap_2d against direct computations: the column
// formula (the highest wall to the left and to the right) on the page's rows, the edge
// cases and 3,000 random rows; the escape height by relaxation (no heap) on the page's
// map, the edge cases and 2,000 random maps up to 7 x 7.
module tb;
  //@page Part a: two pointers
  //@page Part b: a cell of the boundary

  int errors = 0;

  function automatic int columns(int h[]);
    int total = 0, lm, rm;
    foreach (h[i]) begin
      lm = 0; rm = 0;
      for (int k = 0; k <= i; k++) if (h[k] > lm) lm = h[k];
      for (int k = i; k < h.size(); k++) if (h[k] > rm) rm = h[k];
      total += (lm < rm ? lm : rm) - h[i];
    end
    return total;
  endfunction

  function automatic int relax(int h[][]);
    int m = h.size(), n, e[][], total = 0, v, lo;
    bit changed = 1;
    if (m == 0 || h[0].size() == 0) return 0;
    n = h[0].size();
    e = new[m];
    foreach (e[i]) begin
      e[i] = new[n];
      foreach (e[i][j]) e[i][j] = (i == 0 || i == m - 1 || j == 0 || j == n - 1) ? h[i][j] : 1 << 30;
    end
    while (changed) begin
      changed = 0;
      for (int i = 1; i < m - 1; i++)
        for (int j = 1; j < n - 1; j++) begin
          lo = e[i + 1][j];
          if (e[i - 1][j] < lo) lo = e[i - 1][j];
          if (e[i][j + 1] < lo) lo = e[i][j + 1];
          if (e[i][j - 1] < lo) lo = e[i][j - 1];
          v = h[i][j] > lo ? h[i][j] : lo;
          if (v < e[i][j]) begin e[i][j] = v; changed = 1; end
        end
    end
    foreach (h[i, j]) total += e[i][j] - h[i][j];
    return total;
  endfunction

  task automatic expect_eq(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: got %0d, want %0d", what, got, want); end
  endtask

  initial begin
    int h[], g[][], m, n, top;
    void'($urandom(47));
    h = '{3, 0, 2, 0, 4};
    expect_eq("row example", trap(h), 7);
    h = '{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
    expect_eq("leetcode row", trap(h), 6);
    h = new[0];
    expect_eq("empty row", trap(h), 0);
    h = '{5};
    expect_eq("one column", trap(h), 0);
    g = new[5];
    g[0] = '{3, 3, 3, 3, 3}; g[1] = '{3, 1, 1, 1, 3}; g[2] = '{3, 1, 5, 1, 3}; g[3] = '{3, 1, 1, 1, 2}; g[4] = '{3, 3, 3, 3, 3};
    expect_eq("map example", trap_2d(g), 8);
    g = new[3];
    g[0] = '{1, 4, 3, 1, 3, 2}; g[1] = '{3, 2, 1, 3, 2, 4}; g[2] = '{2, 3, 3, 2, 3, 1};
    expect_eq("leetcode map", trap_2d(g), 4);
    g = new[0];
    expect_eq("empty map", trap_2d(g), 0);
    for (int t = 0; t < 3000; t++) begin
      top = $urandom_range(0, 2) == 0 ? 3 : 50;
      h = new[$urandom_range(1, 30)];
      foreach (h[i]) h[i] = $urandom_range(0, top);
      expect_eq("random row", trap(h), columns(h));
    end
    for (int t = 0; t < 2000; t++) begin
      top = $urandom_range(0, 1) ? 2 : 9;
      m = $urandom_range(1, 7); n = $urandom_range(1, 7);
      g = new[m];
      foreach (g[i]) begin
        g[i] = new[n];
        foreach (g[i][j]) g[i][j] = $urandom_range(0, top);
      end
      expect_eq("random map", trap_2d(g), relax(g));
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
