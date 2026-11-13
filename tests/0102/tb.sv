// Question 0102: the page's topo_kahn, topo_dfs and critical_path on the page's examples,
// the edge cases (no edges, a self loop, two components, duplicate edges, a long chain) and
// random graphs: an order is checked by its property (every task once, a before b for every
// edge), a cycle against the transitive closure (Warshall) and edge by edge, and the critical
// path against the heaviest path by repeated relaxation.
module tb;
  //@page function automatic bit topo_kahn
  //@page function automatic bit topo_dfs
  //@page function automatic int critical_path

  int errors = 0;

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // every task once, and a before b for every edge
  function automatic bit valid(int n, int edges[][2], int order[$]);
    int pos[];
    pos = new[n];
    foreach (pos[i]) pos[i] = -1;
    if (order.size() != n) return 0;
    foreach (order[i]) begin
      if (order[i] < 0 || order[i] >= n || pos[order[i]] >= 0) return 0;
      pos[order[i]] = i;
    end
    foreach (edges[i]) if (pos[edges[i][0]] >= pos[edges[i][1]]) return 0;
    return 1;
  endfunction

  // the transitive closure: a task that reaches itself
  function automatic bit has_cycle(int n, int edges[][2]);
    bit r[][];
    r = new[n];
    foreach (r[i]) r[i] = new[n];
    foreach (edges[i]) r[edges[i][0]][edges[i][1]] = 1;
    for (int k = 0; k < n; k++)
      for (int i = 0; i < n; i++)
        if (r[i][k]) for (int j = 0; j < n; j++) if (r[k][j]) r[i][j] = 1;
    for (int v = 0; v < n; v++) if (r[v][v]) return 1;
    return 0;
  endfunction

  // an edge from every task of the cycle to the next, and from the last to the first
  function automatic bit is_cycle(int n, int edges[][2], int cyc[$]);
    bit seen[];
    bit found;
    seen = new[n];
    if (cyc.size() == 0) return 0;
    foreach (cyc[i]) begin
      if (seen[cyc[i]]) return 0;
      seen[cyc[i]] = 1;
      found = 0;
      foreach (edges[j]) if (edges[j][0] == cyc[i] && edges[j][1] == cyc[(i + 1) % cyc.size()]) found = 1;
      if (!found) return 0;
    end
    return 1;
  endfunction

  // the heaviest path of a graph without a cycle: n rounds of relaxation over every edge
  function automatic int heaviest(int n, int edges[][2], int dur[]);
    int fin[], best = 0;
    fin = new[n];
    foreach (fin[v]) fin[v] = dur[v];
    for (int r = 0; r < n; r++)
      foreach (edges[i]) if (fin[edges[i][0]] + dur[edges[i][1]] > fin[edges[i][1]])
        fin[edges[i][1]] = fin[edges[i][0]] + dur[edges[i][1]];
    foreach (fin[v]) if (fin[v] > best) best = fin[v];
    return best;
  endfunction

  function automatic string letters(int q[$]);
    string s = "";
    foreach (q[i]) s = {s, string'(8'd65 + q[i])};
    return s;
  endfunction

  initial begin
    int e[][2], dur[], d2[], order[$], cyc[$], start[], slack[], s2[], sl2[];
    int want_start[7], want_slack[7];
    int n, m, u, v, total, ok;
    string got;
    // the page's example: Kahn A E B C D F G, DFS E A C B D F G
    e = '{'{0, 1}, '{0, 2}, '{4, 2}, '{1, 3}, '{2, 3}, '{3, 5}, '{5, 6}};
    dur = '{3, 2, 4, 1, 5, 1, 4};
    check("example kahn", topo_kahn(7, e, order), 1);
    got = letters(order);
    if (got != "AEBCDFG") begin errors++; $display("example kahn order %s", got); end
    check("example dfs", topo_dfs(7, e, order, cyc), 1);
    got = letters(order);
    if (got != "EACBDFG") begin errors++; $display("example dfs order %s", got); end
    // part c: 15, the starts 0 3 5 9 0 10 11, the slack 2 4 0 0 0 0 0
    check("example total", critical_path(7, e, dur, start, slack), 15);
    want_start = '{0, 3, 5, 9, 0, 10, 11};
    want_slack = '{2, 4, 0, 0, 0, 0, 0};
    foreach (start[i]) check($sformatf("example start %0d", i), start[i], want_start[i]);
    foreach (slack[i]) check($sformatf("example slack %0d", i), slack[i], want_slack[i]);
    // A takes 6: the total moves to 16 and E gets a slack of 1
    d2 = '{6, 2, 4, 1, 5, 1, 4};
    check("A takes 6", critical_path(7, e, d2, start, slack), 16);
    check("A takes 6, slack of A", slack[0], 0);
    check("A takes 6, slack of E", slack[4], 1);
    // the cycle: D -> E; Kahn gives out A and B, DFS finds D E C
    e = '{'{0, 1}, '{0, 2}, '{4, 2}, '{1, 3}, '{2, 3}, '{3, 5}, '{5, 6}, '{3, 4}};
    check("cycle kahn", topo_kahn(7, e, order), 0);
    got = letters(order);
    if (got != "AB") begin errors++; $display("cycle kahn ran %s", got); end
    check("cycle dfs", topo_dfs(7, e, order, cyc), 0);
    got = letters(cyc);
    if (got != "DEC") begin errors++; $display("cycle dfs %s", got); end
    check("cycle part c", critical_path(7, e, dur, start, slack), -1);
    // no edges, a self loop, two components, duplicate edges
    e = new[0];
    check("no edges", topo_kahn(4, e, order), 1);
    check("no edges, in index order", letters(order) == "ABCD", 1);
    e = '{'{0, 1}, '{1, 1}, '{1, 2}};
    check("self loop kahn", topo_kahn(3, e, order), 0);
    check("self loop dfs", topo_dfs(3, e, order, cyc), 0);
    check("self loop is the cycle", letters(cyc) == "B", 1);
    e = '{'{0, 1}, '{1, 2}, '{3, 4}};
    check("two components", topo_kahn(5, e, order), 1);
    check("two components, order", letters(order) == "ADBEC", 1);
    e = '{'{0, 1}, '{0, 1}, '{1, 2}, '{1, 2}, '{1, 2}};
    check("duplicates kahn", topo_kahn(3, e, order) && valid(3, e, order), 1);
    check("duplicates dfs", topo_dfs(3, e, order, cyc) && valid(3, e, order), 1);
    // a chain of 5000 tasks, and the same closed into one cycle
    e = new[4999];
    foreach (e[i]) e[i] = '{i, i + 1};
    check("chain dfs", topo_dfs(5000, e, order, cyc) && valid(5000, e, order), 1);
    e = new[5000](e);
    e[4999] = '{4999, 0};
    check("ring dfs", topo_dfs(5000, e, order, cyc), 0);
    check("ring cycle", cyc.size(), 5000);
    // random graphs: anything, with self loops and duplicates
    for (int r = 0; r < 3000; r++) begin
      n = $urandom_range(1, 8);
      m = $urandom_range(0, 2 * n + 2);
      e = new[m];
      dur = new[n];
      foreach (dur[i]) dur[i] = $urandom_range(0, 9);
      for (int i = 0; i < m; i++) begin
        u = $urandom_range(0, n - 1); v = $urandom_range(0, n - 1);
        // half of the runs keep only edges that go up in index order: no cycle
        if (r % 2 == 0 && u >= v) begin
          if (u == v) v = (u + 1) % n;
          if (u > v) begin int t = u; u = v; v = t; end
          if (u == v) u = -1;
        end
        if (u < 0) begin u = 0; v = 0; end
        e[i] = '{u, v};
      end
      if (r % 2 == 0) begin
        // drop the self loops a one-task run may have made
        int k = 0;
        int f[][2];
        f = new[m];
        foreach (e[i]) if (e[i][0] != e[i][1]) begin f[k] = e[i]; k++; end
        e = new[k](f);
      end
      ok = topo_kahn(n, e, order);
      check($sformatf("run %0d kahn", r), ok, !has_cycle(n, e));
      if (ok) check($sformatf("run %0d kahn valid", r), valid(n, e, order), 1);
      ok = topo_dfs(n, e, order, cyc);
      check($sformatf("run %0d dfs", r), ok, !has_cycle(n, e));
      if (ok) check($sformatf("run %0d dfs valid", r), valid(n, e, order), 1);
      else check($sformatf("run %0d dfs cycle", r), is_cycle(n, e, cyc), 1);
      total = critical_path(n, e, dur, start, slack);
      if (!ok) check($sformatf("run %0d part c on a cycle", r), total, -1);
      else begin
        check($sformatf("run %0d total", r), total, heaviest(n, e, dur));
        foreach (e[i]) if (start[e[i][1]] < start[e[i][0]] + dur[e[i][0]]) begin
          errors++; $display("run %0d: edge %0d starts too early", r, i);
        end
        // a task late by its slack keeps the total; one more minute moves it
        for (int t = 0; t < n; t++) begin
          if (slack[t] < 0) begin errors++; $display("run %0d: negative slack", r); end
          d2 = new[n](dur);
          d2[t] += slack[t];
          check($sformatf("run %0d slack of %0d", r, t), critical_path(n, e, d2, s2, sl2), total);
          d2[t] += 1;
          check($sformatf("run %0d slack of %0d plus one", r, t), critical_path(n, e, d2, s2, sl2), total + 1);
        end
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
