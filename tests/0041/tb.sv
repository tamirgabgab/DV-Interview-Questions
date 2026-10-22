// Question 0041: the page's functions against each other and against the page's numbers:
// n H_n for 16 and 100 bins, the chain's 95 % quantiles (90, 754) and median (51), the
// chain against the alternating inclusion-exclusion sum for small n, the integral against
// the k = 1 closed form and against n H_n for equal bins, and the simulation mean within
// the statistical error of the integral for several (p, k).
module tb;
  //@page function automatic real expected_uniform
  //@page function automatic real poisson_at_least

  int errors = 0;

  function automatic real harmonic_expect(int n);
    real h = 0.0;
    for (int i = 1; i <= n; i++) h += 1.0 / real'(i);
    return real'(n) * h;
  endfunction

  // P(all n bins covered within t tests) by inclusion-exclusion (small n only)
  function automatic real incl_excl(int n, int t);
    real s = 0.0, c;
    for (int j = 0; j <= n; j++) begin
      c = 1.0;
      for (int i = 0; i < j; i++) c = c * real'(n - i) / real'(i + 1);    // C(n, j)
      s += (j % 2 ? -1.0 : 1.0) * c * $pow(real'(n - j) / real'(n), t);
    end
    return s;
  endfunction

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f", what, got, want); end
  endtask

  task automatic sim_case(string what, real p[MAXN], int n, int k, int runs);
    real exact = expected_tests(p, n, k), mean = 0.0, variance = 0.0, x;
    int samples[2000];
    for (int r = 0; r < runs; r++) begin samples[r] = simulate_tests(p, n, k); mean += samples[r]; end
    mean /= runs;
    for (int r = 0; r < runs; r++) begin x = samples[r] - mean; variance += x * x; end
    variance /= runs;
    near(what, mean, exact, 4.0 * $sqrt(variance / runs) + 0.1);
  endtask

  initial begin
    real curve[MAXB];
    real p[MAXN];
    int t95;

    near("expected_uniform(16)", expected_uniform(16), 54.0917, 0.001);
    near("expected_uniform(100)", expected_uniform(100), 518.738, 0.001);
    for (int n = 1; n <= 100; n += 9) near("expected_uniform vs harmonic", expected_uniform(n), harmonic_expect(n), 1e-9);
    if (tests_for(16, 0.95) != 90) begin errors++; $display("tests_for(16, 0.95) = %0d", tests_for(16, 0.95)); end
    if (tests_for(16, 0.5) != 51) begin errors++; $display("tests_for(16, 0.5) = %0d", tests_for(16, 0.5)); end
    if (tests_for(100, 0.95) != 754) begin errors++; $display("tests_for(100, 0.95) = %0d", tests_for(100, 0.95)); end
    cover_curve(16, 120, curve);
    near("curve(16)[54]", curve[54], 0.591, 0.002);
    near("curve(16)[90]", curve[90], 0.95, 0.01);
    if (curve[0] != 0.0 || curve[16] <= 0.0 || curve[120] >= 1.0) begin errors++; $display("curve(16) shape wrong"); end
    for (int n = 1; n <= 8; n++) begin
      cover_curve(n, 60, curve);
      for (int t = 0; t <= 60; t++) near("chain vs inclusion-exclusion", curve[t], incl_excl(n, t), 1e-9);
    end

    // the integral: equal bins give n H_n, and the k = 1 closed form
    for (int n = 1; n <= 8; n++) begin
      foreach (p[i]) p[i] = (i < n) ? 1.0 / real'(n) : 0.0;
      near("integral vs n H_n", expected_tests(p, n, 1), expected_uniform(n), 0.02);
      near("closed form vs n H_n", expected_k1(p, n), expected_uniform(n), 1e-9);
    end
    foreach (p[i]) p[i] = 0.0;
    p[0] = 0.1; p[1] = 0.2; p[2] = 0.3; p[3] = 0.4;
    near("integral 0.1..0.4", expected_tests(p, 4, 1), 12.3611, 0.02);
    near("closed form 0.1..0.4", expected_k1(p, 4), 12.3611, 0.001);
    near("integral 0.1..0.4, k = 3", expected_tests(p, 4, 3), 32.16, 0.05);
    foreach (p[i]) p[i] = (i == 0) ? 0.01 : (i < 16 ? 0.99 / 15.0 : 0.0);
    near("rare bin", expected_tests(p, 16, 1), 111.79, 0.05);

    // the simulation against the integral
    void'($urandom(41));
    foreach (p[i]) p[i] = (i < 4) ? 0.25 : 0.0;
    sim_case("4 equal, k = 1", p, 4, 1, 2000);
    sim_case("4 equal, k = 2", p, 4, 2, 2000);
    foreach (p[i]) p[i] = 0.0;
    p[0] = 0.1; p[1] = 0.2; p[2] = 0.3; p[3] = 0.4;
    sim_case("0.1..0.4, k = 1", p, 4, 1, 2000);
    sim_case("0.1..0.4, k = 3", p, 4, 3, 2000);
    foreach (p[i]) p[i] = (i < 16) ? 1.0 / 16.0 : 0.0;
    sim_case("16 equal, k = 1", p, 16, 1, 2000);

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
