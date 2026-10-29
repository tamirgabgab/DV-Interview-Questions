// Question 0069: the page's Fenwick tree, passed, passed_merge, overtook, inversions,
// disorder, arrival_order and live_overtakes on the page's example, the self-checks,
// fixed arrays whose answers were computed by the page's Python (written here), and
// random arrays with and without ties against an O(n^2) count of every pair.
module tb;
  //@page class Fenwick
  //@page function automatic idxq_t sort_count
  //@page function automatic void overtook
  //@page function automatic int inversions

  int errors = 0;

  function automatic void brute(input int done[], output int p[], output int o[]);
    int n = done.size();
    p = new[n]; o = new[n];
    for (int i = 0; i < n; i++) begin
      p[i] = 0; o[i] = 0;
      for (int j = i + 1; j < n; j++) if (done[j] < done[i]) p[i]++;
      for (int j = 0; j < i; j++) if (done[j] > done[i]) o[i]++;
    end
  endfunction

  function automatic bit same(int a[], int b[]);
    if (a.size() != b.size()) return 0;
    foreach (a[i]) if (a[i] != b[i]) return 0;
    return 1;
  endfunction

  function automatic void check(string name, input int done[], input int want_p[], input int want_o[]);
    int p[], pm[], o[], order[$], live[$], total = 0, inv;
    passed(done, p);
    passed_merge(done, pm);
    overtook(done, o);
    inv = inversions(done);
    arrival_order(done, order);
    live_overtakes(order, done.size(), live);
    if (!same(p, want_p)) begin errors++; $display("%s: passed %p, expected %p", name, p, want_p); end
    if (!same(pm, want_p)) begin errors++; $display("%s: passed_merge %p, expected %p", name, pm, want_p); end
    if (!same(o, want_o)) begin errors++; $display("%s: overtook %p, expected %p", name, o, want_o); end
    foreach (want_p[i]) total += want_p[i];
    if (inv != total) begin errors++; $display("%s: inversions %0d, expected %0d", name, inv, total); end
    total = 0;
    foreach (want_o[i]) total += want_o[i];
    if (inv != total) begin errors++; $display("%s: sum of overtook %0d differs", name, total); end
    if (live.size() != done.size()) begin errors++; $display("%s: live size", name); end
    foreach (order[k]) begin
      if (live[k] != want_p[order[k]]) begin errors++; $display("%s: live[%0d] = %0d, passed[%0d] = %0d", name, k, live[k], order[k], want_p[order[k]]); end
      if (k > 0 && done[order[k - 1]] > done[order[k]]) begin errors++; $display("%s: arrival order", name); end
      if (k > 0 && done[order[k - 1]] == done[order[k]] && order[k - 1] > order[k]) begin errors++; $display("%s: ties out of send order", name); end
    end
    if (done.size() >= 2) begin
      real d = disorder(done);
      real want = real'(inv) / (done.size() * (done.size() - 1) / 2);
      if (d < want - 1e-9 || d > want + 1e-9) begin errors++; $display("%s: disorder %f, expected %f", name, d, want); end
    end else if (disorder(done) != 0.0) begin errors++; $display("%s: disorder of a short array", name); end
  endfunction

  initial begin
    int done[], p[], o[];
    Fenwick ft;
    // the Fenwick tree itself: the example of the idea on 8 cells
    ft = new(8);
    ft.add(3);
    if (ft.tree[3] != 1 || ft.tree[4] != 1 || ft.tree[8] != 1 || ft.tree[1] != 0 || ft.tree[2] != 0) begin errors++; $display("add(3)"); end
    ft.add(5); ft.add(7);
    if (ft.prefix(7) != 3 || ft.prefix(4) != 1 || ft.prefix(2) != 0 || ft.prefix(8) != 3 || ft.prefix(0) != 0) begin errors++; $display("prefix"); end
    if ((12 & -12) != 4 || (6 & -6) != 2 || (8 & -8) != 8 || (7 & -7) != 1) begin errors++; $display("lowest set bit"); end
    // the page's example and the self-checks
    done = '{5, 2, 6, 1};
    check("example", done, '{2, 1, 1, 0}, '{0, 1, 0, 3});
    if (inversions(done) != 4) begin errors++; $display("example: inversions"); end
    done = '{7, 3, 9, 2, 8};
    check("self-check", done, '{2, 1, 2, 0, 0}, '{0, 1, 0, 3, 1});
    if (inversions(done) != 5) begin errors++; $display("self-check: inversions"); end
    // answers written by the page's Python (tests/0069/test_0069_code.py checks the same code)
    done = '{5, 5, 5};
    check("all equal", done, '{0, 0, 0}, '{0, 0, 0});
    done = '{9, 8, 7, 6, 5, 4};
    check("reversed", done, '{5, 4, 3, 2, 1, 0}, '{0, 1, 2, 3, 4, 5});
    if (disorder(done) != 1.0) begin errors++; $display("reversed: disorder"); end
    done = '{1, 2, 3, 4};
    check("in order", done, '{0, 0, 0, 0}, '{0, 0, 0, 0});
    if (disorder(done) != 0.0) begin errors++; $display("in order: disorder"); end
    done = '{12, 7, 7, 30, 1, 7, 12};
    check("ties", done, '{4, 1, 1, 3, 0, 0, 0}, '{0, 1, 1, 0, 4, 2, 1});
    done = '{1000000, 3, 1000000, 999999, 3};
    check("large times", done, '{3, 0, 2, 1, 0}, '{0, 1, 0, 2, 3});
    done = new[0];
    check("empty", done, done, done);
    done = '{42};
    check("one", done, '{0}, '{0});
    // random arrays: distinct-ish, many ties, long
    for (int r = 0; r < 3000; r++) begin
      int n = $urandom_range(0, r < 2000 ? 14 : 60);
      done = new[n];
      foreach (done[i]) done[i] = (r % 3 == 0) ? $urandom_range(0, 3) : (r % 3 == 1) ? $urandom_range(0, 99) : $urandom_range(0, 1000000);
      brute(done, p, o);
      check($sformatf("run %0d", r), done, p, o);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
