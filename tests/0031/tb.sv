// Question 0031: the page's bridge_time (Dijkstra over who is across and the torch side)
// against the greedy rule min(t1 + 2 t2 + tn, 2 t1 + t(n-1) + tn), which tests/0031 proves
// equal to brute force, on the page's cases and on random sets; the plan string is replayed
// and must end with everyone across at exactly the returned time.
module tb;
  //@page function automatic int bridge_time

  int errors = 0;

  function automatic int greedy(int n, int times[MAXN]);
    int s[MAXN], tmp, total = 0, m = n;
    for (int i = 0; i < n; i++) s[i] = times[i];
    for (int i = 0; i < n; i++)                       // sort ascending
      for (int j = i + 1; j < n; j++)
        if (s[j] < s[i]) begin tmp = s[i]; s[i] = s[j]; s[j] = tmp; end
    while (m > 3) begin
      total += (s[0] + 2 * s[1] + s[m - 1] < 2 * s[0] + s[m - 2] + s[m - 1]) ? s[0] + 2 * s[1] + s[m - 1] : 2 * s[0] + s[m - 2] + s[m - 1];
      m -= 2;
    end
    if (m == 3) total += s[0] + s[1] + s[2];
    else if (m == 2) total += s[1];
    else if (m == 1) total += s[0];
    return total;
  endfunction

  // Replay "AB> A< ..." from the near bank; -1 when a crossing is illegal or not everyone ends across.
  function automatic int replay(int n, int times[MAXN], string plan);
    int across = 0, side = 0, t = 0, i = 0, mask, cost, who;
    while (i < plan.len()) begin
      mask = 0; cost = 0;
      while (i < plan.len() && plan[i] >= "A" && plan[i] <= "H") begin
        who = plan[i] - "A";
        if (who >= n || ((across >> who) & 1) != side) return -1;     // not on the torch's bank
        mask |= 1 << who;
        if (times[who] > cost) cost = times[who];
        i++;
      end
      if (mask == 0 || $countones(mask) > 2) return -1;
      if (i >= plan.len() || plan[i] != ((side == 0) ? ">" : "<")) return -1;
      i++;
      if (i < plan.len()) begin
        if (plan[i] != " ") return -1;
        i++;
      end
      across ^= mask; side = 1 - side; t += cost;
    end
    return (across == (1 << n) - 1 && side == 1) ? t : -1;
  endfunction

  task automatic check(int n, int times[MAXN], int expected);
    string plan;
    int got = bridge_time(n, times, plan);
    if (got != expected) begin
      errors++;
      $display("n=%0d: got %0d, expected %0d (plan '%s')", n, got, expected, plan);
    end
    if (replay(n, times, plan) != got) begin
      errors++;
      $display("n=%0d: plan '%s' does not replay to %0d", n, plan, got);
    end
  endtask

  initial begin
    int times[MAXN];
    string plan;
    int got;

    times = '{1, 2, 5, 10, 0, 0, 0, 0};
    got = bridge_time(4, times, plan);
    if (got != 17 || !(plan == "AB> A< CD> B< AB>" || plan == "AB> B< CD> A< AB>")) begin
      errors++;
      $display("page example: got %0d, plan '%s'", got, plan);
    end
    times = '{1, 2, 5, 10, 20, 0, 0, 0};  check(5, times, 33);
    times = '{1, 2, 3, 4, 0, 0, 0, 0};    check(4, times, 11);
    times = '{7, 0, 0, 0, 0, 0, 0, 0};    check(1, times, 7);
    times = '{3, 9, 0, 0, 0, 0, 0, 0};    check(2, times, 9);
    times = '{1, 5, 8, 0, 0, 0, 0, 0};    check(3, times, 14);
    times = '{2, 2, 2, 2, 2, 2, 2, 2};    check(8, times, 26);

    void'($urandom(31));
    for (int k = 0; k < 400; k++) begin
      int n = 1 + $urandom % MAXN;
      foreach (times[i]) times[i] = (i < n) ? 1 + $urandom % 30 : 0;
      check(n, times, greedy(n, times));
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
