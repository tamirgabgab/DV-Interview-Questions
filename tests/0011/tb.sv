// The class runs as published: Verilator (development snapshot after 5.052, see the CI
// workflow for the exact commit) with the z3 solver supports randomize() with the
// constraints, "solve result before board" and the inline constraint of part b. The 5.052
// release crashes on this class (segmentation fault in its randomization runtime on the
// rand enum array). The published final_result is checked against a full game tree, and
// every randomized board must be a legal end position with the result the class says.
//@page class ttt_end;

module tb;
  //@page function automatic bit final_result

  int errors = 0;

  function automatic void decode(int code, output board_t board);
    foreach (board[i]) begin
      board[i] = cell_e'(code % 3);
      code /= 3;
    end
  endfunction

  function automatic bit has_line(board_t board, cell_e p, int n_lines);
    for (int l = 0; l < n_lines; l++)
      if (board[ttt_end::LINES[l][0]] == p && board[ttt_end::LINES[l][1]] == p &&
          board[ttt_end::LINES[l][2]] == p) return 1;
    return 0;
  endfunction

  // Play every game (X first), one move at a time; ends[code] = result where a game stops
  function automatic void game_tree(int n_lines, ref result_e ends[int]);
    bit     level[int], next[int];
    board_t board;
    int     pow3[9];
    ends.delete();
    level.delete();
    level[0] = 1;
    pow3[0] = 1;
    for (int i = 1; i < 9; i++) pow3[i] = pow3[i - 1] * 3;
    for (int moves = 0; moves <= 9; moves++) begin
      next.delete();
      foreach (level[code]) begin
        decode(code, board);
        if (has_line(board, X, n_lines))      ends[code] = X_WINS;
        else if (has_line(board, O, n_lines)) ends[code] = O_WINS;
        else if (moves == 9)                 ends[code] = DRAW;
        else
          foreach (board[i])
            if (board[i] == EMPTY) next[code + pow3[i] * ((moves % 2 == 0) ? 1 : 2)] = 1;
      end
      level = next;
    end
  endfunction

  initial begin
    result_e ends[int];
    result_e r;
    board_t  board;
    ttt_end  t = new();
    int      seen[3];
    int      expect_total[2] = '{958, 1314};
    int      expect_draw[2]  = '{16, 0};
    int      n, legal_count;

    // 1. The page's final_result against the game tree, classic board and part b
    for (int k = 0; k < 2; k++) begin
      n = (k == 0) ? 8 : 12;
      game_tree(n, ends);
      if (ends.size() != expect_total[k]) errors++;
      legal_count = 0;
      seen = '{0, 0, 0};
      for (int code = 0; code < 19683; code++) begin
        decode(code, board);
        if (final_result(board, n, r)) begin
          legal_count++;
          seen[r]++;
          if (!ends.exists(code) || ends[code] != r) errors++;
        end else if (ends.exists(code)) errors++;
      end
      if (legal_count != expect_total[k] || seen[DRAW] != expect_draw[k]) errors++;
    end

    // 2. The class as published: every board legal for its result, every feasible result seen
    for (int k = 0; k < 2; k++) begin
      t.n_lines = (k == 0) ? 8 : 12;
      seen = '{0, 0, 0};
      repeat (150) begin
        if (!t.randomize()) errors++;
        seen[t.result]++;
        if (!final_result(t.board, t.n_lines, r) || r != t.result) errors++;
      end
      if (seen[X_WINS] == 0 || seen[O_WINS] == 0) errors++;
      if (k == 0 && seen[DRAW] == 0) errors++;           // classic board: draws exist (16 of 958)
      if (k == 1 && seen[DRAW] != 0) errors++;           // part b: no draw is possible
    end
    // part b: randomize() with { result == DRAW; } has no solution with the wrap-around lines
    // (expected: UNSATCONSTR warnings), and a solution on the classic board
    if (t.randomize() with { result == DRAW; }) errors++;
    t.n_lines = 8;
    if (!t.randomize() with { result == DRAW; } || t.result != DRAW) errors++;
    else if (!final_result(t.board, 8, r) || r != DRAW) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
