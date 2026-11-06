// Question 0087: the page's SystemVerilog: press_masks, gauss, solve_lights, chase,
// solve_by_chasing, king_quiet and plus_nullity. Part a's example (the presses 3, 4, 5 and
// 7); every state of the boards up to 3 x 3 against the states the press sets reach; random
// boards up to 8 x 8 with and without diagonals (a solution turns every light off, chasing
// agrees with the elimination); the free variables of the boards (2n - 1 with diagonals when
// n % 3 == 2) and the quiet patterns of king_quiet (quiet, independent); plus_nullity against
// the free variables of the elimination and the table up to 30.
module tb;
  //@page typedef bit [127:0] vec_t;
  //@page function automatic vec_t chase
  //@page function automatic void king_quiet
  //@page function automatic int deg

  int errors = 0;

  task automatic same(string what, longint got, longint want);
    if (got != want) begin errors++; $display("%s: got %0d, expected %0d", what, got, want); end
  endtask

  function automatic vec_t apply(int n, bit diag, vec_t lit, vec_t press);
    vec_t m[$];
    press_masks(n, diag, m);
    for (int k = 0; k < n * n; k++) if (press[k]) lit ^= m[k];
    return lit;
  endfunction

  function automatic vec_t rand_vec(int bits);
    vec_t v = '0;
    for (int k = 0; k < bits; k++) v[k] = $urandom_range(0, 1);
    return v;
  endfunction

  initial begin
    vec_t x, y, lit, pats[$], full;
    bit ok, ok2;
    int f;
    int plus_free[30] = '{0, 0, 0, 4, 2, 0, 0, 0, 8, 0, 6, 0, 0, 4, 0, 8, 2, 0, 16, 0, 0, 0, 14, 4, 0, 0, 0, 0, 10, 20};

    // part a: the top row of 3 x 3
    f = solve_lights(3, 128'h7, 0, x, ok);
    same("3x3 ok", ok, 1);
    same("3x3 free", f, 0);
    same("3x3 presses", x, 128'hb8);

    // every state of the small boards against the states the press sets reach
    for (int d = 0; d < 2; d++)
      for (int n = 1; n <= 3; n++) begin
        bit reach[512];
        int count;
        count = 0;
        for (int s = 0; s < (1 << (n * n)); s++) reach[s] = 0;
        for (int p = 0; p < (1 << (n * n)); p++) begin
          y = apply(n, d, '0, vec_t'(p));
          reach[int'(y)] = 1;
        end
        for (int s = 0; s < (1 << (n * n)); s++) begin
          f = solve_lights(n, vec_t'(s), d, x, ok);
          same($sformatf("%0dx%0d d%0d state %0d solvable", n, n, d, s), ok, reach[s]);
          if (ok) same($sformatf("%0dx%0d d%0d state %0d off", n, n, d, s), apply(n, d, vec_t'(s), x) != 0, 0);
          count += reach[s];
        end
        same($sformatf("%0dx%0d d%0d reachable", n, n, d), count, 1 << (n * n - f));
      end

    // random boards, with and without diagonals; chasing without
    for (int n = 1; n <= 8; n++)
      for (int d = 0; d < 2; d++)
        for (int t = 0; t < 20; t++) begin
          lit = rand_vec(n * n);
          f = solve_lights(n, lit, d, x, ok);
          if (ok) same($sformatf("random %0d d%0d off", n, d), apply(n, d, lit, x) != 0, 0);
          else if (f == 0) begin errors++; $display("unsolvable with no free variable, n = %0d", n); end
          if (d == 0) begin
            ok2 = solve_by_chasing(n, lit, y);
            same($sformatf("chasing %0d agrees", n), ok2, ok);
            if (ok2) same($sformatf("chasing %0d off", n), apply(n, 0, lit, y) != 0, 0);
          end
        end

    // the free variables; with diagonals 2n - 1 when n % 3 == 2, and king_quiet's patterns
    for (int n = 1; n <= 11; n++) begin
      f = solve_lights(n, '0, 0, x, ok);
      same($sformatf("free %0d", n), f, plus_free[n - 1]);
      same($sformatf("plus_nullity %0d", n), plus_nullity(n), f);
      f = solve_lights(n, '0, 1, x, ok);
      same($sformatf("free with diagonals %0d", n), f, n % 3 == 2 ? 2 * n - 1 : 0);
      king_quiet(n, pats);
      same($sformatf("king_quiet %0d count", n), pats.size(), f);
      foreach (pats[i]) same($sformatf("king_quiet %0d quiet", n), apply(n, 1, '0, pats[i]) != 0, 0);
      if (pats.size()) same($sformatf("king_quiet %0d independent", n), gauss(pats, n * n, x, ok), n * n - pats.size());
      full = '0;
      for (int k = 0; k < n * n; k++) full[k] = 1;
      void'(solve_lights(n, full, 0, x, ok));
      same($sformatf("all lit %0d", n), ok, 1);
    end
    for (int n = 1; n <= 30; n++) same($sformatf("plus_nullity %0d", n), plus_nullity(n), plus_free[n - 1]);

    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
