// Question 0057: the page's last_fall, collisions and fall_times on the page's six ants
// (90 s, 5 collisions, the fall times 25 60 75 90 60 10), 100 ants at the bounds (100 s,
// 2500 collisions), and random poles against a half-second simulation written here (ants
// on doubled coordinates that turn at every meeting).
module tb;
  //@page function automatic int last_fall
  //@page function automatic int collisions
  //@page function automatic void fall_times
  //@page function automatic int ring_shift

  int errors = 0;

  // the simulation: returns each ant's fall time in half seconds and the collisions
  function automatic void simulate(int pos[], int dirs[], int len, ref int fall2[], ref int hits);
    int x[], d[];
    int n = pos.size(), left = pos.size(), tick = 0;
    x = new[n]; d = new[n]; fall2 = new[n];
    foreach (pos[i]) begin x[i] = 2 * pos[i]; d[i] = dirs[i]; fall2[i] = -1; end
    hits = 0;
    while (left > 0) begin
      foreach (x[i]) if (fall2[i] < 0 && ((x[i] <= 0 && d[i] < 0) || (x[i] >= 2 * len && d[i] > 0))) begin
        fall2[i] = tick; left--;
      end
      if (left == 0) break;
      foreach (x[i]) if (fall2[i] < 0) x[i] += d[i];
      tick++;
      for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
        if (fall2[i] < 0 && fall2[j] < 0 && x[i] == x[j]) begin d[i] = -d[i]; d[j] = -d[j]; hits++; end
    end
  endfunction

  initial begin
    int pos[], dirs[], t[$], fall2[], hits, n, worst;
    int want[6] = '{25, 60, 75, 90, 60, 10};
    pos = '{10, 25, 40, 60, 75, 90};
    dirs = '{1, -1, 1, -1, -1, 1};
    if (last_fall(pos, dirs) != 90 || collisions(pos, dirs) != 5) begin errors++; $display("example: %0d %0d", last_fall(pos, dirs), collisions(pos, dirs)); end
    fall_times(pos, dirs, 100, t);
    foreach (want[i]) if (t[i] != want[i]) begin errors++; $display("fall_times[%0d] = %0d", i, t[i]); end
    pos = new[100]; dirs = new[100];
    foreach (pos[i]) begin pos[i] = i + 1; dirs[i] = i < 50 ? 1 : -1; end
    if (collisions(pos, dirs) != 2500) begin errors++; $display("2500: %0d", collisions(pos, dirs)); end
    pos[0] = 0;
    if (last_fall(pos, dirs) != 100) begin errors++; $display("100: %0d", last_fall(pos, dirs)); end
    for (int r = 0; r < 300; r++) begin
      n = $urandom_range(1, 12);
      pos = new[n]; dirs = new[n];
      for (int i = 0; i < n; i++) begin                    // distinct positions, ascending
        pos[i] = (i == 0 ? 0 : pos[i - 1] + 1) + $urandom_range(0, 8);
        dirs[i] = $urandom_range(0, 1) ? 1 : -1;
      end
      if (pos[n - 1] > 100) continue;
      simulate(pos, dirs, 100, fall2, hits);
      fall_times(pos, dirs, 100, t);
      worst = 0;
      foreach (fall2[i]) begin
        if (2 * t[i] != fall2[i]) begin errors++; $display("run %0d ant %0d: %0d vs %0d/2", r, i, t[i], fall2[i]); end
        if (fall2[i] > worst) worst = fall2[i];
      end
      if (2 * last_fall(pos, dirs) != worst || collisions(pos, dirs) != hits) begin errors++; $display("run %0d: last or hits", r); end
    end
    // part d: the shift and the first return on the ring, against counts made here
    dirs = '{1, 1, 1, -1, -1, 1};
    if (ring_shift(dirs) != 2 || ring_home(dirs) != 300) begin errors++; $display("ring example: %0d %0d", ring_shift(dirs), ring_home(dirs)); end
    for (int r = 0; r < 200; r++) begin
      int right, s, k;
      n = $urandom_range(1, 9);
      dirs = new[n];
      right = 0;
      foreach (dirs[i]) begin dirs[i] = $urandom_range(0, 1) ? 1 : -1; if (dirs[i] > 0) right++; end
      s = right - (n - right);
      while (s < 0) s += n;
      s = s % n;
      k = 1;
      while ((k * s) % n != 0) k++;
      if (ring_shift(dirs) != s || ring_home(dirs, 100) != 100 * k) begin errors++; $display("ring run %0d", r); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
