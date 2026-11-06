//@flags --timing
//@page function automatic real p_full
//@page function automatic void by_recurrence
//@page module credit_counter
// Question 0094: the page's p_full, mean_cycles and by_recurrence against the exact values of
// the parts (and each other), and the page's credit_counter driven by Bernoulli returns and
// uses: directed checks (both at once, the walls), then a Monte Carlo of thousands of runs
// from 3 with N = 10 for several lambda1, lambda2, whose share of full runs and mean cycles
// must be within four standard errors of p_full and mean_cycles.
module tb;
  localparam int N = 10;
  logic clk = 0, rst_n = 1, ret = 0, take = 0;
  logic [$clog2(N + 1) - 1:0] start = 3, count;
  logic full, empty;
  int errors = 0;

  credit_counter #(.N(N)) dut (.clk, .rst_n, .start, .ret, .take, .count, .full, .empty);

  always #5 clk = ~clk;

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f (+- %f)", what, got, want, tol); end
  endtask

  // reset the counter to s (asynchronously, between clock edges)
  task automatic load(int s);
    @(negedge clk);
    start = s;
    rst_n = 0;
    #1 rst_n = 1;
  endtask

  // one cycle with the given ret and take; the result is read after the rising edge
  task automatic cycle(bit r, bit t);
    ret = r;
    take = t;
    @(negedge clk);
  endtask

  // one run from 3: Bernoulli(l1) returns and Bernoulli(l2) uses until a wall
  task automatic walk(real l1, real l2, output bit filled, output int cycles);
    load(3);
    cycles = 0;
    while (!full && !empty) begin
      cycle(real'($urandom) / 4294967296.0 < l1, real'($urandom) / 4294967296.0 < l2);
      cycles++;
    end
    filled = full;
  endtask

  task automatic monte_carlo(real l1, real l2, int runs);
    real p = l1 * (1.0 - l2), q = l2 * (1.0 - l1), pf, mc, sum = 0.0, sum2 = 0.0, mean, sd;
    int fills = 0, c;
    bit f;
    pf = p_full(3, N, p, q);
    mc = mean_cycles(3, N, p, q);
    for (int r = 0; r < runs; r++) begin
      walk(l1, l2, f, c);
      fills += f;
      sum += c;
      sum2 += real'(c) * c;
    end
    mean = sum / runs;
    sd = $sqrt((sum2 / runs - mean * mean) / runs);
    near($sformatf("share full, l1 = %0.2f, l2 = %0.2f", l1, l2), real'(fills) / runs, pf, 4.0 * $sqrt(pf * (1.0 - pf) / runs) + 1e-9);
    near($sformatf("mean cycles, l1 = %0.2f, l2 = %0.2f", l1, l2), mean, mc, 4.0 * sd + 1e-9);
  endtask

  initial begin
    real fr, cy;
    void'($urandom(94));
    // the formulas of the parts
    near("part a, P(full)", p_full(3, 10, 0.5, 0.5), 0.3, 1e-12);
    near("part a, mean cycles", mean_cycles(3, 10, 0.5, 0.5), 21.0, 1e-9);
    near("part b, P(full)", p_full(3, 10, 0.6, 0.4), 41553.0 / 58025.0, 1e-12);
    near("part b, mean cycles", mean_cycles(3, 10, 0.6, 0.4), 48291.0 / 2321.0, 1e-9);
    near("part c, P(full)", p_full(3, 10, 0.3, 0.2), 41553.0 / 58025.0, 1e-12);
    near("part c, mean cycles", mean_cycles(3, 10, 0.3, 0.2), 96582.0 / 2321.0, 1e-9);
    near("part d, P(full)", p_full(3, 10, 0.375, 0.125), 28431.0 / 29524.0, 1e-12);
    near("part d, mean cycles", mean_cycles(3, 10, 0.375, 0.125), 195738.0 / 7381.0, 1e-9);
    near("equal rates 1/2", mean_cycles(3, 10, 0.25, 0.25), 42.0, 1e-9);
    near("walls", p_full(0, 10, 0.6, 0.4) + mean_cycles(10, 10, 0.6, 0.4) + mean_cycles(0, 10, 0.6, 0.4), 0.0, 0.0);
    near("never up", p_full(4, 10, 0.0, 0.5), 0.0, 0.0);
    near("never up, cycles", mean_cycles(4, 10, 0.0, 0.5), 8.0, 1e-12);
    // by_recurrence agrees with the closed form
    for (int n = 2; n <= 12; n += 5)
      for (int k = 0; k <= n; k++) begin
        by_recurrence(k, n, 0.3, 0.2, fr, cy);
        near($sformatf("by_recurrence P, n = %0d, k = %0d", n, k), fr, p_full(k, n, 0.3, 0.2), 1e-9);
        near($sformatf("by_recurrence E, n = %0d, k = %0d", n, k), cy, mean_cycles(k, n, 0.3, 0.2), 1e-7);
        by_recurrence(k, n, 0.25, 0.25, fr, cy);
        near($sformatf("by_recurrence fair E, n = %0d, k = %0d", n, k), cy, real'(k) * (n - k) / 0.5, 1e-7);
      end
    // the counter: both at once keeps it, a wall holds it
    load(3);
    cycle(1, 1); if (count != 3) begin errors++; $display("ret and take: %0d", count); end
    cycle(1, 0); if (count != 4) begin errors++; $display("ret: %0d", count); end
    cycle(0, 1); cycle(0, 1); if (count != 2) begin errors++; $display("take twice: %0d", count); end
    cycle(0, 0); if (count != 2) begin errors++; $display("idle: %0d", count); end
    cycle(0, 1); cycle(0, 1);
    if (count != 0 || !empty || full) begin errors++; $display("empty: %0d %0b", count, empty); end
    cycle(1, 0); if (count != 0) begin errors++; $display("left the wall 0: %0d", count); end
    load(9);
    cycle(1, 0); if (count != N || !full) begin errors++; $display("full: %0d", count); end
    cycle(0, 1); if (count != N) begin errors++; $display("left the wall N: %0d", count); end
    // Monte Carlo against the formula
    monte_carlo(0.5, 0.25, 4000);
    monte_carlo(0.5, 0.5, 4000);
    monte_carlo(0.4, 0.5, 4000);
    monte_carlo(0.9, 0.8, 2000);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
