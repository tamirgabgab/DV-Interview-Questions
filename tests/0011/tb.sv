// Simulator limitation (Verilator 5.020): no randomize() with constraints. The translation
// keeps the class as published, turns every constraint block into a check function, and
// replaces randomize() by an exhaustive solver: it goes over every assignment of `board`
// (3^9 of them), keeps the ones that satisfy all constraints, and applies
// "solve result before board": a feasible result uniformly, then a solution with it uniformly.
//@translation-of class ttt_end; 21ff93603ab7

typedef enum bit [1:0] {EMPTY, X, O} cell_e;
typedef enum bit [1:0] {X_WINS, O_WINS, DRAW} result_e;
typedef cell_e board_t[9];

class ttt_end;
  static const int LINES[12][3] = '{'{0, 1, 2}, '{3, 4, 5}, '{6, 7, 8},
                                    '{0, 3, 6}, '{1, 4, 7}, '{2, 5, 8},
                                    '{0, 4, 8}, '{2, 4, 6},
                                    '{1, 5, 6}, '{2, 3, 7},
                                    '{0, 5, 7}, '{1, 3, 8}};
  int n_lines = 8;

  board_t  board;                       // was: rand
  result_e result;                     // was: rand
  int      n_x, n_o;                   // was: rand
  bit      x_line[12], o_line[12];     // was: rand
  int      x_lines, o_lines;           // was: rand

  int      sol_code[$];               // solver cache: every solution (base-3 code of board)
  result_e sol_result[$];             // ... and the value of result in it
  int solved_for = 0;                  // n_lines the cache was built for

  // The equalities of c_count and c_lines fix every helper variable from `board`
  function void derive();
    n_x = 0; n_o = 0; x_lines = 0; o_lines = 0;
    foreach (board[i]) begin
      n_x += (board[i] == X);
      n_o += (board[i] == O);
    end
    foreach (x_line[l]) begin
      x_line[l] = (l < n_lines && board[LINES[l][0]] == X && board[LINES[l][1]] == X && board[LINES[l][2]] == X);
      o_line[l] = (l < n_lines && board[LINES[l][0]] == O && board[LINES[l][1]] == O && board[LINES[l][2]] == O);
      x_lines += x_line[l];
      o_lines += o_line[l];
    end
  endfunction

  // constraint c_count (the inside part)
  function bit c_count_ok();
    return n_x == n_o || n_x == n_o + 1;
  endfunction

  // constraint c_result, for a given value of result
  function bit c_result_ok(result_e r);
    if (r == X_WINS) return x_lines > 0 && o_lines == 0 && n_x == n_o + 1;
    if (r == O_WINS) return o_lines > 0 && x_lines == 0 && n_x == n_o;
    return x_lines == 0 && o_lines == 0 && n_x + n_o == 9;
  endfunction

  function void decode(int code);
    foreach (board[i]) begin
      board[i] = cell_e'(code % 3);
      code /= 3;
    end
  endfunction

  // Replacement for randomize() (and randomize() with { result == want; })
  function bit test_randomize(bit with_result = 0, result_e want = X_WINS);
    result_e feasible[$];
    int      matching[$];
    if (solved_for != n_lines) begin
      sol_code.delete();
      sol_result.delete();
      for (int code = 0; code < 19683; code++) begin
        decode(code);
        derive();
        if (!c_count_ok()) continue;
        for (int r = 0; r < 3; r++)
          if (c_result_ok(result_e'(r))) begin
            sol_code.push_back(code);
            sol_result.push_back(result_e'(r));
          end
      end
      solved_for = n_lines;
    end
    // solve result before board: a result that has a solution, uniformly
    feasible.delete();
    for (int r = 0; r < 3; r++)
      if ((!with_result || result_e'(r) == want) && (result_e'(r) inside {sol_result}))
        feasible.push_back(result_e'(r));
    if (feasible.size() == 0) return 0;
    result = feasible[$urandom_range(0, feasible.size() - 1)];
    // then one of its solutions, uniformly
    matching.delete();
    foreach (sol_code[i]) if (sol_result[i] == result) matching.push_back(sol_code[i]);
    decode(matching[$urandom_range(0, matching.size() - 1)]);
    derive();
    return 1;
  endfunction

  function string show();
    string s = "";
    foreach (board[i])
      s = {s, (board[i] == X) ? "X" : (board[i] == O) ? "O" : ".", (i % 3 == 2) ? "\n" : " "};
    return s;
  endfunction
endclass

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

    // 2. The class: every result equally likely, every board legal for its result
    for (int k = 0; k < 2; k++) begin
      t.n_lines = (k == 0) ? 8 : 12;
      seen = '{0, 0, 0};
      repeat (3000) begin
        if (!t.test_randomize()) errors++;
        seen[t.result]++;
        if (!final_result(t.board, t.n_lines, r) || r != t.result) errors++;
      end
      if (k == 0 && (seen[X_WINS] < 880 || seen[O_WINS] < 880 || seen[DRAW] < 880)) errors++;
      if (k == 1 && (seen[DRAW] != 0 || seen[X_WINS] < 1380 || seen[O_WINS] < 1380)) errors++;
    end
    if (t.test_randomize(1, DRAW)) errors++;      // part b: randomize() with { result == DRAW; }
    t.n_lines = 8;
    if (!t.test_randomize(1, DRAW) || t.result != DRAW) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
