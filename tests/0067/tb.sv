// Question 0067: the page's delay_bfs, delay_dijkstra and delay_directed against the
// least total weight of every simple path (a depth-first walk) on the page's examples,
// the self-checks and random graphs, directed and not; part a against part b with unit
// weights; and the page's answers written in from the Python tests.
module tb;
  //@page function automatic int delay_bfs
  //@page function automatic int delay_dijkstra
  //@page function automatic int delay_directed

  int errors = 0;

  // the least weight of a simple path from k to every node: every path walked
  function automatic void walk(int n, int edges[][3], bit directed, int u, int d, ref int seen[], ref int best[]);
    if (best[u] < 0 || d < best[u]) best[u] = d;
    foreach (edges[i]) begin
      if (edges[i][0] == u && !seen[edges[i][1]]) begin
        seen[edges[i][1]] = 1; walk(n, edges, directed, edges[i][1], d + edges[i][2], seen, best); seen[edges[i][1]] = 0;
      end
      if (!directed && edges[i][1] == u && !seen[edges[i][0]]) begin
        seen[edges[i][0]] = 1; walk(n, edges, directed, edges[i][0], d + edges[i][2], seen, best); seen[edges[i][0]] = 0;
      end
    end
  endfunction

  function automatic int brute(int n, int edges[][3], int k, bit directed);
    int seen[], best[], ans = 0;
    seen = new[n + 1]; best = new[n + 1];
    foreach (best[i]) begin best[i] = -1; seen[i] = 0; end
    seen[k] = 1;
    walk(n, edges, directed, k, 0, seen, best);
    for (int v = 1; v <= n; v++) begin
      if (best[v] < 0) return -1;
      if (best[v] > ans) ans = best[v];
    end
    return ans;
  endfunction

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  initial begin
    int e2[][2], e3[][3], ones[][3], n, m, k, u, v;
    // the page's example: 3 without weights, 6 with, -1 directed (7 without node 6)
    e3 = '{'{1, 2, 1}, '{1, 3, 5}, '{3, 2, 1}, '{3, 4, 2}, '{2, 5, 6}, '{4, 5, 1}, '{6, 5, 1}};
    e2 = '{'{1, 2}, '{1, 3}, '{3, 2}, '{3, 4}, '{2, 5}, '{4, 5}, '{6, 5}};
    check("example a", delay_bfs(6, e2, 1), 3);
    check("example b", delay_dijkstra(6, e3, 1, 0), 6);
    check("example c", delay_directed(6, e3, 1), -1);
    e3 = '{'{1, 2, 1}, '{1, 3, 5}, '{3, 2, 1}, '{3, 4, 2}, '{2, 5, 6}, '{4, 5, 1}};
    check("example c without 6", delay_directed(5, e3, 1), 7);
    // the self-checks
    e2 = '{'{1, 2}, '{2, 3}, '{3, 4}, '{4, 5}, '{5, 6}, '{6, 7}, '{1, 7}, '{2, 6}};
    check("self-check a", delay_bfs(7, e2, 1), 3);
    e3 = '{'{1, 2, 4}, '{1, 3, 1}, '{3, 2, 1}, '{2, 4, 2}, '{3, 4, 5}};
    check("self-check b", delay_dijkstra(4, e3, 1, 0), 4);
    e3 = '{'{1, 2, 4}, '{1, 3, 1}, '{2, 3, 1}, '{2, 4, 2}, '{3, 4, 5}};
    check("self-check c", delay_directed(4, e3, 1), 6);
    // the edges of the cost block
    e2 = new[0]; e3 = new[0];
    check("one node a", delay_bfs(1, e2, 1), 0);
    check("one node b", delay_dijkstra(1, e3, 1, 0), 0);
    e2 = '{'{1, 2}, '{1, 2}, '{2, 2}, '{2, 3}};
    check("double link and self-loop", delay_bfs(3, e2, 1), 2);
    e3 = '{'{1, 2, 4}};
    check("unreachable b", delay_dijkstra(3, e3, 1, 0), -1);
    e3 = '{'{1, 2, 0}};
    check("zero weight", delay_dijkstra(2, e3, 1, 0), 0);
    // random graphs against every path
    for (int r = 0; r < 1500; r++) begin
      n = $urandom_range(1, 7);
      m = $urandom_range(0, 12);
      e3 = new[m]; e2 = new[m]; ones = new[m];
      for (int i = 0; i < m; i++) begin
        u = $urandom_range(1, n); v = $urandom_range(1, n);
        e3[i] = '{u, v, int'($urandom_range(0, 9))};
        e2[i] = '{u, v};
        ones[i] = '{u, v, 1};
      end
      k = $urandom_range(1, n);
      check($sformatf("run %0d bfs", r), delay_bfs(n, e2, k), brute(n, ones, k, 0));
      check($sformatf("run %0d dijkstra", r), delay_dijkstra(n, e3, k, 0), brute(n, e3, k, 0));
      check($sformatf("run %0d directed", r), delay_directed(n, e3, k), brute(n, e3, k, 1));
      check($sformatf("run %0d unit weights", r), delay_dijkstra(n, ones, k, 0), delay_bfs(n, e2, k));
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
