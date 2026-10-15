//@flags --timing
//@page module rise_detect

module tb;
  logic clk = 0, rst_n = 0, sig = 0, pulse;
  logic prev = 0;          // reference model: value of sig at the previous rising edge
  int   errors = 0, pulses = 0, rises = 0;

  rise_detect dut (.*);

  always #5 clk = ~clk;
  always @(posedge clk) prev <= rst_n ? sig : 1'b0;

  initial begin
    repeat (2) @(posedge clk);
    rst_n = 1;
    for (int k = 0; k < 2000; k++) begin
      @(negedge clk) sig = 1'($urandom_range(0, 1));
      #1;
      if (pulse !== (sig & ~prev)) errors++;
      if (sig && !prev) rises++;
      if (pulse) pulses++;
    end
    if (errors == 0 && pulses == rises && rises > 0) $display("PASS rises=%0d", rises);
    else $display("FAIL errors=%0d pulses=%0d rises=%0d", errors, pulses, rises);
    $finish;
  end
endmodule
