//@flags --timing
//@page module div3_50
//@page module div_odd_50
// Question 0035: part a's div3_50 and part b's div_odd_50 for N = 3, 5 and 7, measured with
// $realtime over many periods after the counters settle: every period is N clock periods,
// every high time N / 2, and there are no extra edges (a glitch would show up as a short
// period).
module measure #(parameter int N = 3, parameter real T = 10.0) (input logic rst_n, input logic sig);
  int errors = 0, periods = 0;
  real t_rise = -1, high = 0;
  always @(posedge sig) begin
    if (t_rise >= 0 && rst_n && $realtime > 300) begin
      periods++;
      if ($realtime - t_rise != N * T) begin errors++; $display("N=%0d period %0f at %0t", N, $realtime - t_rise, $realtime); end
      if (high != N * T / 2) begin errors++; $display("N=%0d high time %0f at %0t", N, high, $realtime); end
    end
    t_rise = $realtime;
  end
  always @(negedge sig) high = $realtime - t_rise;
endmodule

module tb;
  logic clk = 0, rst_n = 0, out3, o3, o5, o7;
  localparam real T = 10.0;          // clock period

  div3_50 dut (.clk, .rst_n, .clk_out(out3));
  div_odd_50 #(.N(3)) d3 (.clk, .rst_n, .clk_out(o3));
  div_odd_50 #(.N(5)) d5 (.clk, .rst_n, .clk_out(o5));
  div_odd_50 #(.N(7)) d7 (.clk, .rst_n, .clk_out(o7));
  measure #(.N(3)) m (.rst_n, .sig(out3));
  measure #(.N(3)) m3 (.rst_n, .sig(o3));
  measure #(.N(5)) m5 (.rst_n, .sig(o5));
  measure #(.N(7)) m7 (.rst_n, .sig(o7));

  always #(T / 2) clk = ~clk;

  initial begin
    int errors, mismatch = 0;
    repeat (3) @(posedge clk);
    #1 rst_n = 1;
    repeat (600) begin
      @(clk);
      #1 if (o3 !== out3) mismatch++;
    end
    errors = m.errors + m3.errors + m5.errors + m7.errors + mismatch;
    if (errors == 0 && m.periods >= 90 && m5.periods >= 50 && m7.periods >= 35)
      $display("PASS periods=%0d/%0d/%0d", m.periods, m5.periods, m7.periods);
    else $display("FAIL errors=%0d mismatch=%0d periods=%0d/%0d/%0d", errors, mismatch, m.periods, m5.periods, m7.periods);
    $finish;
  end
endmodule
