// Question 0046: the page's largest_square and largest_rectangle against a brute force on
// the page's two examples, the edge cases and 3,000 random grids up to 8 x 8: the area is
// the largest, the corners hold a shape of ones of that area (a square in part a), and a
// grid without a 1 gives area 0 and corners -1.
module tb;
  //@page typedef struct { int area
  //@page function automatic int min3
  //@page Part b: every row as a histogram

  int errors = 0;

  function automatic bit ones(bit g[][], int r1, int c1, int r2, int c2);
    for (int r = r1; r <= r2; r++)
      for (int c = c1; c <= c2; c++)
        if (!g[r][c]) return 0;
    return 1;
  endfunction

  function automatic int brute(bit g[][], bit sq);
    int best = 0, m = g.size(), n = g[0].size();
    for (int r1 = 0; r1 < m; r1++)
      for (int r2 = r1; r2 < m; r2++)
        for (int c1 = 0; c1 < n; c1++)
          for (int c2 = c1; c2 < n; c2++)
            if ((!sq || r2 - r1 == c2 - c1) && ones(g, r1, c1, r2, c2) && (r2 - r1 + 1) * (c2 - c1 + 1) > best)
              best = (r2 - r1 + 1) * (c2 - c1 + 1);
    return best;
  endfunction

  task automatic check(string what, bit g[][], bit sq, shape_t s);
    int want = brute(g, sq);
    if (s.area != want) begin errors++; $display("%s: area %0d, want %0d", what, s.area, want); return; end
    if (want == 0) begin
      if (s.r1 != -1 || s.c1 != -1 || s.r2 != -1 || s.c2 != -1) begin errors++; $display("%s: corners for no shape", what); end
      return;
    end
    if ((s.r2 - s.r1 + 1) * (s.c2 - s.c1 + 1) != s.area || !ones(g, s.r1, s.c1, s.r2, s.c2) || (sq && s.r2 - s.r1 != s.c2 - s.c1)) begin
      errors++; $display("%s: bad corners (%0d, %0d) (%0d, %0d) for area %0d", what, s.r1, s.c1, s.r2, s.c2, s.area);
    end
  endtask

  task automatic expect_shape(string what, shape_t s, int area, int r1, int c1, int r2, int c2);
    if (s.area != area || s.r1 != r1 || s.c1 != c1 || s.r2 != r2 || s.c2 != c2) begin
      errors++; $display("%s: got %0d (%0d, %0d) (%0d, %0d)", what, s.area, s.r1, s.c1, s.r2, s.c2);
    end
  endtask

  initial begin
    bit g[][];
    int m, n;
    void'($urandom(46));
    g = new[4];
    g[0] = '{1, 0, 1, 1, 1}; g[1] = '{1, 1, 1, 1, 1}; g[2] = '{0, 1, 1, 1, 1}; g[3] = '{1, 1, 1, 1, 0};
    expect_shape("square example", largest_square(g), 9, 0, 2, 2, 4);
    g = new[3];
    g[0] = '{1, 1, 1, 1, 0}; g[1] = '{1, 1, 1, 1, 1}; g[2] = '{0, 1, 1, 0, 1};
    expect_shape("rectangle example", largest_rectangle(g), 8, 0, 0, 1, 3);
    expect_shape("its square", largest_square(g), 4, 0, 0, 1, 1);
    g = new[0];
    expect_shape("empty square", largest_square(g), 0, -1, -1, -1, -1);
    expect_shape("empty rectangle", largest_rectangle(g), 0, -1, -1, -1, -1);
    g = new[1]; g[0] = '{1, 1, 1};
    expect_shape("row square", largest_square(g), 1, 0, 0, 0, 0);
    expect_shape("row rectangle", largest_rectangle(g), 3, 0, 0, 0, 2);
    for (int t = 0; t < 3000; t++) begin
      int p = $urandom_range(30, 100);
      m = $urandom_range(1, 8); n = $urandom_range(1, 8);
      g = new[m];
      foreach (g[i]) begin
        g[i] = new[n];
        foreach (g[i][j]) g[i][j] = $urandom_range(1, 100) <= p;
      end
      check("square", g, 1, largest_square(g));
      check("rectangle", g, 0, largest_rectangle(g));
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
