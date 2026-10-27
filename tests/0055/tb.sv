//@flags --timing
// Question 0055: the page's div3_msb, div3_lsb and div_fsm (four parameter sets) clocked
// on random bits and digits; every cycle each div is compared with the value read so far
// kept here as a remainder by the definition (MSB: v = B*v + d; LSB: v += d * B^k).
//@page module div3_msb
//@page module div3_lsb
//@page module div_fsm

module tb;
  logic clk = 0, rst_n = 0;
  always #5 clk = ~clk;

  logic bm, bl;
  logic [3:0] d1, d2, d3, d4;
  logic o_msb, o_lsb, o1, o2, o3, o4;
  int errors = 0;

  div3_msb u_msb (.clk, .rst_n, .din(bm), .div(o_msb));
  div3_lsb u_lsb (.clk, .rst_n, .din(bl), .div(o_lsb));
  div_fsm #(.M(7), .B(8), .LSB(1))  u1 (.clk, .rst_n, .d(d1[2:0]), .div(o1));
  div_fsm #(.M(7), .B(10), .LSB(0)) u2 (.clk, .rst_n, .d(d2), .div(o2));
  div_fsm #(.M(9), .B(2), .LSB(1))  u3 (.clk, .rst_n, .d(d3[0]), .div(o3));
  div_fsm #(.M(5), .B(16), .LSB(1)) u4 (.clk, .rst_n, .d(d4), .div(o4));

  // the reference: the remainder of the value read so far, and B^k mod m for the LSB
  int rm, rl, r1, r2, r3, r4, p_l, p1, p3, p4;

  task automatic check(string what, logic got, int rem);
    if (got !== (rem == 0)) begin errors++; $display("%s: div=%0b, remainder %0d", what, got, rem); end
  endtask

  initial begin
    rm = 0; rl = 0; r1 = 0; r2 = 0; r3 = 0; r4 = 0;
    p_l = 1; p1 = 1; p3 = 1; p4 = 1;
    {bm, bl, d1, d2, d3, d4} = '0;
    repeat (2) @(posedge clk);
    for (int t = 0; t < 5000; t++) begin
      @(negedge clk);
      if (t % 600 == 0) begin                // start a new number now and then
        rst_n = 0; #1 rst_n = 1;
        rm = 0; rl = 0; r1 = 0; r2 = 0; r3 = 0; r4 = 0; p_l = 1; p1 = 1; p3 = 1; p4 = 1;
      end
      bm = 1'($urandom); bl = 1'($urandom);
      d1 = 4'($urandom_range(0, 7)); d2 = 4'($urandom_range(0, 9));
      d3 = 4'($urandom_range(0, 1)); d4 = 4'($urandom_range(0, 15));
      @(posedge clk);
      rm = (2 * rm + bm) % 3;
      rl = (rl + bl * p_l) % 3; p_l = p_l * 2 % 3;
      r1 = (r1 + d1 * p1) % 7;  p1 = p1 * 8 % 7;
      r2 = (10 * r2 + d2) % 7;
      r3 = (r3 + d3 * p3) % 9;  p3 = p3 * 2 % 9;
      r4 = (r4 + d4 * p4) % 5;  p4 = p4 * 16 % 5;
      #1;
      check("div3_msb", o_msb, rm);
      check("div3_lsb", o_lsb, rl);
      check("M=7 B=8 LSB", o1, r1);
      check("M=7 B=10 MSB", o2, r2);
      check("M=9 B=2 LSB", o3, r3);
      check("M=5 B=16 LSB", o4, r4);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
