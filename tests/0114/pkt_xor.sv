// Question 0114: the DUT the page describes (pkt_xor), run by tests/0114/test_0114.py.
module pkt_xor (
  input  logic       clk, rst_n,
  input  logic       cfg_valid, cfg_addr,  // a register write; addr 0: CTRL (bit 0 = enable), 1: KEY
  input  logic [7:0] cfg_data,
  input  logic       in_valid, in_last,    // a packet: one byte a cycle, in_last on its last byte
  input  logic [7:0] in_data,
  output logic       out_valid, out_last,
  output logic [7:0] out_data,
  output logic [7:0] drops                 // packets dropped because the block was disabled
);
  logic       enable, mid, keep;
  logic [7:0] key;
  wire        pass = mid ? keep : enable;   // the first byte decides for the whole packet

  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) begin
      {enable, mid, keep, key, out_valid, out_last, out_data, drops} <= '0;
    end else begin
      if (cfg_valid) begin
        if (cfg_addr) key    <= cfg_data;
        else          enable <= cfg_data[0];
      end
      out_valid <= in_valid && pass;
      out_last  <= in_last;
      out_data  <= in_data ^ key;
      if (in_valid) begin
        mid  <= !in_last;
        keep <= pass;
        if (!mid && !enable) drops <= drops + 1;
      end
    end
endmodule
