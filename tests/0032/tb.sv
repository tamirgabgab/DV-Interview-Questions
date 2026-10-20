// Question 0032: testbench. //@page pulls the page's SystemVerilog block that contains
// the given text; the run must print a line starting with PASS.
module tb;
  //@page my_function
  initial begin
    $display("PASS");
    $finish;
  end
endmodule
