// Question 0065: the page's count_islands, count_islands8 and island_sizes against a
// brute force (repeated label propagation: every land cell takes the smallest label among
// itself and its neighbours until nothing changes) on the page's examples, the self-check
// grids, the edge cases and 2,000 random grids up to 8 x 8 with both neighbourhoods.
module tb;
  //@page typedef struct { int r, c; } cell_t;
  //@page function automatic int count_islands8
  //@page function automatic void island_sizes

  int errors = 0;

  // the brute force: labels propagated until stable, then the sizes per label, largest first
  function automatic void brute(string grid[], bit diag, output int sizes[$]);
    int m = grid.size(), n = m > 0 ? grid[0].len() : 0, changed, lab[][], cnt[int];
    lab = new[m];
    foreach (lab[r]) begin
      lab[r] = new[n];
      for (int c = 0; c < n; c++) lab[r][c] = grid[r].getc(c) == "1" ? r * n + c : -1;
    end
    do begin
      changed = 0;
      for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++) begin
          if (lab[r][c] < 0) continue;
          for (int dr = -1; dr <= 1; dr++)
            for (int dc = -1; dc <= 1; dc++) begin
              int a = r + dr, b = c + dc;
              if (dr == 0 && dc == 0) continue;
              if (!diag && dr != 0 && dc != 0) continue;
              if (a < 0 || a >= m || b < 0 || b >= n || lab[a][b] < 0) continue;
              if (lab[a][b] < lab[r][c]) begin lab[r][c] = lab[a][b]; changed = 1; end
            end
        end
    end while (changed);
    sizes = {};
    for (int r = 0; r < m; r++)
      for (int c = 0; c < n; c++)
        if (lab[r][c] >= 0) begin
          if (!cnt.exists(lab[r][c])) cnt[lab[r][c]] = 0;
          cnt[lab[r][c]]++;
        end
    foreach (cnt[k]) sizes.push_back(cnt[k]);
    sizes.rsort();
  endfunction

  task automatic check(string what, string grid[]);
    int want[$], got[$], land = 0;
    foreach (grid[r]) for (int c = 0; c < grid[r].len(); c++) if (grid[r].getc(c) == "1") land++;
    for (int d = 0; d <= 1; d++) begin
      brute(grid, bit'(d), want);
      island_sizes(grid, bit'(d), got);
      if (got != want) begin errors++; $display("%s, diag %0d: sizes %p, want %p", what, d, got, want); end
      if (got.size() != (d ? count_islands8(grid) : count_islands(grid))) begin errors++; $display("%s, diag %0d: count", what, d); end
      if (got.sum() != land) begin errors++; $display("%s, diag %0d: sum %0d, land %0d", what, d, got.sum(), land); end
    end
    if (count_islands8(grid) > count_islands(grid)) begin errors++; $display("%s: corners split an island", what); end
  endtask

  initial begin
    string g[];
    int s[$], want[$], m, n;
    void'($urandom(65));
    g = '{"110000", "110011", "000010", "000100", "000100"};
    if (count_islands(g) != 3) begin errors++; $display("page example: %0d", count_islands(g)); end
    if (count_islands8(g) != 2) begin errors++; $display("page example, eight: %0d", count_islands8(g)); end
    island_sizes(g, 0, s); want = '{4, 3, 2};
    if (s != want) begin errors++; $display("page sizes %p", s); end
    island_sizes(g, 1, s); want = '{5, 4};
    if (s != want) begin errors++; $display("page sizes, eight %p", s); end
    check("page example", g);
    g = '{"101", "010", "101"};
    if (count_islands(g) != 5 || count_islands8(g) != 1) begin errors++; $display("the X"); end
    check("the X", g);
    g = '{"1101", "1001", "0111"};
    island_sizes(g, 0, s); want = '{5, 3};
    if (s != want) begin errors++; $display("self-check c %p", s); end
    g = '{"0001", "0010", "0100", "1000"};
    if (count_islands(g) != 4 || count_islands8(g) != 1) begin errors++; $display("the diagonal line"); end
    g = new[0];
    island_sizes(g, 1, s);
    if (count_islands(g) != 0 || s.size() != 0) begin errors++; $display("empty grid"); end
    g = '{"000", "000"};
    check("all water", g);
    g = '{"111", "111"};
    island_sizes(g, 0, s); want = '{6};
    if (count_islands(g) != 1 || s != want) begin errors++; $display("all land"); end
    g = '{"1011101"};
    island_sizes(g, 0, s); want = '{3, 1, 1};
    if (s != want) begin errors++; $display("one row %p", s); end
    g = '{"10101", "01010", "10101", "01010"};
    if (count_islands(g) != 10 || count_islands8(g) != 1) begin errors++; $display("checkerboard"); end
    for (int r = 0; r < 2000; r++) begin
      int p = $urandom_range(20, 85);
      m = $urandom_range(1, 8); n = $urandom_range(1, 8);
      g = new[m];
      for (int i = 0; i < m; i++) begin
        g[i] = "";
        for (int j = 0; j < n; j++) g[i] = {g[i], ($urandom_range(0, 99) < p ? "1" : "0")};
      end
      check($sformatf("run %0d", r), g);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
