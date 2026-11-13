// Question 0109: the page's car_fleets and collision_times on the page's examples, the edge
// cases (one car, the same speed, ties at the target, a car absorbed before it is reached) and
// random roads, against references that compare every pair of free lines with exact
// cross-multiplication.
module tb;
  //@page function automatic int car_fleets
  //@page function automatic void collision_times

  int errors = 0;

  function automatic void check(string what, longint got, longint want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // part a: a car starts a new fleet when its time alone is later than the time alone of
  // every car ahead of it (the running maximum, without sorting)
  function automatic int ref_fleets(int target, int position[], int speed[]);
    int count = 0;
    bit later;
    foreach (position[i]) begin
      later = 1;
      foreach (position[j])
        if (position[j] > position[i] &&
            longint'(target - position[i]) * speed[j] <= longint'(target - position[j]) * speed[i]) later = 0;
      if (later) count++;
    end
    return count;
  endfunction

  // part b: car i's collision time is the earliest crossing of its free line with a free line
  // ahead that lies on the lower envelope of the lines ahead at that moment
  function automatic void ref_times(int position[], int speed[], output longint num[], output longint den[]);
    int n = position.size();
    longint a, b;
    bit low;
    num = new[n];
    den = new[n];
    for (int i = 0; i < n; i++)
      for (int j = i + 1; j < n; j++)
        if (speed[i] > speed[j]) begin
          a = position[j] - position[i];                   // t = a / b
          b = speed[i] - speed[j];
          low = 1;                                         // line j lowest at t: p_k + s_k t >= p_j + s_j t
          for (int k = i + 1; k < n; k++)
            if ((position[k] - position[j]) * b + (speed[k] - speed[j]) * a < 0) low = 0;
          if (low && (den[i] == 0 || a * den[i] < num[i] * b)) begin
            num[i] = a;
            den[i] = b;
          end
        end
  endfunction

  function automatic void check_times(string what, int position[], int speed[]);
    longint num[], den[], rn[], rd[];
    collision_times(position, speed, num, den);
    ref_times(position, speed, rn, rd);
    foreach (num[i]) begin
      check($sformatf("%s car %0d none", what, i), den[i] == 0, rd[i] == 0);
      if (den[i] != 0 && rd[i] != 0) check($sformatf("%s car %0d time", what, i), num[i] * rd[i], rn[i] * den[i]);
    end
  endfunction

  initial begin
    int position[], speed[], n, target, pool[$];
    longint num[], den[];
    // part a: the statement, 3 fleets
    position = '{10, 8, 0, 5, 3}; speed = '{2, 4, 1, 1, 3};
    check("example", car_fleets(12, position, speed), 3);
    check("example ref", ref_fleets(12, position, speed), 3);
    position = '{0, 1}; speed = '{3, 1};
    check("half", car_fleets(10, position, speed), 1);
    position = '{0, 2, 6}; speed = '{3, 4, 1};
    check("three", car_fleets(10, position, speed), 1);
    position = '{0, 1}; speed = '{3, 3};
    check("ten thirds", car_fleets(10, position, speed), 2);
    position = '{0}; speed = '{1};
    check("one", car_fleets(5, position, speed), 1);
    position = '{0, 2, 4}; speed = '{2, 2, 2};
    check("same speed", car_fleets(10, position, speed), 3);
    position = '{4, 2, 0}; speed = '{3, 4, 5};
    check("all at the target", car_fleets(10, position, speed), 1);
    // part b: the chain, 2, 1, 3/2, -1
    position = '{3, 5, 6, 9}; speed = '{4, 4, 3, 1};
    collision_times(position, speed, num, den);
    check("chain 0", num[0] * 1, 2 * den[0]);
    check("chain 1", num[1] * 1, 1 * den[1]);
    check("chain 2", num[2] * 2, 3 * den[2]);
    check("chain 3", den[3], 0);
    check_times("chain", position, speed);
    position = '{1, 2, 4, 7}; speed = '{2, 1, 3, 1};
    check_times("leetcode", position, speed);
    position = '{0}; speed = '{1};
    check_times("one", position, speed);
    position = '{0, 1, 2}; speed = '{1, 1, 1};
    check_times("same speed", position, speed);
    // random roads
    for (int r = 0; r < 3000; r++) begin
      n = $urandom_range(8, 1);
      pool.delete();
      for (int v = 0; v < 25; v++) pool.push_back(v);
      pool.shuffle();
      position = new[n];
      speed = new[n];
      foreach (position[i]) begin
        position[i] = pool[i];
        speed[i] = $urandom_range(7, 1);
      end
      target = 24 + $urandom_range(15, 1);
      check($sformatf("run %0d fleets", r), car_fleets(target, position, speed), ref_fleets(target, position, speed));
      position.sort();
      check_times($sformatf("run %0d", r), position, speed);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
