// Question 0089: the page's SystemVerilog. two_coins and can_pay_two for every pair of small
// coins against a direct table of the payable amounts; frobenius (Dijkstra on the remainders)
// and frobenius_dp (the plain run) for every pair and triple of small coins, against the same
// table: the largest amount that is not payable, and nothing payable is missed.
module tb;
  //@page function automatic bit two_coins
  //@page function automatic bit frobenius(

  int errors = 0;

  // the largest amount up to lim that the coins cannot pay, by a table (-1: none)
  function automatic int largest_by_table(int coins[$], int lim);
    bit ok[];
    int last = -1;
    ok = new[lim + 1];
    ok[0] = 1;
    for (int n = 1; n <= lim; n++) begin
      ok[n] = 0;
      foreach (coins[k]) if (coins[k] <= n && ok[n - coins[k]]) ok[n] = 1;
      if (!ok[n]) last = n;
    end
    return last;
  endfunction

  initial begin
    int g, cnt, g2, want, bad;
    int q[$];
    bit has;

    if (!two_coins(3, 5, g, cnt) || g != 7 || cnt != 4) begin errors++; $display("two_coins(3, 5): %0d %0d", g, cnt); end
    if (two_coins(6, 9, g, cnt)) begin errors++; $display("two_coins(6, 9) should be none"); end
    q = '{6, 9, 20};
    if (!frobenius(q, g) || g != 43) begin errors++; $display("frobenius(6, 9, 20) = %0d", g); end
    if (!frobenius_dp(q, g) || g != 43) begin errors++; $display("frobenius_dp(6, 9, 20) = %0d", g); end
    q = '{4, 6, 9, 20};
    if (!frobenius(q, g) || g != 11) begin errors++; $display("frobenius(4, 6, 9, 20) = %0d", g); end
    q = '{4, 6};
    if (frobenius(q, g) || frobenius_dp(q, g)) begin errors++; $display("4, 6 should have no largest"); end

    for (int a = 2; a <= 11; a++)
      for (int b = a + 1; b <= 13; b++) begin
        q = '{a, b};
        has = two_coins(a, b, g, cnt);
        if (has != (gcd2(a, b) == 1)) begin errors++; $display("two_coins(%0d, %0d) gcd", a, b); end
        if (!has) continue;
        want = largest_by_table(q, 2 * a * b);
        bad = 0;
        for (int n = 0; n <= want; n++) if (!can_pay_two(n, a, b)) bad++;
        if (g != want || cnt != bad) begin errors++; $display("two_coins(%0d, %0d): %0d %0d, table %0d %0d", a, b, g, cnt, want, bad); end
        for (int n = want + 1; n <= want + 2 * b; n++)
          if (!can_pay_two(n, a, b)) begin errors++; $display("can_pay_two(%0d, %0d, %0d)", n, a, b); end
      end

    for (int a = 2; a <= 9; a++)
      for (int b = a + 1; b <= 10; b++)
        for (int c = b + 1; c <= 11; c++) begin
          q = '{c, a, b};                                   // not sorted: the functions find the smallest
          has = frobenius(q, g);
          if (has != frobenius_dp(q, g2)) begin errors++; $display("%0d %0d %0d: the two disagree on the gcd", a, b, c); end
          if (!has) continue;
          want = largest_by_table(q, 2 * b * c);
          if (g != want || g2 != want) begin errors++; $display("%0d %0d %0d: %0d %0d, table %0d", a, b, c, g, g2, want); end
        end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
