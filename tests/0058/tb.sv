// Question 0058: the page's best_total against a minimax written here on random rows of 1 to
// 9 coins, the page's numbers (6, 19, 2), and parity_move as the first player against random
// replies: it always collects its whole colour, at least half the sum.
module tb;
  //@page function automatic bit parity_move
  //@page function automatic int best_total

  int errors = 0;

  // the most the player to move collects on coins[i..j]
  function automatic int gain(int coins[], int i, int j);
    int rest = 0, a, b;
    if (i > j) return 0;
    for (int k = i; k <= j; k++) rest += coins[k];
    a = rest - gain(coins, i + 1, j);
    b = rest - gain(coins, i, j - 1);
    return a > b ? a : b;
  endfunction

  initial begin
    int coins[], n, i, j, mine, odd_s, even_s, k;
    coins = '{1, 2, 5, 3};          if (best_total(coins) != 6)  begin errors++; $display("1253"); end
    coins = '{1, 1, 9, 1, 1, 9};    if (best_total(coins) != 19) begin errors++; $display("119119"); end
    coins = '{1, 5, 1};             if (best_total(coins) != 2)  begin errors++; $display("151"); end
    for (int r = 0; r < 300; r++) begin
      n = $urandom_range(1, 9);
      coins = new[n];
      foreach (coins[m]) coins[m] = $urandom_range(1, 30);
      if (best_total(coins) != gain(coins, 0, n - 1)) begin errors++; $display("run %0d: %0d vs %0d", r, best_total(coins), gain(coins, 0, n - 1)); end
      if (n % 2 == 0) begin
        i = 0; j = n - 1; mine = 0; odd_s = 0; even_s = 0;
        foreach (coins[m]) if (m % 2 == 0) odd_s += coins[m]; else even_s += coins[m];
        while (i <= j) begin
          k = parity_move(coins, i, j) ? j : i;          // the trick
          mine += coins[k];
          if (k == i) i++; else j--;
          if (i <= j) begin if ($urandom_range(0, 1)) i++; else j--; end   // any reply
        end
        if (mine != (odd_s > even_s ? odd_s : even_s)) begin errors++; $display("parity run %0d: %0d", r, mine); end
      end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
