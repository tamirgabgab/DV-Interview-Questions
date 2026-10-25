// Question 0046: the page's largest_square, largest_rectangle and largest_triangle against
// a brute force on the page's examples, the edge cases and 3,000 random grids up to 8 x 8:
// the area is the largest, the corners hold a shape of ones of that area (a square in part
// a, a right triangle with equal legs in part c), and a grid without a 1 gives area 0 and
// corners -1.
module tb;
  //@page typedef struct { int area
  //@page function automatic int min3
  //@page Part b: every row as a histogram
  //@page Part c: a pass for each direction

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

  // the triangle with its right angle at (r, c), leg k, the legs going dv rows and dh columns
  function automatic bit tri_ones(bit g[][], int r, int c, int k, int dv, int dh);
    for (int a = 0; a < k; a++)
      for (int b = 0; a + b < k; b++) begin
        int rr = r + dv * a, cc = c + dh * b;
        if (rr < 0 || rr >= g.size() || cc < 0 || cc >= g[0].size() || !g[rr][cc]) return 0;
      end
    return 1;
  endfunction

  function automatic int brute_tri(bit g[][]);
    int best = 0;
    foreach (g[r, c])
      for (int dv = -1; dv <= 1; dv += 2)
        for (int dh = -1; dh <= 1; dh += 2)
          for (int k = 1; k <= g.size() && k <= g[0].size(); k++)
            if (tri_ones(g, r, c, k, dv, dh) && k * (k + 1) / 2 > best) best = k * (k + 1) / 2;
    return best;
  endfunction

  task automatic check_tri(bit g[][], tri_t t);
    int want = brute_tri(g), k;
    if (t.area != want) begin errors++; $display("triangle: area %0d, want %0d", t.area, want); return; end
    if (want == 0) begin
      if (t.r0 != -1 || t.c0 != -1 || t.r1 != -1 || t.c1 != -1 || t.r2 != -1 || t.c2 != -1) begin
        errors++; $display("triangle: vertices for no shape");
      end
      return;
    end
    k = (t.r1 > t.r0 ? t.r1 - t.r0 : t.r0 - t.r1) + 1;
    if (t.c1 != t.c0 || t.r2 != t.r0 || (t.c2 > t.c0 ? t.c2 - t.c0 : t.c0 - t.c2) + 1 != k || k * (k + 1) / 2 != t.area ||
        !tri_ones(g, t.r0, t.c0, k, t.r1 >= t.r0 ? 1 : -1, t.c2 >= t.c0 ? 1 : -1)) begin
      errors++; $display("triangle: bad vertices (%0d, %0d) (%0d, %0d) (%0d, %0d) for area %0d", t.r0, t.c0, t.r1, t.c1, t.r2, t.c2, t.area);
    end
  endtask

  task automatic expect_tri(string what, tri_t t, int area, int r0, int c0, int r1, int c1, int r2, int c2);
    if (t.area != area || t.r0 != r0 || t.c0 != c0 || t.r1 != r1 || t.c1 != c1 || t.r2 != r2 || t.c2 != c2) begin
      errors++; $display("%s: got %0d (%0d, %0d) (%0d, %0d) (%0d, %0d)", what, t.area, t.r0, t.c0, t.r1, t.c1, t.r2, t.c2);
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
    expect_tri("row triangle", largest_triangle(g), 1, 0, 0, 0, 0, 0, 0);
    g = new[0];
    expect_tri("empty triangle", largest_triangle(g), 0, -1, -1, -1, -1, -1, -1);
    g = new[3];
    g[0] = '{1, 0, 0}; g[1] = '{1, 1, 0}; g[2] = '{1, 1, 1};
    expect_tri("left triangle", largest_triangle(g), 6, 2, 0, 0, 0, 2, 2);
    g[0] = '{0, 0, 1}; g[1] = '{0, 1, 1}; g[2] = '{1, 1, 1};
    expect_tri("right triangle", largest_triangle(g), 6, 2, 2, 0, 2, 2, 0);
    g = new[2];
    g[0] = '{0, 1, 0}; g[1] = '{1, 1, 1};
    expect_tri("pyramid", largest_triangle(g), 3, 1, 1, 0, 1, 1, 0);
    g = new[5];
    g[0] = '{1, 0, 0, 0, 0, 0, 1}; g[1] = '{1, 1, 0, 0, 0, 1, 1}; g[2] = '{1, 1, 1, 0, 1, 1, 1};
    g[3] = '{1, 1, 1, 1, 0, 1, 0}; g[4] = '{0, 1, 0, 1, 1, 1, 1};
    expect_tri("triangle example", largest_triangle(g), 10, 3, 0, 0, 0, 3, 3);
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
      check_tri(g, largest_triangle(g));
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
