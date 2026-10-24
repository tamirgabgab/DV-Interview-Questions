// Question 0045: the page's three solvers against a hidden odd ball. For every ball, heavy and
// light: the tree of part a and the fixed weighings of part b on 12 balls in at most 3
// weighings, and odd_ball of part c for every n from 3 to 130 and for 363 in exactly the
// fewest weighings, ceil(log3(2n + 3)); every weighing has the same number of balls on both
// pans, each ball at most once and only balls 1 to n.
module tb;
  //@page virtual class scale
  //@page function automatic odd_t odd_ball_12_tree
  //@page localparam int CODES
  //@page localparam int MAXK

  int errors = 0;

  class hidden_scale extends scale;
    int n, odd, calls;
    bit heavy;
    function new(int n, int odd, bit heavy);
      this.n = n; this.odd = odd; this.heavy = heavy; calls = 0;
    endfunction
    function int w(int b);
      return b == odd ? (heavy ? 11 : 9) : 10;
    endfunction
    virtual function int weigh(int left[$], int right[$]);
      int l = 0, r = 0;
      bit seen[int];
      calls++;
      if (left.size() != right.size()) begin errors++; $display("n=%0d odd=%0d: %0d balls against %0d", n, odd, left.size(), right.size()); end
      foreach (left[i]) begin
        if (left[i] < 1 || left[i] > n || seen.exists(left[i])) begin errors++; $display("n=%0d: bad ball %0d", n, left[i]); end
        seen[left[i]] = 1; l += w(left[i]);
      end
      foreach (right[i]) begin
        if (right[i] < 1 || right[i] > n || seen.exists(right[i])) begin errors++; $display("n=%0d: bad ball %0d", n, right[i]); end
        seen[right[i]] = 1; r += w(right[i]);
      end
      return l > r ? 1 : r > l ? -1 : 0;
    endfunction
  endclass

  function automatic int fewest(int n);
    int k = 0, p = 1;
    while (p < 2 * n + 3) begin p *= 3; k++; end
    return k;
  endfunction

  task automatic check(string what, int n, int odd, bit heavy, odd_t got, int calls, int want);
    if (got.ball != odd || got.heavy != heavy) begin errors++; $display("%s n=%0d: ball %0d %s, got %0d %s", what, n, odd, heavy ? "heavy" : "light", got.ball, got.heavy ? "heavy" : "light"); end
    if (calls > want) begin errors++; $display("%s n=%0d ball %0d: %0d weighings, at most %0d", what, n, odd, calls, want); end
  endtask

  initial begin
    hidden_scale s;
    odd_t got;
    int worst;
    for (int odd = 1; odd <= 12; odd++)
      for (int h = 0; h < 2; h++) begin
        s = new(12, odd, h); got = odd_ball_12_tree(s); check("tree", 12, odd, h, got, s.calls, 3);
        s = new(12, odd, h); got = odd_ball_12(s);      check("codes", 12, odd, h, got, s.calls, 3);
      end
    for (int n = 3; n <= 363; n++) begin
      if (n > 130 && n != 363) continue;
      worst = 0;
      for (int odd = 1; odd <= n; odd++)
        for (int h = 0; h < 2; h++) begin
          s = new(n, odd, h); got = odd_ball(n, s); check("odd_ball", n, odd, h, got, s.calls, fewest(n));
          if (s.calls > worst) worst = s.calls;
        end
      if (worst != fewest(n)) begin errors++; $display("n=%0d: %0d weighings, the fewest is %0d", n, worst, fewest(n)); end
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
