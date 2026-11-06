// Question 0091: the page's mirror_move, eat, chomp_table, winning_first and two_rows_move.
// chomp_table on every board of 1 to 7 rows and 1 to 8 columns: the first player wins every
// board but 1 x 1 (strategy stealing), and the first winning move matches the page's table
// (column * 16 + row, -1 for none); 8 x 8 has C(16, 8) = 12870 staircases and b2 wins. The
// mirror on the square boards 2 to 7: b2 first, the L with equal arms loses, and with unequal
// arms the mirror move leaves equal arms. The 2-row strategy on every position up to 2 x 8.
module tb;
  //@page function automatic bit mirror_move
  //@page function automatic void chomp_table
  //@page function automatic bit two_rows_move

  int errors = 0;
  int want[56] = '{-1, 16, 16, 16, 16, 16, 16, 16, 1, 17, 33, 49, 65, 81, 97, 113, 1, 18, 17, 33, 50, 49, 66, 65,
                   1, 19, 18, 17, 34, 33, 50, 49, 1, 20, 35, 34, 17, 50, 33, 100, 1, 21, 19, 18, 35, 17, 68, 50,
                   1, 22, 36, 35, 18, 68, 17, 34};

  // the staircase of an L: column a of up + 1 squares, then `right` columns of one square
  function automatic int ell(int up, int right);
    int h = 0;
    h[3:0] = up + 1;
    for (int c = 1; c <= right; c++) h[4*c +: 4] = 1;
    return h;
  endfunction

  function automatic int count_cols(int h, int n);
    int k = 0;
    for (int c = 0; c < n; c++) if (h[4*c +: 4] > 0) k++;
    return k;
  endfunction

  initial begin
    bit win[int];
    int col, row, full, h, t, got, cnt;
    bit ok;
    // every board: who wins, and the first winning move
    for (int m = 1; m <= 7; m++)
      for (int n = 1; n <= 8; n++) begin
        win.delete();
        chomp_table(m, n, win);
        full = 0;
        for (int c = 0; c < n; c++) full[4*c +: 4] = m;
        if (win[full] != (m != 1 || n != 1)) begin errors++; $display("%0d x %0d: win = %0d", m, n, win[full]); end
        ok = winning_first(m, n, win, col, row);
        got = ok ? col * 16 + row : -1;
        if (got != want[(m - 1) * 8 + (n - 1)]) begin
          errors++; $display("%0d x %0d: first winning move %0d, expected %0d", m, n, got, want[(m - 1) * 8 + (n - 1)]);
        end
      end
    // 8 x 8: 12870 staircases (the empty one included), b2 wins
    win.delete();
    chomp_table(8, 8, win);
    cnt = win.num();
    if (cnt != 12870) begin errors++; $display("8 x 8: %0d staircases", cnt); end
    if (!winning_first(8, 8, win, col, row) || col != 1 || row != 1) begin errors++; $display("8 x 8: not b2"); end
    // the mirror on n x n
    for (int n = 2; n <= 7; n++) begin
      win.delete();
      chomp_table(n, n, win);
      full = 0;
      for (int c = 0; c < n; c++) full[4*c +: 4] = n;
      if (!mirror_move(full, n, col, row) || col != 1 || row != 1) begin errors++; $display("%0d x %0d: the mirror does not open b2", n, n); end
      for (int up = 0; up < n; up++)
        for (int right = 0; right < n; right++) begin
          h = ell(up, right);
          ok = mirror_move(h, n, col, row);
          if (win[h] != (up != right) || ok != (up != right)) begin
            errors++; $display("L of %0d and %0d on %0d x %0d: win %0d, mirror %0d", up, right, n, n, win[h], ok);
          end
          if (ok) begin
            t = eat(h, n, col, row);
            if (t[3:0] - 1 != count_cols(t, n) - 1 || win[t]) begin
              errors++; $display("L of %0d and %0d: the mirror move %0d, %0d leaves unequal arms", up, right, col, row);
            end
          end
        end
    end
    // two rows: every position up to 2 x 8 (the packing holds 8 columns)
    for (int n = 1; n <= 8; n++) begin
      win.delete();
      chomp_table(2, n, win);
      for (int b = 1; b <= n; b++)
        for (int tp = 0; tp <= b; tp++) begin
          h = 0;
          for (int c = 0; c < b; c++) h[4*c +: 4] = (c < tp) ? 2 : 1;
          ok = two_rows_move(b, tp, col, row);
          if (ok != win[h]) begin errors++; $display("2 x %0d, rows %0d and %0d: move %0d, win %0d", n, b, tp, ok, win[h]); end
          if (ok) begin
            t = eat(h, n, col, row);
            if (win[t]) begin errors++; $display("2 x %0d, rows %0d and %0d: the move %0d, %0d does not win", n, b, tp, col, row); end
          end
        end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
