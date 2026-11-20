// Question 0115: what the page leaves out of its SystemVerilog bench. tests/0115/variants.py
// writes tb.sv from this file and the page's blocks: the DUT once, then every bench as the
// module below with the page's code at the line "// the page's code", under its own name.
// The page's bench forks the monitor first; a variant may swap the two lines of the fork.
// The benches do not call $finish: tb ends the run once every bench has done its cycles.

// ---- the DUT
module add1 (
  input  logic       clk,
  input  logic       in_valid,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic [7:0] out_data
);
  always_ff @(posedge clk) begin
    out_valid <= in_valid;
    out_data  <= in_data + 8'd1;
  end
endmodule

// ---- the bench
module race_tb;
  localparam int N = 10;
  logic       clk = 0, in_valid = 0, out_valid;
  logic [7:0] in_data = 0, out_data;
  int         cycle = 0, mismatches = 0;
  string      cycles = "";                 // the cycle of every mismatch, for tb

  add1 dut (.*);
  always #5 clk = ~clk;
  always @(mismatches) if (mismatches) cycles = cycles == "" ? $sformatf("%0d", cycle) : $sformatf("%s %0d", cycles, cycle);

  function automatic string item(logic valid, logic [7:0] data);
    return valid ? $sformatf("%0d", data) : "none";
  endfunction

  // the page's code

  initial begin
    fork
      monitor();
      drive();
    join_any
    repeat (3) @(posedge clk);
    $display("%m: %0d mismatches", mismatches);
  end
endmodule
