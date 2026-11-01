//@flags --timing
// Question 0075: the page's transpose8_loop and transpose8 against each other and the
// definition on every single bit and random words; transpose32 on random matrices; and the
// module bit_transpose at N = 8 and N = 4 against the functions.
//@page function automatic logic [63:0] transpose8_loop
//@page function automatic logic [63:0] delta_swap
//@page function automatic void transpose32
//@page module bit_transpose

module tb;
  int errors = 0;
  logic [63:0] in8, out8;
  logic [15:0] in4, out4;

  bit_transpose #(.N(8)) dut8 (.in(in8), .out(out8));
  bit_transpose #(.N(4)) dut4 (.in(in4), .out(out4));

  function automatic logic [15:0] transpose4_ref(logic [15:0] x);
    logic [15:0] y;
    for (int r = 0; r < 4; r++)
      for (int c = 0; c < 4; c++) y[4*c + r] = x[4*r + c];
    return y;
  endfunction

  initial begin
    logic [63:0] x;
    logic [31:0] a[32], rows[32];
    for (int b = 0; b < 64; b++) begin
      x = 64'd1 << b;
      if (transpose8(x) != (64'd1 << (8 * (b % 8) + b / 8)) || transpose8_loop(x) != transpose8(x)) begin
        errors++; $display("bit %0d", b);
      end
    end
    for (int k = 0; k < 2000; k++) begin
      x = {$urandom, $urandom};
      if (transpose8(x) != transpose8_loop(x) || transpose8(transpose8(x)) != x) begin errors++; $display("word %h", x); end
      in8 = x;
      in4 = x[15:0];
      #1;
      if (out8 != transpose8_loop(x) || out4 != transpose4_ref(x[15:0])) begin errors++; $display("rtl %h", x); end
    end
    for (int k = 0; k < 50; k++) begin
      foreach (rows[r]) rows[r] = $urandom;
      a = rows;
      transpose32(a);
      for (int r = 0; r < 32; r++)
        for (int c = 0; c < 32; c++)
          if (a[c][r] != rows[r][c]) begin errors++; $display("t32 %0d %0d", r, c); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
