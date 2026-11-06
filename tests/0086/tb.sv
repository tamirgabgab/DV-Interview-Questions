// Question 0086: the page's SystemVerilog. meetings_to and min_meetings against a
// breadth-first search written here (every state with counts up to 9, each colour), and
// meeting_plan replayed meeting by meeting: legal meetings only, the colour asked for at
// the end, as many meetings as meetings_to says. The numbers of the page: 13, 15, 17 has no
// single colour; 13, 16, 17 turns blue in 16; 14, 15, 17 green in 17; 7, 1, 3 in the plan
// of the table.
module tb;
  //@page function automatic int meeting_plan
  //@page function automatic int meetings_to

  int errors = 0;
  localparam int M = 9;

  // the fewest meetings from s to the state where every chameleon is of colour c, or -1
  function automatic int bfs_to(int s[3], int c);
    int depth[int];
    int queue[$];
    int n = s[0] + s[1] + s[2], cur, t[3], u[3], key, goal;
    goal = (c == 0) ? n * 10000 : (c == 1) ? n * 100 : n;
    key = s[0] * 10000 + s[1] * 100 + s[2];
    depth[key] = 0; queue.push_back(key);
    while (queue.size() > 0) begin
      cur = queue.pop_front();
      if (cur == goal) return depth[cur];
      t[0] = cur / 10000; t[1] = (cur / 100) % 100; t[2] = cur % 100;
      for (int i = 0; i < 3; i++)
        for (int j = i + 1; j < 3; j++)
          if (t[i] > 0 && t[j] > 0) begin
            u = t; u[i]--; u[j]--; u[3 - i - j] += 2;
            key = u[0] * 10000 + u[1] * 100 + u[2];
            if (!depth.exists(key)) begin depth[key] = depth[cur] + 1; queue.push_back(key); end
          end
    end
    return -1;
  endfunction

  // replay "RG RB ..." from s; returns 1 if every meeting is legal and all end in colour c
  function automatic bit replay(int s[3], int c, string plan);
    int t[3], i, j, k = 0;
    t = s;
    while (k < plan.len()) begin
      i = (plan[k] == "R") ? 0 : (plan[k] == "G") ? 1 : 2;
      j = (plan[k + 1] == "R") ? 0 : (plan[k + 1] == "G") ? 1 : 2;
      if (i >= j || t[i] == 0 || t[j] == 0) return 0;
      t[i]--; t[j]--; t[3 - i - j] += 2;
      k += 3;
    end
    for (int x = 0; x < 3; x++) if (x != c && t[x] != 0) return 0;
    return 1;
  endfunction

  initial begin
    int s[3], m, want, colour, best, best_c;
    string plan;

    s = '{13, 15, 17};
    if (min_meetings(s, colour) != -1) begin errors++; $display("13, 15, 17: no single colour"); end
    s = '{13, 16, 17};
    m = min_meetings(s, colour);
    $display("13, 16, 17: %0d meetings, colour %0d", m, colour);
    if (m != 16 || colour != 2) begin errors++; $display("expected 16 meetings to blue"); end
    s = '{14, 15, 17};
    if (min_meetings(s, colour) != 17 || colour != 1) begin errors++; $display("14, 15, 17: 17 to green"); end
    s = '{7, 1, 3};
    m = meeting_plan(s, 2, plan);
    $display("7, 1, 3 to blue: %s", plan);
    if (m != 7 || plan != "RG RB RG RG RB RG RG") begin errors++; $display("unexpected plan"); end

    for (int r = 0; r <= M; r++)
      for (int g = 0; g <= M; g++)
        for (int b = 0; b <= M; b++) begin
          if (r + g + b == 0) continue;
          s = '{r, g, b};
          best = -1; best_c = -1;
          for (int c = 0; c < 3; c++) begin
            want = bfs_to(s, c);
            m = meetings_to(s, c);
            if (m != want) begin errors++; $display("%0d, %0d, %0d to %0d: %0d, the search says %0d", r, g, b, c, m, want); end
            if (want >= 0 && (best < 0 || want < best)) begin best = want; best_c = c; end
            if (m >= 0) begin
              if (meeting_plan(s, c, plan) != m || !replay(s, c, plan)) begin
                errors++; $display("%0d, %0d, %0d to %0d: the plan '%s' is wrong", r, g, b, c, plan);
              end
            end
          end
          m = min_meetings(s, colour);
          if (m != best || colour != best_c) begin errors++; $display("%0d, %0d, %0d: min %0d (%0d), expected %0d (%0d)", r, g, b, m, colour, best, best_c); end
        end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
