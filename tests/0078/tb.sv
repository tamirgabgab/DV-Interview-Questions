// Question 0078: the page's SystemVerilog: rand7 over 70000 draws (every output near 10000),
// calls_needed and expected_calls against the page's numbers (50/21, 24/5, 64/15, 9/4) and
// against k M^k / L for many (M, N, k), rand_n's outputs uniform and its mean calls near the
// expectation, and exact_calls against a brute force (n | m^k) and the page's examples.
module tb;
  //@page function automatic int rand7
  //@page function automatic int rand_n
  //@page function automatic int exact_calls

  int errors = 0;

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f", what, got, want); end
  endtask

  task automatic same(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: got %0d, expected %0d", what, got, want); end
  endtask

  // brute force: the fewest k <= 40 with n | m^k, 0 when none
  function automatic int brute(int m, int n);
    longint p = 1;
    for (int k = 1; k <= 40; k++) begin
      p = p * m % n;
      if (p == 0) return k;
    end
    return 0;
  endfunction

  // rand_n(m, n, k) many times: every output within 5 sigma of draws / n
  task automatic uniform(int m, int n, int k, int draws);
    int count[64];
    real want = real'(draws) / real'(n), sigma = $sqrt(want);
    foreach (count[i]) count[i] = 0;
    for (int i = 0; i < draws; i++) begin
      int r = rand_n(m, n, k);
      if (r < 1 || r > n) begin errors++; $display("rand_n(%0d, %0d) = %0d out of range", m, n, r); return; end
      count[r]++;
    end
    for (int r = 1; r <= n; r++) near($sformatf("rand_n(%0d, %0d, %0d) count of %0d", m, n, k, r), count[r], want, 5.0 * sigma);
  endtask

  // in the initial block every variable is declared here and assigned in the loops: an
  // initialiser inside a loop of an initial block is static and runs once (IEEE 6.21)
  initial begin
    int count[8];
    int r, k0;
    longint below, size;
    real e;
    void'($urandom(78));

    // rand7
    foreach (count[i]) count[i] = 0;
    for (int i = 0; i < 70000; i++) begin
      r = rand7();
      if (r < 1 || r > 7) begin errors++; $display("rand7 = %0d", r); end
      else count[r]++;
    end
    for (int r = 1; r <= 7; r++) near($sformatf("rand7 count of %0d", r), count[r], 10000.0, 450.0);

    // the page's numbers
    same("calls_needed(5, 7)", calls_needed(5, 7), 2);
    same("calls_needed(2, 40)", calls_needed(2, 40), 6);
    same("calls_needed(7, 5)", calls_needed(7, 5), 1);
    near("expected_calls(5, 7)", expected_calls(5, 7), 50.0 / 21.0, 1e-12);
    near("expected_calls(2, 5, 3)", expected_calls(2, 5, 3), 24.0 / 5.0, 1e-12);
    near("expected_calls(2, 5, 4)", expected_calls(2, 5, 4), 64.0 / 15.0, 1e-12);
    near("expected_calls(6, 8)", expected_calls(6, 8), 9.0 / 4.0, 1e-12);
    near("expected_calls(7, 5)", expected_calls(7, 5), 7.0 / 5.0, 1e-12);
    near("expected_calls(20, 10)", expected_calls(20, 10), 1.0, 1e-12);

    // the expectation against k M^k / L and the bound 2k
    for (int m = 2; m <= 10; m++)
      for (int n = 2; n <= 40; n++) begin
        k0 = calls_needed(m, n);
        below = 1;
        repeat (k0 - 1) below *= m;
        if (below * m < n || (k0 > 1 && below >= n)) begin errors++; $display("calls_needed(%0d, %0d) = %0d", m, n, k0); end
        for (int k = k0; k <= k0 + 2; k++) begin
          size = 1;
          repeat (k) size *= m;
          e = expected_calls(m, n, k);
          near($sformatf("expected_calls(%0d, %0d, %0d)", m, n, k), e, real'(k) * real'(size) / real'(size - size % n), 1e-9);
          if (e >= 2.0 * k) begin errors++; $display("expected_calls(%0d, %0d, %0d) = %f is not below 2k", m, n, k, e); end
        end
      end

    // rand_n: uniform, and its mean calls near the expectation (counted by the draws of a fixed seed)
    uniform(5, 7, 0, 21000);
    uniform(2, 5, 4, 20000);
    uniform(6, 8, 0, 16000);
    uniform(7, 10, 0, 20000);
    uniform(10, 40, 3, 40000);

    // exact_calls
    for (int m = 2; m <= 20; m++)
      for (int n = 2; n <= 60; n++) same($sformatf("exact_calls(%0d, %0d)", m, n), exact_calls(m, n), brute(m, n));
    same("exact_calls(5, 7)", exact_calls(5, 7), 0);
    same("exact_calls(6, 8)", exact_calls(6, 8), 3);
    same("exact_calls(6, 9)", exact_calls(6, 9), 2);
    same("exact_calls(2, 6)", exact_calls(2, 6), 0);
    same("exact_calls(20, 10)", exact_calls(20, 10), 1);
    same("exact_calls(10, 4)", exact_calls(10, 4), 2);

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
