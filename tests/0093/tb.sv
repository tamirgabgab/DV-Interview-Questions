// Question 0093: the page's SystemVerilog. gale_shapley on the example (both sides proposing),
// count_stable on the example; on random instances of 2 to 6, the result is a stable perfect
// matching within n^2 - n + 1 proposals, and no stable matching (all of them, by next_perm and
// is_stable) gives any proposer a better partner or any receiver a worse one; the instances
// that need exactly n^2 - n + 1 proposals.
module tb;
  //@page function automatic int gale_shapley
  //@page function automatic int count_stable

  int errors = 0;

  // a row of digits, best first: "615324" -> 5 0 4 2 1 3 (jobs), "ECBAFD" -> 4 2 1 0 5 3
  function automatic void row(ref prefs_t p, input int x, input string s, input bit letters);
    for (int k = 0; k < s.len(); k++) p[x][k] = letters ? int'(s[k]) - 65 : int'(s[k]) - 49;
  endfunction

  function automatic void shuffle_rows(int n, ref prefs_t p);
    int r, t;
    for (int x = 0; x < n; x++) begin
      for (int k = 0; k < n; k++) p[x][k] = k;
      for (int k = n - 1; k > 0; k--) begin
        r = $urandom_range(k, 0);
        t = p[x][k];
        p[x][k] = p[x][r];
        p[x][r] = t;
      end
    end
  endfunction

  initial begin
    prefs_t C, J, P, Q;
    match_t m, mj, s;
    int props, n, want[8], a, b;

    row(C, 0, "615324", 0); row(C, 1, "142356", 0); row(C, 2, "213645", 0);
    row(C, 3, "365241", 0); row(C, 4, "341562", 0); row(C, 5, "136425", 0);
    row(J, 0, "ECBAFD", 1); row(J, 1, "ABFDEC", 1); row(J, 2, "AFCDEB", 1);
    row(J, 3, "ADCEFB", 1); row(J, 4, "DCEFAB", 1); row(J, 5, "FCDAEB", 1);

    props = gale_shapley(6, C, J, m);
    want = '{4, 0, 1, 5, 3, 2, 0, 0};
    for (int i = 0; i < 6; i++) if (m[i] != want[i]) begin errors++; $display("example: candidate %0d got %0d", i, m[i]); end
    if (props != 11) begin errors++; $display("example: %0d proposals", props); end
    if (!is_stable(6, C, J, m)) begin errors++; $display("example: not stable"); end
    props = gale_shapley(6, J, C, mj);
    want = '{4, 1, 0, 2, 3, 5, 0, 0};           // job j's candidate: E B A C D F
    for (int j = 0; j < 6; j++) if (mj[j] != want[j]) begin errors++; $display("jobs propose: job %0d got %0d", j, mj[j]); end
    if (props != 9) begin errors++; $display("jobs propose: %0d proposals", props); end
    if (count_stable(6, C, J) != 5) begin errors++; $display("example: %0d stable", count_stable(6, C, J)); end

    // random instances: stable, within the bound, best for proposers and worst for receivers
    void'($urandom(93));
    for (int t = 0; t < 120; t++) begin
      n = 2 + t % 5;
      shuffle_rows(n, P);
      shuffle_rows(n, Q);
      props = gale_shapley(n, P, Q, m);
      if (!is_stable(n, P, Q, m) || props > n * n - n + 1) begin errors++; $display("random %0d: stable %0d, %0d proposals", t, is_stable(n, P, Q, m), props); end
      for (int x = 0; x < n; x++) s[x] = x;
      do begin
        if (is_stable(n, P, Q, s))
          for (int i = 0; i < n; i++) begin
            a = -1;
            b = -1;
            for (int k = 0; k < n; k++) begin
              if (P[i][k] == m[i]) a = k;
              if (P[i][k] == s[i]) b = k;
            end
            if (b < a) begin errors++; $display("random %0d: proposer %0d does better in another stable matching", t, i); end
            for (int k = 0; k < n; k++) begin
              if (Q[m[i]][k] == i) a = k;
            end
            for (int x = 0; x < n; x++)
              if (s[x] == m[i])
                for (int k = 0; k < n; k++) if (Q[m[i]][k] == x) b = k;
            if (b > a) begin errors++; $display("random %0d: receiver %0d does worse in another stable matching", t, m[i]); end
          end
      end while (next_perm(n, s));
    end

    // the instances that need n^2 - n + 1 proposals
    for (n = 2; n <= 8; n++) begin
      for (int i = 0; i < n; i++) begin
        for (int k = 0; k < n - 1; k++) P[i][k] = (i + k) % (n - 1);
        P[i][n - 1] = n - 1;
      end
      for (int j = 0; j < n; j++) begin
        if (j == n - 1) begin
          for (int k = 0; k < n; k++) Q[j][k] = k;
          continue;
        end
        Q[j][0] = (j + 1) % (n - 1);
        Q[j][1] = n - 1;
        for (int k = 1; k < n - 1; k++) Q[j][k + 1] = (j + 1 + k) % (n - 1);
      end
      props = gale_shapley(n, P, Q, m);
      if (props != n * n - n + 1) begin errors++; $display("worst case %0d: %0d proposals", n, props); end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
