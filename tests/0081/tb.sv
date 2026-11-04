// Question 0081: the page's SystemVerilog: count_queens for N = 1 .. 12 against the known
// counts (and with row 0 limited, against the halves), count_half equal to it, distinct
// (the solutions up to rotation and reflection) for N = 1 .. 10, and construct checked to be
// a solution (a permutation with no two queens on a diagonal) for every N from 4 to 64.
module tb;
  //@page function automatic int count_queens
  //@page function automatic int count_half
  //@page function automatic void construct

  int errors = 0;

  task automatic same(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: got %0d, expected %0d", what, got, want); end
  endtask

  // in the initial block every variable is declared here and assigned in the loops: an
  // initialiser inside a loop of an initial block is static and runs once (IEEE 6.21)
  initial begin
    int counts[13] = '{0, 1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200};
    int classes[11] = '{0, 1, 0, 0, 1, 2, 1, 6, 12, 46, 92};
    int halves[11] = '{0, 0, 0, 0, 1, 4, 2, 17, 46, 149, 362};
    int col[64];
    bit used[65];
    bit ok;

    for (int n = 1; n <= 12; n++) begin
      same($sformatf("count_queens(%0d)", n), count_queens(n), counts[n]);
      same($sformatf("count_half(%0d)", n), count_half(n), counts[n]);
    end
    for (int n = 4; n <= 10; n++) same($sformatf("count_queens(%0d, half)", n), count_queens(n, (1 << (n / 2)) - 1), halves[n]);
    for (int n = 1; n <= 10; n++) same($sformatf("distinct(%0d)", n), distinct(n), classes[n]);

    for (int n = 4; n <= 64; n++) begin
      construct(n, col);
      ok = 1;
      foreach (used[i]) used[i] = 0;
      for (int i = 0; i < n; i++) begin
        if (col[i] < 1 || col[i] > n || used[col[i]]) ok = 0;
        else used[col[i]] = 1;
        for (int j = 0; j < i; j++)
          if (col[i] - col[j] == i - j || col[j] - col[i] == i - j) ok = 0;
      end
      if (!ok) begin errors++; $display("construct(%0d) is not a solution", n); end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
