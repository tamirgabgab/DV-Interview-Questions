// Question 0079: the page's coin_c, fair_bit, biased_bit and die_roll. fair_bit gives ones
// at a rate of 1/2 for coins of p = 0.1, 0.3, 0.5 and 0.8, with 1/(p(1-p)) flips per bit;
// biased_bit gives 1 at a rate of p for p = 1/3, 5/8, 1/sqrt(2) and 0.2, with 2 flips on
// average (2 - 2^(1-k) for a p of k binary digits), and exactly 1 flip for p = 1/2; die_roll
// gives each face 1/6 of the time with 4/(p(1-p)) flips per roll. Every rate is checked within
// four standard errors.
module tb;
  //@page class coin_c;
  //@page function automatic bit biased_bit
  //@page function automatic int die_roll

  int errors = 0;

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f (+- %f)", what, got, want, tol); end
  endtask

  task automatic check_fair(real p, int runs);
    coin_c c = new(p);
    int ones = 0;
    real s = 2.0 * p * (1.0 - p);
    for (int r = 0; r < runs; r++) ones += fair_bit(c);
    near($sformatf("fair_bit share of ones, p = %0.2f", p), real'(ones) / runs, 0.5, 4.0 * $sqrt(0.25 / runs));
    near($sformatf("fair_bit flips per bit, p = %0.2f", p), real'(c.flips) / runs, 1.0 / (p * (1.0 - p)),
         4.0 * $sqrt(4.0 * (1.0 - s) / (s * s) / runs));
  endtask

  task automatic check_biased(real p, real mean, int runs);
    coin_c fair = new(0.5);
    int ones = 0;
    for (int r = 0; r < runs; r++) ones += biased_bit(p, fair);
    near($sformatf("biased_bit share of ones, p = %f", p), real'(ones) / runs, p, 4.0 * $sqrt(p * (1.0 - p) / runs));
    near($sformatf("biased_bit flips, p = %f", p), real'(fair.flips) / runs, mean, 4.0 * $sqrt(2.0 / runs));
  endtask

  initial begin
    coin_c c, fair;
    int faces[7];
    int v, runs;
    void'($urandom(79));
    check_fair(0.1, 20000);
    check_fair(0.3, 20000);
    check_fair(0.5, 20000);
    check_fair(0.8, 20000);
    check_biased(1.0 / 3.0, 2.0, 20000);
    check_biased(0.625, 1.75, 20000);
    check_biased(1.0 / $sqrt(2.0), 2.0, 20000);
    check_biased(0.2, 2.0, 20000);
    // p = 1/2 is 0.1 in binary: one flip decides, always
    fair = new(0.5);
    for (int r = 0; r < 1000; r++) void'(biased_bit(0.5, fair));
    if (fair.flips != 1000) begin errors++; $display("p = 1/2 took %0d flips for 1000 bits", fair.flips); end
    // the smallest double has 1074 binary digits, 1073 zeros and a 1: a coin of only 0s
    // matches the zeros and is decided by the last digit, after 1074 flips (the loop's bound)
    fair = new(0.0);
    v = biased_bit(4.9406564584124654e-324, fair);
    if (v != 1 || fair.flips != 1074) begin errors++; $display("smallest double: got %0d after %0d flips", v, fair.flips); end
    // the die
    runs = 12000;
    c = new(0.3);
    for (int r = 0; r < runs; r++) begin
      v = die_roll(c);
      if (v < 1 || v > 6) begin errors++; $display("die_roll gave %0d", v); end
      else faces[v]++;
    end
    for (int f = 1; f <= 6; f++)
      near($sformatf("die face %0d", f), real'(faces[f]) / runs, 1.0 / 6.0, 4.0 * $sqrt((5.0 / 36.0) / runs));
    near("die flips per roll, p = 0.3", real'(c.flips) / runs, 4.0 / (0.3 * 0.7), 0.6);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
