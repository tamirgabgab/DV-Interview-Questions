module tb;
  //@page function automatic void swap_temp
  //@page function automatic void swap_arith
  //@page function automatic void swap_xor

  int errors = 0;

  task automatic check(string name, int got_a, int got_b, int exp_a, int exp_b);
    if (got_a != exp_a || got_b != exp_b) begin
      errors++;
      $display("FAIL %s: got (%0d, %0d) expected (%0d, %0d)", name, got_a, got_b, exp_a, exp_b);
    end
  endtask

  initial begin
    int a, b, x;
    int pairs[6][2] = '{'{5, 3}, '{-7, 12}, '{32'h7fffffff, 1}, '{0, 0}, '{32'h80000000, -1}, '{123456789, -987654321}};
    foreach (pairs[k]) begin
      a = pairs[k][0]; b = pairs[k][1]; swap_temp(a, b);  check("temp",  a, b, pairs[k][1], pairs[k][0]);
      a = pairs[k][0]; b = pairs[k][1]; swap_arith(a, b); check("arith", a, b, pairs[k][1], pairs[k][0]);
      a = pairs[k][0]; b = pairs[k][1]; swap_xor(a, b);   check("xor",   a, b, pairs[k][1], pairs[k][0]);
    end
    // Same variable twice: documented pitfall
    x = 9; swap_temp(x, x);  check("temp alias",  x, 0, 9, 0);
    x = 9; swap_arith(x, x); check("arith alias", x, 0, 0, 0);
    x = 9; swap_xor(x, x);   check("xor alias",   x, 0, 0, 0);
    if (errors == 0) $display("PASS");
    $finish;
  end
endmodule
