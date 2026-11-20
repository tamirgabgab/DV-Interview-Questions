//@flags --timing
// Question 0113: the DUT the page describes, module pipe (sim0113.py takes it from this file
// for the page's pyuvm testbench), and a test of it alone. With the page's clock (10 ns, low
// first), reset for two rising edges and items given one per cycle as the page's driver gives
// them, every item comes out LAT = 4 cycles later with its data plus 1: the item taken at the
// rising edge of 25 + 10i ns is on out_valid from 55 + 10i ns and seen at the falling edge of
// 60 + 10i ns, the times tools/figures/q0113.py uses. Then random traffic with gaps, and a
// reset in the middle that empties the pipeline.

module pipe #(parameter int LAT = 4) (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       in_valid,
  input  logic [7:0] in_data,
  output logic       out_valid,
  output logic [7:0] out_data
);
  logic [LAT-1:0] v;              // a valid bit per stage
  logic [7:0]     d [LAT];        // the data of every stage

  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) v <= '0;
    else        v <= {v[LAT-2:0], in_valid};

  always_ff @(posedge clk) begin
    d[0] <= in_data + 8'd1;
    for (int i = 1; i < LAT; i++) d[i] <= d[i-1];
  end

  assign out_valid = v[LAT-1];
  assign out_data  = d[LAT-1];
endmodule

module tb;
  localparam int LAT = 4;
  logic       clk = 0, rst_n = 0, in_valid = 0;
  logic [7:0] in_data = 0;
  logic       out_valid;
  logic [7:0] out_data;
  int         errors = 0, n_out = 0;

  pipe dut (.*);
  always #5 clk = ~clk;

  // the reference: the cycle (rising-edge count) and data of every item taken
  int         edge_no = 0;
  int         taken_at[$];
  logic [7:0] taken_data[$];
  always @(posedge clk) begin
    edge_no++;
    if (rst_n && in_valid) begin
      taken_at.push_back(edge_no);
      taken_data.push_back(in_data);
    end
  end

  // the output, sampled at the falling edge like the page's monitor
  realtime first_seen = -1;
  int         at;
  logic [7:0] d;
  always @(negedge clk) if (out_valid) begin
    if (taken_at.size() == 0) begin
      $display("ERROR: item out at %0t with nothing in", $realtime);
      errors++;
    end else begin
      at = taken_at.pop_front();
      d  = taken_data.pop_front();
      if (edge_no != at + LAT - 1) begin
        $display("ERROR: item taken at edge %0d seen after edge %0d", at, edge_no);
        errors++;
      end
      if (out_data !== 8'(d + 1)) begin
        $display("ERROR: data %0d out as %0d", d, out_data);
        errors++;
      end
      if (first_seen < 0) first_seen = $realtime;
      n_out++;
    end
  end

  initial begin
    repeat (2) @(posedge clk);             // reset for two rising edges, as the page's driver
    rst_n <= 1;
    for (int k = 0; k < 8; k++) begin       // eight items back to back, 0x10 + k
      in_valid <= 1;
      in_data  <= 8'h10 + k;
      @(posedge clk);
    end
    in_valid <= 0;
    repeat (LAT + 1) @(posedge clk);
    if (first_seen != 60) begin
      $display("ERROR: the first item seen at %0t, not 60 ns", first_seen);
      errors++;
    end
    if (n_out != 8) begin
      $display("ERROR: %0d items out of 8", n_out);
      errors++;
    end
    for (int k = 0; k < 2000; k++) begin    // random traffic with gaps
      in_valid <= $urandom_range(0, 2) != 0;
      in_data  <= 8'($urandom);
      @(posedge clk);
    end
    in_valid <= 1;                           // a reset with items inside: they are gone
    repeat (3) @(posedge clk);
    in_valid <= 0;
    @(negedge clk);
    rst_n = 0;
    taken_at.delete();
    taken_data.delete();
    @(posedge clk);
    rst_n <= 1;
    repeat (LAT + 2) @(posedge clk);
    if (out_valid !== 0) begin
      $display("ERROR: out_valid after a reset with an empty pipeline");
      errors++;
    end
    if (errors == 0) $display("PASS: 0113 pipe, latency %0d, %0d items out, data + 1", LAT, n_out);
    else             $display("FAIL: 0113 pipe, %0d errors", errors);
    $finish;
  end
endmodule
