// Question 0083: the page's SystemVerilog. jugs_shortest for 3, 5 and 4 (six steps, the plan
// of the page), the impossible cases, and for every a <= 7, b <= 9, t <= 11 the rule: a plan
// exists exactly when t <= max(a, b) and gcd(a, b) divides t, replayed step by step to t; the
// minimum numbers of the examples table; split_shortest for 8, 5, 3 (seven pours, the page's
// plan) and from the 8 into the 3 first (seven more).
module tb;
  //@page function automatic int jugs_shortest
  //@page function automatic int split_shortest

  int errors = 0;

  function automatic int gcd_of(int a, int b);
    while (b != 0) begin int r = a % b; a = b; b = r; end
    return a;
  endfunction

  // replay a plan "fill B, pour B A, ..." from two empty jugs; returns 1 if a jug ends with t
  function automatic bit replay(int a, int b, int t, string plan);
    int x = 0, y = 0, i = 0, d;
    string w;
    while (i < plan.len()) begin
      int j = i;
      while (j < plan.len() && plan[j] != ",") j++;
      w = plan.substr(i, j - 1);
      case (w)
        "fill A": x = a;
        "fill B": y = b;
        "empty A": x = 0;
        "empty B": y = 0;
        "pour A B": begin d = (x < b - y) ? x : b - y; x -= d; y += d; end
        "pour B A": begin d = (y < a - x) ? y : a - x; x += d; y -= d; end
        default: return 0;
      endcase
      i = j + 2;
    end
    return x == t || y == t;
  endfunction

  initial begin
    string plan;
    int n, want_min[4][3], caps[3], start[3], goal[3];
    bit can;

    n = jugs_shortest(3, 5, 4, plan);
    $display("3, 5, 4: %0d steps: %s", n, plan);
    if (n != 6) begin errors++; $display("expected 6 steps"); end
    if (plan != "fill B, pour B A, empty A, pour B A, fill B, pour B A") begin errors++; $display("unexpected plan"); end
    if (jugs_shortest(3, 5, 7, plan) != -1) begin errors++; $display("7 litres with 3 and 5 is impossible"); end
    if (jugs_shortest(4, 6, 3, plan) != -1) begin errors++; $display("3 litres with 4 and 6 is impossible"); end
    if (jugs_shortest(3, 5, 1, plan) != 4) begin errors++; $display("1 litre with 3 and 5: 4 steps"); end
    if (jugs_shortest(7, 11, 6, plan) != 10) begin errors++; $display("6 litres with 7 and 11: 10 steps"); end
    if (jugs_shortest(6, 10, 8, plan) != 6) begin errors++; $display("8 litres with 6 and 10: 6 steps"); end

    for (int a = 1; a <= 7; a++)
      for (int b = 1; b <= 9; b++)
        for (int t = 0; t <= 11; t++) begin
          n = jugs_shortest(a, b, t, plan);
          can = t <= ((a > b) ? a : b) && t % gcd_of(a, b) == 0;
          if ((n >= 0) != can) begin errors++; $display("%0d, %0d, %0d: %0d steps, expected %s", a, b, t, n, can ? "a plan" : "none"); end
          else if (n > 0 && !replay(a, b, t, plan)) begin errors++; $display("%0d, %0d, %0d: the plan '%s' does not reach t", a, b, t, plan); end
        end

    caps = '{8, 5, 3}; start = '{8, 0, 0}; goal = '{4, 4, 0};
    n = split_shortest(caps, start, goal, plan);
    $display("8, 5, 3: %0d pours: %s", n, plan);
    if (n != 7) begin errors++; $display("expected 7 pours"); end
    if (plan != "8>5, 5>3, 3>8, 5>3, 8>5, 5>3, 3>8") begin errors++; $display("unexpected pours"); end
    start = '{5, 0, 3};
    if (split_shortest(caps, start, goal, plan) != 7) begin errors++; $display("from the 8 into the 3 first: 1 + 7 pours"); end
    caps = '{6, 4, 2}; start = '{6, 0, 0}; goal = '{3, 3, 0};
    if (split_shortest(caps, start, goal, plan) != -1) begin errors++; $display("6, 4, 2 into halves is impossible"); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
