// Question 0051: the page's functions on every bottle of small cellars for one to four
// rounds (find_bottle of the deaths gives the bottle back), the page's numbers (10, 7 and
// 5 mice for 1000 bottles; bottle 613 in two rounds) and the edge cases.
module tb;
  //@page function automatic int mice_needed

  int errors = 0;

  // the deaths of a run: mouse i dies in round drink_round(x, i) of the poisoned bottle
  function automatic void deaths(int x, int m, int rounds, ref int death[]);
    death = new[m];
    for (int i = 0; i < m; i++) death[i] = drink_round(x, i, rounds);
  endfunction

  initial begin
    int death[];
    int m;
    int want613[7] = '{1, 0, 2, 1, 1, 2, 0};
    if (mice_needed(1000, 1) != 10 || mice_needed(1000, 2) != 7 || mice_needed(1000, 3) != 5 || mice_needed(1000, 9) != 3) begin
      errors++; $display("mice_needed(1000, b) wrong");
    end
    if (mice_needed(1, 1) != 0 || mice_needed(1024, 1) != 10 || mice_needed(1025, 1) != 11) begin
      errors++; $display("edge cases wrong");
    end
    deaths(613, 7, 2, death);
    foreach (want613[i]) if (death[i] != want613[i]) begin errors++; $display("613 digit %0d = %0d", i, death[i]); end
    if (find_bottle(death, 2) != 613) begin errors++; $display("find_bottle(613) = %0d", find_bottle(death, 2)); end
    for (int rounds = 1; rounds <= 4; rounds++)
      for (int n = 1; n <= 300; n += 7) begin
        m = mice_needed(n, rounds);            // an initializer here would run once (static)
        for (int x = 0; x < n; x++) begin
          deaths(x, m, rounds, death);
          if (find_bottle(death, rounds) != x) begin errors++; $display("n=%0d b=%0d x=%0d", n, rounds, x); end
        end
      end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
