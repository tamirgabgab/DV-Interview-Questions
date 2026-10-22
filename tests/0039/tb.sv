// Question 0039: the page's egg_table / min_drops / egg_run against the binomial sum
// C(t, 1) + ... + C(t, k) (exact in longint while below n), the page's numbers (9 drops,
// the floors 37, 66, 88, 100, the run against threshold 36), and the plan replayed against
// every threshold of several (k, n): never more drops than the worst case, every floor
// inside the unknown range, the outcome as the threshold dictates, and the run ends with
// the threshold settled. The worst case must also be reached by some threshold.
module tb;
  //@page function automatic void egg_table

  int errors = 0;

  // C(t, 1) + ... + C(t, k), capped at cap (the terms grow fast; stop once past the cap)
  function automatic int covered(int k, int t, int cap);
    longint c = 1, sum = 0;
    for (int i = 1; i <= k; i++) begin
      c = c * (t - i + 1) / i;                 // C(t, i) from C(t, i - 1), exact
      sum += c;
      if (sum >= cap) return cap;
      if (c == 0) break;
    end
    return int'(sum);
  endfunction

  function automatic int ref_drops(int k, int n);
    for (int t = 0; t <= n; t++) if (covered(k, t, n) >= n) return t;
    return n;
  endfunction

  task automatic check_pair(int k, int n);
    int floors[MAXN];
    bit broke[MAXN];
    int t = min_drops(k, n), worst = 0, d, low, high, eggs;
    if (t != ref_drops(k, n)) begin errors++; $display("k=%0d n=%0d: min_drops %0d, binomial %0d", k, n, t, ref_drops(k, n)); end
    for (int T = 0; T <= n; T++) begin
      d = egg_run(k, n, T, floors, broke);
      if (d > t) begin errors++; $display("k=%0d n=%0d T=%0d: %0d drops > %0d", k, n, T, d, t); end
      if (d > worst) worst = d;
      low = 0; high = n + 1; eggs = k;
      for (int i = 0; i < d; i++) begin
        if (!(floors[i] > low && floors[i] < high) || eggs < 1) begin errors++; $display("k=%0d n=%0d T=%0d: floor %0d outside (%0d, %0d)", k, n, T, floors[i], low, high); end
        if (broke[i] != (floors[i] > T)) begin errors++; $display("k=%0d n=%0d T=%0d: outcome at floor %0d wrong", k, n, T, floors[i]); end
        if (broke[i]) begin high = floors[i]; eggs--; end
        else low = floors[i];
      end
      if (high != low + 1 || low != T) begin errors++; $display("k=%0d n=%0d T=%0d: ended at low=%0d high=%0d", k, n, T, low, high); end
    end
    if (worst != t) begin errors++; $display("k=%0d n=%0d: worst case %0d reached, expected %0d", k, n, worst, t); end
  endtask

  initial begin
    int floors[MAXN];
    bit broke[MAXN];
    int d;
    int F[MAXK + 1][MAXN + 1];

    if (min_drops(3, 100) != 9) begin errors++; $display("min_drops(3, 100) = %0d", min_drops(3, 100)); end
    if (min_drops(2, 100) != 14) begin errors++; $display("min_drops(2, 100) = %0d", min_drops(2, 100)); end
    egg_table(3, 100, F);
    if (F[3][8] != 92 || F[3][9] != 100 || F[2][8] != 36) begin errors++; $display("table: F[3][8]=%0d F[3][9]=%0d F[2][8]=%0d", F[3][8], F[3][9], F[2][8]); end

    d = egg_run(3, 100, 100, floors, broke);         // the first egg never breaks
    if (d != 4 || floors[0] != 37 || floors[1] != 66 || floors[2] != 88 || floors[3] != 100) begin
      errors++; $display("first egg floors: %0d drops, %0d %0d %0d %0d", d, floors[0], floors[1], floors[2], floors[3]);
    end
    d = egg_run(3, 100, 36, floors, broke);
    if (d != 9 || floors[0] != 37 || !broke[0] || floors[1] != 8 || broke[1] || floors[8] != 36) begin
      errors++; $display("threshold 36: %0d drops, first %0d (%0d), then %0d, last %0d", d, floors[0], broke[0], floors[1], floors[8]);
    end

    check_pair(3, 100);
    check_pair(2, 100);
    check_pair(1, 12);
    check_pair(3, 14);
    check_pair(4, 1000);
    check_pair(10, 1000);
    check_pair(2, 36);
    check_pair(5, 1);
    for (int k = 1; k <= 6; k++)
      for (int n = 1; n <= 40; n++) check_pair(k, n);

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
