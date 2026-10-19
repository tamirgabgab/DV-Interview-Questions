module tb;
  //@page function automatic bit measure_from_zero

  // Replay a plan ("0:AB 7:A ...") from rest and return the time of its last event,
  // or -1 when the plan is inconsistent (action at a time that is not an event, nothing running).
  function automatic int replay(int A, int B, string plan);
    int t = 0, a = 0, b = 0, i = 0, when, delay;
    string action;
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
    end
    return t;
  endfunction

  initial begin
    string plan;
    bit    ok, want;
    int    A, B;
    int    errors = 0;
    // Which D (1..30) can be measured from time 0, per (A, B); computed independently in test_0018.py.
    int    pairs[$] = {3, 5, 4, 7, 7, 11, 4, 6, 5, 8};
    int    expected[5][$] = '{
      '{3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30},
      '{4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30},
      '{7, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30},
      '{4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30},
      '{5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}
    };

    ok = measure_from_zero(7, 11, 15, plan);
    if (!ok || plan != "0:AB 7:A 11:A") begin
      $display("page example: ok=%0d plan='%s'", ok, plan);
      errors++;
    end

    for (int k = 0; k < 5; k++) begin
      A = pairs[2 * k];                  // assigned, not initialised: an initialiser in a loop runs once
      B = pairs[2 * k + 1];
      for (int D = 1; D <= 30; D++) begin
        want = 0;
        foreach (expected[k][j]) if (expected[k][j] == D) want = 1;
        ok = measure_from_zero(A, B, D, plan);
        if (ok != want) begin
          $display("A=%0d B=%0d D=%0d: ok=%0d expected %0d", A, B, D, ok, want);
          errors++;
        end
        else if (ok && replay(A, B, plan) != D) begin
          $display("A=%0d B=%0d D=%0d: plan '%s' does not end at D", A, B, D, plan);
          errors++;
        end
      end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
