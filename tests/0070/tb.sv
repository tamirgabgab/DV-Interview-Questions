// Question 0070: the page's shortest_path, shortest_with_breaks and cheapest_path against
// brute-force searches written here (a BFS over every state (cell, breaks left) with one
// visit per state and no pruning, and costs relaxed over every move until nothing changes)
// on the page's examples, the self-checks, the trap of part b and 2,000 random grids up to
// 6 x 6 with both neighbourhoods; the path of part a is checked step by step.
module tb;
  //@page typedef struct { int r, c; } cell_t;
  //@page function automatic int shortest_with_breaks
  //@page function automatic int cheapest_path

  int errors = 0;

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // a move of the page's rules: inside, one step in a direction of the table, not a
  // diagonal between two walls
  function automatic bit is_move(string grid[], cell_t u, cell_t v, bit diag, byte wall);
    int dr = v.r - u.r, dc = v.c - u.c;
    if (v.r < 0 || v.r >= grid.size() || v.c < 0 || v.c >= grid[0].len()) return 0;
    if (dr < -1 || dr > 1 || dc < -1 || dc > 1 || (dr == 0 && dc == 0)) return 0;
    if (dr != 0 && dc != 0 && (!diag || (grid[u.r].getc(v.c) == wall && grid[v.r].getc(u.c) == wall))) return 0;
    return 1;
  endfunction

  // BFS over every state (cell, breaks left), each visited once
  function automatic int brute_breaks(string grid[], cell_t s, cell_t t, int k, bit diag);
    int m = grid.size(), n = grid[0].len(), seen[string];
    int qr[$], qc[$], ql[$], qd[$], r, c, l, d, rest;
    cell_t u, v;
    qr.push_back(s.r); qc.push_back(s.c); ql.push_back(k); qd.push_back(0);
    seen[$sformatf("%0d,%0d,%0d", s.r, s.c, k)] = 1;
    while (qr.size() > 0) begin
      r = qr.pop_front(); c = qc.pop_front(); l = ql.pop_front(); d = qd.pop_front();
      if (r == t.r && c == t.c) return d;
      for (int dr = -1; dr <= 1; dr++)
        for (int dc = -1; dc <= 1; dc++) begin
          u = '{r, c}; v = '{r + dr, c + dc};
          if (!is_move(grid, u, v, diag, "1")) continue;
          rest = l - (grid[v.r].getc(v.c) == "1");
          if (rest < 0 || seen.exists($sformatf("%0d,%0d,%0d", v.r, v.c, rest))) continue;
          seen[$sformatf("%0d,%0d,%0d", v.r, v.c, rest)] = 1;
          qr.push_back(v.r); qc.push_back(v.c); ql.push_back(rest); qd.push_back(d + 1);
        end
    end
    return -1;
  endfunction

  // the least entry cost, every move relaxed until nothing changes
  function automatic int brute_cost(string grid[], cell_t s, cell_t t, bit diag);
    int m = grid.size(), n = grid[0].len(), best[][], changed;
    cell_t u, v;
    best = new[m];
    foreach (best[i]) begin best[i] = new[n]; foreach (best[i][j]) best[i][j] = -1; end
    best[s.r][s.c] = 0;
    do begin
      changed = 0;
      for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++) begin
          if (best[r][c] < 0) continue;
          for (int dr = -1; dr <= 1; dr++)
            for (int dc = -1; dc <= 1; dc++) begin
              int w;
              u = '{r, c}; v = '{r + dr, c + dc};
              if (!is_move(grid, u, v, diag, "#") || grid[v.r].getc(v.c) == "#") continue;
              w = grid[v.r].getc(v.c) - "0";
              if (best[v.r][v.c] < 0 || best[r][c] + w < best[v.r][v.c]) begin best[v.r][v.c] = best[r][c] + w; changed = 1; end
            end
        end
    end while (changed);
    return best[t.r][t.c];
  endfunction

  // shortest_path: the length against the brute force with k = 0, and the path walked
  function automatic void check_path(string what, string grid[], cell_t s, cell_t t, bit diag, int want);
    cell_t path[$];
    int d = shortest_path(grid, s, t, diag, path);
    check(what, d, want);
    if (d < 0) begin
      if (path.size() != 0) begin errors++; $display("%s: a path without a length", what); end
      return;
    end
    if (path.size() != d + 1 || path[0].r != s.r || path[0].c != s.c || path[d].r != t.r || path[d].c != t.c) begin errors++; $display("%s: the path does not run from s to t", what); return; end
    for (int i = 0; i + 1 < path.size(); i++)
      if (!is_move(grid, path[i], path[i + 1], diag, "1") || grid[path[i + 1].r].getc(path[i + 1].c) != "0") begin
        errors++; $display("%s: step %0d is not a move", what, i); return;
      end
  endfunction

  function automatic void random_grid(output string grid[], input int m, int n, int pct, bit costs);
    grid = new[m];
    foreach (grid[i]) begin
      grid[i] = "";
      for (int j = 0; j < n; j++) begin
        bit w = $urandom_range(0, 99) < pct;
        if (costs) grid[i] = {grid[i], w ? "#" : $sformatf("%0d", $urandom_range(1, 9))};
        else grid[i] = {grid[i], w ? "1" : "0"};
      end
    end
  endfunction

  initial begin
    string g[], c3[], sc[], ce[];
    cell_t s, t;
    int m, n;
    // the page's example: 20 and 15; the answers for k = 0..5 and the eight-direction ones
    g = '{"001010000", "001001010", "001010010", "001001010", "001010010", "001001010", "000000010"};
    check_path("example a", g, '{3, 0}, '{3, 8}, 0, 20);
    check_path("example a, diagonals", g, '{3, 0}, '{3, 8}, 1, 15);
    for (int k = 0; k <= 5; k++) check($sformatf("example b, k = %0d", k), shortest_with_breaks(g, '{3, 0}, '{3, 8}, k, 0), k == 0 ? 20 : k < 3 ? 14 : 8);
    check("example b, k = 1, diagonals", shortest_with_breaks(g, '{3, 0}, '{3, 8}, 1, 1), 9);
    // the trap of part b and the terrain of part c
    ce = '{"001", "101", "010"};
    check("trap of part b", shortest_with_breaks(ce, '{0, 0}, '{2, 2}, 1, 0), 4);
    c3 = '{"1111111", "1559551", "1599951", "1599951", "1559551", "1115111"};
    check("example c", cheapest_path(c3, '{2, 0}, '{3, 6}, 0), 11);
    check("example c, diagonals", cheapest_path(c3, '{2, 0}, '{3, 6}, 1), 9);
    // the self-checks
    sc = '{"0000", "1110", "0000", "0111"};
    check_path("self-check a", sc, '{3, 0}, '{0, 0}, 0, 9);
    check("self-check b", shortest_with_breaks(sc, '{3, 0}, '{0, 0}, 1, 0), 3);
    sc = '{"191", "151", "111"};
    check("self-check c", cheapest_path(sc, '{0, 0}, '{0, 2}, 0), 6);
    // edge cases
    sc = '{"010", "111", "000"};
    check_path("walled in", sc, '{0, 0}, '{2, 2}, 0, -1);
    sc = '{"000"};
    check_path("start is the target", sc, '{0, 1}, '{0, 1}, 0, 0);
    // random grids
    for (int r = 0; r < 2000; r++) begin
      m = $urandom_range(1, 6); n = $urandom_range(1, 6);
      random_grid(g, m, n, $urandom_range(10, 45), 0);
      s = '{$urandom_range(0, m - 1), $urandom_range(0, n - 1)};
      t = '{$urandom_range(0, m - 1), $urandom_range(0, n - 1)};
      g[s.r] = {g[s.r].substr(0, s.c - 1), "0", g[s.r].substr(s.c + 1, n - 1)};
      g[t.r] = {g[t.r].substr(0, t.c - 1), "0", g[t.r].substr(t.c + 1, n - 1)};
      for (int diag = 0; diag < 2; diag++) begin
        check_path($sformatf("run %0d a diag %0d", r, diag), g, s, t, diag, brute_breaks(g, s, t, 0, diag));
        for (int k = 0; k < 4; k++)
          check($sformatf("run %0d b k %0d diag %0d", r, k, diag), shortest_with_breaks(g, s, t, k, diag), brute_breaks(g, s, t, k, diag));
      end
      random_grid(c3, m, n, 15, 1);
      c3[s.r] = {c3[s.r].substr(0, s.c - 1), "1", c3[s.r].substr(s.c + 1, n - 1)};
      c3[t.r] = {c3[t.r].substr(0, t.c - 1), "1", c3[t.r].substr(t.c + 1, n - 1)};
      for (int diag = 0; diag < 2; diag++)
        check($sformatf("run %0d c diag %0d", r, diag), cheapest_path(c3, s, t, diag), brute_cost(c3, s, t, diag));
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
