//@flags --assert --timing --coverage-user
// Question 0082: the page's nim_move, misere_move, grundy and subtraction_move. Every
// position of three heaps of 0 to 7 is solved by brute force (a position wins when some
// legal move leads to a losing one), for the three rules: the last to take wins, the last to
// take loses, and a move takes only 1, 3 or 4. Each function must return 0 exactly on the
// losing positions, and otherwise a legal move to a losing position.
// Then the page's combinational nim_move_hw (3 heaps of 3 bits) gets all 512 positions, one
// per clock, against the same brute force, with the page's nim_move_check bound to it: no
// assertion fails and the covers count the lost positions (64) and the candidate heaps (1 or
// 3); a copy with a bug (a candidate is any heap sharing a bit with x) must fail a_move.
//@page module nim_move_hw
//@page module nim_move_check

// the bug: a heap that shares any bit with x is taken as a candidate, not only the top bit
module nim_move_bug #(parameter int N = 3, parameter int W = 3) (
  input  logic [N-1:0][W-1:0]  heap,
  output logic                 valid,
  output logic [$clog2(N)-1:0] idx,
  output logic [W-1:0]         new_size
);
  logic [W-1:0] x;
  logic [N-1:0] cand;
  always_comb begin
    x = '0;
    for (int i = 0; i < N; i++) x ^= heap[i];
    for (int i = 0; i < N; i++) cand[i] = |(heap[i] & x);
    valid = |cand;
    idx = '0;
    for (int i = N - 1; i >= 0; i--) if (cand[i]) idx = i;
    new_size = heap[idx] ^ x;
  end
endmodule

module tb;
  //@page function automatic bit nim_move
  //@page function automatic bit misere_move
  //@page function automatic int grundy

  localparam int M = 8;
  bit win_n[M * M * M], win_m[M * M * M], win_s[M * M * M];
  int errors = 0;

  // the hardware: 3 heaps of 3 bits, heap[0] in the low bits
  logic clk = 0;
  logic [2:0][2:0] heap = '0;
  logic valid, bvalid;
  logic [1:0] idx_hw, bidx;
  logic [2:0] new_hw, bnew;
  always #5 clk = ~clk;
  nim_move_hw #(.N(3), .W(3)) dut (.heap, .valid, .idx(idx_hw), .new_size(new_hw));
  nim_move_check #(.N(3), .W(3)) chk (.clk, .heap, .valid, .idx(idx_hw), .new_size(new_hw));
  nim_move_bug #(.N(3), .W(3)) bug (.heap, .valid(bvalid), .idx(bidx), .new_size(bnew));
  nim_move_check #(.N(3), .W(3)) bchk (.clk, .heap, .valid(bvalid), .idx(bidx), .new_size(bnew));

  function automatic int at(int a, int b, int c);
    return (a * M + b) * M + c;
  endfunction

  // the position after heap i of (a, b, c) goes down to v
  function automatic int after(int a, int b, int c, int i, int v);
    if (i == 0) return at(v, b, c);
    if (i == 1) return at(a, v, c);
    return at(a, b, v);
  endfunction

  initial begin
    int h[3], q[$], sub[$], idx, nw, p, cnt;
    bit got, ok, any_n, any_m, any_s;
    int want[7];
    want = '{0, 1, 0, 1, 2, 3, 2};
    sub = '{1, 3, 4};
    // brute force, by the number of tokens: every move lowers it
    for (int s = 0; s <= 3 * (M - 1); s++)
      for (int a = 0; a < M; a++)
        for (int b = 0; b < M; b++)
          for (int c = 0; c < M; c++) begin
            if (a + b + c != s) continue;
            h = '{a, b, c};
            any_n = 0; any_m = 0; any_s = 0;
            for (int i = 0; i < 3; i++)
              for (int v = 0; v < h[i]; v++) begin
                p = after(a, b, c, i, v);
                if (!win_n[p]) any_n = 1;
                if (!win_m[p]) any_m = 1;
                if ((h[i] - v == 1 || h[i] - v == 3 || h[i] - v == 4) && !win_s[p]) any_s = 1;
              end
            win_n[at(a, b, c)] = any_n;
            win_s[at(a, b, c)] = any_s;
            // the last to take loses: the player who faces the empty table has won
            win_m[at(a, b, c)] = (s == 0) ? 1 : any_m;
          end
    cnt = 0;
    for (int a = 0; a < M; a++)
      for (int b = 0; b < M; b++)
        for (int c = 0; c < M; c++) begin
          h = '{a, b, c};
          q = '{a, b, c};
          // normal Nim
          got = nim_move(q, idx, nw);
          ok = got == win_n[at(a, b, c)];
          if (got) ok = ok && idx >= 0 && idx < 3 && nw >= 0 && nw < h[idx] && !win_n[after(a, b, c, idx, nw)];
          if (!ok) begin errors++; $display("nim_move (%0d, %0d, %0d): got %0d, heap %0d to %0d", a, b, c, got, idx, nw); end
          // misère Nim, with at least one token
          if (a + b + c > 0) begin
            got = misere_move(q, idx, nw);
            ok = got == win_m[at(a, b, c)];
            if (got) ok = ok && idx >= 0 && idx < 3 && nw >= 0 && nw < h[idx] && !win_m[after(a, b, c, idx, nw)];
            if (!ok) begin errors++; $display("misere_move (%0d, %0d, %0d): got %0d, heap %0d to %0d", a, b, c, got, idx, nw); end
          end
          // the subtraction game {1, 3, 4}
          got = subtraction_move(q, sub, idx, nw);
          ok = got == win_s[at(a, b, c)];
          if (got) ok = ok && idx >= 0 && idx < 3 && (h[idx] - nw == 1 || h[idx] - nw == 3 || h[idx] - nw == 4) &&
                         !win_s[after(a, b, c, idx, nw)];
          if (!ok) begin errors++; $display("subtraction_move (%0d, %0d, %0d): got %0d, heap %0d to %0d", a, b, c, got, idx, nw); end
          cnt++;
        end
    // the page's numbers: 3, 4, 5 wins by 3 -> 1; with 1, 3 or 4 it loses; g = 0 1 0 1 2 3 2, period 7
    q = '{3, 4, 5};
    if (!nim_move(q, idx, nw) || idx != 0 || nw != 1) begin errors++; $display("3, 4, 5: not 3 -> 1"); end
    if (subtraction_move(q, sub, idx, nw)) begin errors++; $display("3, 4, 5 with 1, 3, 4: not lost"); end
    for (int n = 0; n < 30; n++) begin
      if (grundy(n, sub) != want[n % 7]) begin errors++; $display("g(%0d) = %0d", n, grundy(n, sub)); end
    end
    q = '{1, 1, 4};
    if (!misere_move(q, idx, nw) || idx != 2 || nw != 1) begin errors++; $display("1, 1, 4 misere: not 4 -> 1"); end
    if (cnt != M * M * M) errors++;
    // the hardware: position p = heap[0] + 8 heap[1] + 64 heap[2], one per clock; the
    // checker samples each on the next rising edge
    for (int p = 0; p < M * M * M; p++) begin
      if (p > 0) @(negedge clk);
      heap = 9'(p);
      #1;
      ok = valid == win_n[at(heap[0], heap[1], heap[2])];
      if (valid) ok = ok && idx_hw < 3 && new_hw < heap[idx_hw] &&
                      !win_n[after(heap[0], heap[1], heap[2], idx_hw, new_hw)];
      if (!ok) begin errors++; $display("nim_move_hw (%0d, %0d, %0d): %0d, heap %0d to %0d", heap[0], heap[1], heap[2], valid, idx_hw, new_hw); end
    end
    @(negedge clk);
    if (chk.fails != 0) begin errors++; $display("nim_move_check: %0d failures on nim_move_hw", chk.fails); end
    if (chk.lost != 64 || chk.hits[1] + chk.hits[3] != 448 || chk.hits[1] == 0 || chk.hits[3] == 0) begin
      errors++; $display("covers: lost %0d, one candidate %0d, three %0d", chk.lost, chk.hits[1], chk.hits[3]);
    end
    if (bchk.fails == 0) begin errors++; $display("nim_move_check misses the bug"); end
    $display("hardware: lost %0d, one candidate %0d, three %0d; the bug fails %0d times", chk.lost, chk.hits[1], chk.hits[3], bchk.fails);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
