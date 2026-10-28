//@flags --timing
// Question 0056: the page's win3_lsb, win3_msb and win_div (several parameter sets, start
// windows and both directions) clocked on random bits and digits; every cycle each div is
// compared with the window kept here as a value, stepped by the definition (at the LSB:
// w = (B*w + d) mod B^L; at the MSB: w = d*B^(L-1) + w / B) and divided by m afresh.
//@page module win3_lsb
//@page module win3_msb
//@page module win_div

module tb;
  logic clk = 0, rst_n = 0;
  always #5 clk = ~clk;

  logic b1, b2, b3, b4;
  logic [3:0] d1, d2, d3, d4, d5;
  logic o1, o2, o3, o4, g1, g2, g3, g4, g5;
  int errors = 0;

  win3_lsb #(.L(1))                     u1 (.clk, .rst_n, .din(b1), .div(o1));
  win3_lsb #(.L(5), .INIT(5'b10110))    u2 (.clk, .rst_n, .din(b2), .div(o2));
  win3_msb #(.L(1))                     u3 (.clk, .rst_n, .din(b3), .div(o3));
  win3_msb #(.L(6), .INIT(6'b100101))   u4 (.clk, .rst_n, .din(b4), .div(o4));
  win_div #(.M(7), .B(8),  .L(3), .MSB(0))              v1 (.clk, .rst_n, .d(d1[2:0]), .div(g1));
  win_div #(.M(7), .B(10), .L(4), .MSB(1), .INIT(1234)) v2 (.clk, .rst_n, .d(d2), .div(g2));
  win_div #(.M(9), .B(2),  .L(6), .MSB(1), .INIT(37))   v3 (.clk, .rst_n, .d(d3[0]), .div(g3));
  win_div #(.M(5), .B(16), .L(2), .MSB(0), .INIT(200))  v4 (.clk, .rst_n, .d(d4), .div(g4));
  win_div #(.M(3), .B(10), .L(1), .MSB(1), .INIT(7))    v5 (.clk, .rst_n, .d(d5), .div(g5));

  // the reference windows, as values
  longint w1, w2, w3, w4, x1, x2, x3, x4, x5;

  function automatic longint lsb_in(longint w, longint d, longint b, int L);
    return (w * b + d) % (b ** L);
  endfunction
  function automatic longint msb_in(longint w, longint d, longint b, int L);
    return d * (b ** (L - 1)) + w / b;
  endfunction
  task automatic check(string what, logic got, longint w, longint m);
    if (got !== (w % m == 0)) begin errors++; $display("%s: div=%0b, window %0d", what, got, w); end
  endtask
  task automatic start();
    w1 = 0; w2 = 5'b10110; w3 = 0; w4 = 6'b100101;
    x1 = 0; x2 = 1234; x3 = 37; x4 = 200; x5 = 7;
  endtask

  initial begin
    start();
    {b1, b2, b3, b4, d1, d2, d3, d4, d5} = '0;
    repeat (2) @(posedge clk);
    for (int t = 0; t < 6000; t++) begin
      @(negedge clk);
      if (t % 700 == 0) begin                // reset now and then: the start windows again
        rst_n = 0; #1 rst_n = 1;
        start();
        #1;
        check("reset L=5 LSB", o2, w2, 3);
        check("reset L=6 MSB", o4, w4, 3);
        check("reset M=7 B=10 MSB", g2, x2, 7);
        check("reset M=9 B=2 MSB", g3, x3, 9);
        check("reset M=5 B=16 LSB", g4, x4, 5);
        check("reset M=3 B=10 L=1", g5, x5, 3);
      end
      b1 = 1'($urandom); b2 = 1'($urandom); b3 = 1'($urandom); b4 = 1'($urandom);
      d1 = 4'($urandom_range(0, 7)); d2 = 4'($urandom_range(0, 9)); d3 = 4'($urandom_range(0, 1));
      d4 = 4'($urandom_range(0, 15)); d5 = 4'($urandom_range(0, 9));
      @(posedge clk);
      w1 = lsb_in(w1, b1, 2, 1); w2 = lsb_in(w2, b2, 2, 5);
      w3 = msb_in(w3, b3, 2, 1); w4 = msb_in(w4, b4, 2, 6);
      x1 = lsb_in(x1, d1, 8, 3); x2 = msb_in(x2, d2, 10, 4); x3 = msb_in(x3, d3, 2, 6);
      x4 = lsb_in(x4, d4, 16, 2); x5 = msb_in(x5, d5, 10, 1);
      #1;
      check("win3_lsb L=1", o1, w1, 3);
      check("win3_lsb L=5", o2, w2, 3);
      check("win3_msb L=1", o3, w3, 3);
      check("win3_msb L=6", o4, w4, 3);
      check("M=7 B=8 L=3 LSB", g1, x1, 7);
      check("M=7 B=10 L=4 MSB", g2, x2, 7);
      check("M=9 B=2 L=6 MSB", g3, x3, 9);
      check("M=5 B=16 L=2 LSB", g4, x4, 5);
      check("M=3 B=10 L=1 MSB", g5, x5, 3);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
