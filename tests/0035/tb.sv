//@flags --timing
//@page module div3_50
// Question 0035: the module's output measured with $realtime over many periods after the
// counter settles: every period is 3 clock periods, every high time 1.5, and there are
// no extra edges (a glitch would show up as a short period).
module tb;
  logic clk = 0, rst_n = 0, clk_out;
  int errors = 0, periods = 0;
  real t_rise = -1, t_fall = -1, high = 0;
  localparam real T = 10.0;          // clock period

  div3_50 dut (.*);

  always #(T / 2) clk = ~clk;

  always @(posedge clk_out) begin
    if (t_rise >= 0 && rst_n && $realtime > 100) begin
      periods++;
      if ($realtime - t_rise != 3 * T) begin errors++; $display("period %0f at %0t", $realtime - t_rise, $realtime); end
      if (high != 1.5 * T) begin errors++; $display("high time %0f at %0t", high, $realtime); end
    end
    t_rise = $realtime;
  end

  always @(negedge clk_out) begin
    t_fall = $realtime;
    high = t_fall - t_rise;
  end

  initial begin
    repeat (3) @(posedge clk);
    #1 rst_n = 1;
    #3000;
    if (errors == 0 && periods >= 90) $display("PASS periods=%0d", periods);
    else $display("FAIL errors=%0d periods=%0d", errors, periods);
    $finish;
  end
endmodule
