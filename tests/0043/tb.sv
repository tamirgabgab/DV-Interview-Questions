// Question 0043: the page's horses_plan on hidden speeds: the ranking it returns is the
// true top c (checked against the speeds), every race is in finishing order, the group
// races and the winners' race come first, the race count matches the page (9 for 36 / 6 / 4,
// 7 for 30 / 6 / 3, 7 for 25 / 5 / 3, 6 for 25 / 5 / 1) over seeded shuffles, and for
// 36 / 6 / 4 the eighth race is always the six candidates with the most missing comparisons.
module tb;
  //@page function automatic void hr_beats

  int errors = 0;
  int seed = 43;

  function automatic int lcg();                 // a small deterministic generator for the shuffles
    seed = (seed * 1103515245 + 12345) & 32'h7fffffff;
    return seed;
  endfunction

  task automatic shuffle(int a, output int speed[MAXA]);
    for (int i = 0; i < MAXA; i++) speed[i] = i;
    for (int i = a - 1; i > 0; i--) begin
      int j = lcg() % (i + 1), t = speed[i];
      speed[i] = speed[j]; speed[j] = t;
    end
  endtask

  // the true rank of horse x (1 = fastest)
  function automatic int true_rank(int a, int x, int speed[MAXA]);
    int r = 1;
    for (int y = 0; y < a; y++) if (speed[y] < speed[x]) r++;
    return r;
  endfunction

  task automatic check_case(string what, int a, int b, int c, int want_races, int trials);
    int speed[MAXA], ranking[MAXB], races[MAXR][MAXB], sizes[MAXR], n, groups, worst = 0;
    for (int t = 0; t < trials; t++) begin
      shuffle(a, speed);
      n = horses_plan(a, b, c, speed, ranking, races, sizes);
      if (n > worst) worst = n;
      for (int r = 0; r < c; r++)
        if (true_rank(a, ranking[r], speed) != r + 1) begin errors++; $display("%s: rank %0d is horse %0d of true rank %0d", what, r + 1, ranking[r], true_rank(a, ranking[r], speed)); end
      groups = (a + b - 1) / b;
      for (int r = 0; r < n; r++) begin
        if (sizes[r] < 1 || sizes[r] > b) begin errors++; $display("%s: race %0d has %0d horses", what, r, sizes[r]); end
        for (int i = 0; i + 1 < sizes[r]; i++)
          if (speed[races[r][i]] > speed[races[r][i + 1]]) begin errors++; $display("%s: race %0d not in finishing order", what, r); end
      end
      for (int k = 0; k < groups; k++)
        if (sizes[k] != ((a - k * b < b) ? a - k * b : b)) begin errors++; $display("%s: group race %0d has %0d horses", what, k, sizes[k]); end
      if (groups > 1 && sizes[groups] != groups) begin errors++; $display("%s: the winners' race has %0d horses", what, sizes[groups]); end
      if (a == 36 && b == 6 && c == 4 && n >= 8) begin           // the eighth race: A2, B1, A3, B2, C1, D1 in the winners' order
        int w[MAXB], ok = 1, found;
        int want[6];
        for (int k = 0; k < 6; k++) w[k] = races[6][k];           // the winners in finishing order
        want[0] = races[w[0] / b][1]; want[1] = w[1]; want[2] = races[w[0] / b][2]; want[3] = races[w[1] / b][1]; want[4] = w[2]; want[5] = w[3];
        if (sizes[7] != 6) ok = 0;
        for (int i = 0; i < 6; i++) begin
          found = 0;
          for (int k = 0; k < 6; k++) if (races[7][k] == want[i]) found = 1;
          if (!found) ok = 0;
        end
        if (!ok) begin errors++; $display("%s: race 8 is not the six staircase candidates", what); end
      end
    end
    if (worst != want_races) begin errors++; $display("%s: worst case %0d races, expected %0d", what, worst, want_races); end
  endtask

  initial begin
    check_case("36 / 6 / 4", 36, 6, 4, 9, 40);
    check_case("30 / 6 / 3", 30, 6, 3, 7, 40);
    check_case("25 / 5 / 3", 25, 5, 3, 7, 40);
    check_case("25 / 5 / 1", 25, 5, 1, 6, 20);
    check_case("16 / 4 / 3", 16, 4, 3, 7, 40);
    check_case("9 / 3 / 2", 9, 3, 2, 5, 20);
    check_case("64 / 8 / 4", 64, 8, 4, 10, 20);
    check_case("6 / 6 / 2", 6, 6, 2, 1, 5);
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
