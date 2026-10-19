module tb;
  //@page function automatic bit measure_interval

  // Replay a plan from rest. Returns the time of the last event (or -1 when the plan is
  // inconsistent) and sets `start_is_event` when `start` is one of the event times.
  function automatic int replay(int A, int B, string plan, int start, output bit start_is_event);
    int t = 0, a = 0, b = 0, i = 0, when, delay;
    string action;
    start_is_event = (start == 0);
    while (i < plan.len()) begin
      when = 0;
      while (i < plan.len() && plan[i] >= "0" && plan[i] <= "9") begin
        when = when * 10 + (plan[i] - "0");
        i++;
      end
      if (i >= plan.len() || plan[i] != ":") return -1;
      i++;
      action = "";
      while (i < plan.len() && plan[i] != " ") begin
        action = {action, plan.substr(i, i)};
        i++;
      end
      i++;                                         // skip the separating space
      if (when != t) return -1;
      foreach (action[k]) begin
        if (action[k] == "A") a = A - a;
        if (action[k] == "B") b = B - b;
      end
      if (a == 0 && b == 0) return -1;
      delay = (a == 0) ? b : (b == 0) ? a : (a < b ? a : b);
      t += delay;
      a = (a > delay) ? a - delay : 0;
      b = (b > delay) ? b - delay : 0;
      if (t == start) start_is_event = 1;
    end
    return t;
  endfunction

  initial begin
    string plan;
    int    start, last, A, B, D;
    bit    ok, start_ok;
    int    errors = 0;
    // (A, B, D, expected start, expected end); -1 = impossible. Verified against an
    // independent oracle in test_0019.py.
    int    cases[$] = {
      3, 5, 1, 5, 6,    3, 5, 2, 3, 5,    3, 5, 3, 0, 3,    3, 5, 4, 3, 7,    3, 5, 5, 0, 5,
      4, 7, 1, 7, 8,    4, 7, 2, 7, 9,    4, 7, 3, 4, 7,    4, 7, 5, 4, 9,    4, 7, 6, 4, 10,
      7, 11, 1, 21, 22, 7, 11, 2, 21, 23, 7, 11, 3, 11, 14, 7, 11, 4, 7, 11, 7, 11, 5, 21, 26,
      7, 11, 6, 11, 17, 7, 11, 8, 7, 15,  7, 11, 9, 11, 20, 7, 11, 10, 7, 17, 7, 11, 12, 7, 19,
      5, 8, 1, 15, 16,  5, 8, 2, 8, 10,   5, 8, 4, 8, 12,   5, 8, 7, 5, 12,   5, 8, 9, 5, 14,
      4, 6, 1, -1, -1,  4, 6, 2, 4, 6,    4, 6, 3, -1, -1,  4, 6, 4, 0, 4,    4, 6, 5, -1, -1
    };

    ok = measure_interval(7, 11, 1, start, plan);
    if (!ok || start != 21 || plan != "0:AB 7:A 11:B 14:A 21:-") begin
      $display("page example: ok=%0d start=%0d plan='%s'", ok, start, plan);
      errors++;
    end

    for (int k = 0; k < cases.size(); k += 5) begin
      A = cases[k];                      // assigned, not initialised: an initialiser in a loop runs once
      B = cases[k + 1];
      D = cases[k + 2];
      ok = measure_interval(A, B, D, start, plan);
      if (!ok) begin
        if (cases[k + 3] != -1) begin
          $display("A=%0d B=%0d D=%0d: no plan, expected start %0d", A, B, D, cases[k + 3]);
          errors++;
        end
        continue;
      end
      last = replay(A, B, plan, start, start_ok);
      if (start != cases[k + 3] || last != cases[k + 4] || !start_ok) begin
        $display("A=%0d B=%0d D=%0d: start=%0d end=%0d plan='%s' (expected %0d..%0d)",
                 A, B, D, start, last, plan, cases[k + 3], cases[k + 4]);
        errors++;
      end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
