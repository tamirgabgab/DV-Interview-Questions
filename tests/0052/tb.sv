// Question 0052: the page's prob, corr, expected_tosses, race and wait_dist on the page's
// numbers (6, 4, 14; a biased coin; the die; the races of two and three patterns; the
// distribution of HH as F(t-1) / 2^t), and a simulation with $urandom: the mean number of
// tosses and the share of races won within a few standard errors of the page.
module tb;
  //@page function automatic real prob
  //@page function automatic real race
  //@page function automatic void wait_dist

  int errors = 0;
  real fair[byte], biased[byte], die[byte];

  task automatic near(string what, real got, real want, real tol = 1e-9);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f", what, got, want); end
  endtask

  function automatic byte toss(real p[byte]);
    real u = real'($urandom) / 4294967296.0, acc = 0.0;
    byte last;
    foreach (p[c]) begin acc += p[c]; last = c; if (u < acc) return c; end
    return last;
  endfunction

  // tosses until w appears, and 1 when a appears before b
  function automatic int wait_for(string w, real p[byte]);
    string seen = "";
    int n = 0;
    while (1) begin
      seen = {seen, string'(toss(p))};
      if (seen.len() > w.len()) seen = seen.substr(1, seen.len() - 1);
      n++;
      if (seen == w) return n;
    end
  endfunction

  function automatic int first(string a, string b, real p[byte]);
    string seen = "";
    int keep = a.len() > b.len() ? a.len() : b.len();
    while (1) begin
      seen = {seen, string'(toss(p))};
      if (seen.len() > keep) seen = seen.substr(1, seen.len() - 1);
      if (seen.len() >= a.len() && seen.substr(seen.len() - a.len(), seen.len() - 1) == a) return 1;
      if (seen.len() >= b.len() && seen.substr(seen.len() - b.len(), seen.len() - 1) == b) return 0;
    end
  endfunction

  task automatic check_mean(string w, real p[byte], int runs);
    real sum = 0.0, sq = 0.0, m, sd, e = expected_tosses(w, p);
    int t;
    for (int r = 0; r < runs; r++) begin t = wait_for(w, p); sum += t; sq += real'(t) * t; end
    m = sum / runs; sd = $sqrt(sq / runs - m * m);
    near({"simulated mean of ", w}, m, e, 4.0 * sd / $sqrt(runs));
  endtask

  task automatic check_race(string a, string b, int runs);
    string pats[$] = '{a, b};
    real win[$];
    int wins = 0;
    real len = race(pats, fair, win), share;
    for (int r = 0; r < runs; r++) wins += first(a, b, fair);
    share = real'(wins) / runs;
    near({"simulated race ", a, " vs ", b}, share, win[0], 4.0 * $sqrt(win[0] * (1 - win[0]) / runs));
  endtask

  initial begin
    string pats[$];
    real win[$], g[$], len, fib[$];
    fair["H"] = 0.5; fair["T"] = 0.5;
    biased["H"] = 2.0 / 3.0; biased["T"] = 1.0 / 3.0;
    for (int i = 1; i <= 6; i++) die[8'h30 + i] = 1.0 / 6.0;
    void'($urandom(52));
    near("E[HH]", expected_tosses("HH", fair), 6);
    near("E[HT]", expected_tosses("HT", fair), 4);
    near("E[HHH]", expected_tosses("HHH", fair), 14);
    near("E[HH], q = 2/3", expected_tosses("HH", biased), 15.0 / 4.0);
    near("E[TT], q = 2/3", expected_tosses("TT", biased), 12);
    near("E[66], die", expected_tosses("66", die), 42);
    near("E[12], die", expected_tosses("12", die), 36);
    pats = '{"HT", "HH"};
    len = race(pats, fair, win);
    near("HT vs HH", win[0], 0.5); near("HT vs HH length", len, 3);
    pats = '{"THH", "HHH"};
    len = race(pats, fair, win);
    near("THH vs HHH", win[0], 7.0 / 8.0);
    pats = '{"HHH", "HTH", "THH"};
    len = race(pats, fair, win);
    near("three: HHH", win[0], 1.0 / 8.0); near("three: HTH", win[1], 5.0 / 12.0);
    near("three: THH", win[2], 11.0 / 24.0); near("three: length", len, 16.0 / 3.0);
    // HH: P(T = t) = F(t - 1) / 2^t
    wait_dist("HH", fair, 30, g);
    fib = '{0.0, 1.0};
    for (int t = 2; t < 30; t++) fib.push_back(fib[t - 1] + fib[t - 2]);
    for (int t = 2; t < 30; t++) near($sformatf("P(T = %0d) for HH", t), g[t], fib[t - 1] / (2.0 ** t), 1e-12);
    near("P(T = 0), P(T = 1)", g[0] + g[1], 0.0);
    // HT: P(T = t) = (t - 1) / 2^t
    wait_dist("HT", fair, 30, g);
    for (int t = 2; t < 30; t++) near($sformatf("P(T = %0d) for HT", t), g[t], (t - 1) / (2.0 ** t), 1e-12);
    check_mean("HH", fair, 20000);
    check_mean("HTH", fair, 20000);
    check_mean("HH", biased, 20000);
    check_race("HT", "HH", 20000);
    check_race("THH", "HHH", 20000);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
