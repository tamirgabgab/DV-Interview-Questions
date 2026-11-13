// Question 0104: the page's start_naive, start_one_pass, start_at_min and good_starts on the
// page's examples, the edge cases (one station, every d zero, ties at the minimum) and random
// rings, against a reference that drives the lap from every station.
module tb;
  //@page function automatic int start_naive
  //@page function automatic int start_one_pass
  //@page function automatic void good_starts

  int errors = 0;

  function automatic void check(string what, int got, int want);
    if (got != want) begin errors++; $display("%s: %0d, expected %0d", what, got, want); end
  endfunction

  // a full lap from s never runs dry
  function automatic bit lap_ok(int gas[], int cost[], int s);
    int n = gas.size(), tank = 0, i;
    bit ok = 1;
    for (int k = 0; k < n; k++) begin
      i = (s + k) % n;
      tank += gas[i] - cost[i];
      if (tank < 0) ok = 0;
    end
    return ok;
  endfunction

  function automatic void check_ring(string what, int gas[], int cost[]);
    int want_first = -1, got[$], want[$];
    for (int s = gas.size() - 1; s >= 0; s--) if (lap_ok(gas, cost, s)) want_first = s;
    for (int s = 0; s < gas.size(); s++) if (lap_ok(gas, cost, s)) want.push_back(s);
    check({what, " naive"}, start_naive(gas, cost), want_first);
    check({what, " one pass"}, start_one_pass(gas, cost), want_first);
    check({what, " at min"}, start_at_min(gas, cost), want_first);
    good_starts(gas, cost, got);
    check({what, " count"}, got.size(), want.size());
    if (got.size() == want.size()) foreach (got[i]) check($sformatf("%s start %0d", what, i), got[i], want[i]);
  endfunction

  initial begin
    int gas[], cost[], got[$], n;
    // the statement: start 3
    gas = '{1, 2, 3, 4, 5}; cost = '{3, 4, 5, 1, 2};
    check("example", start_one_pass(gas, cost), 3);
    check("example at min", start_at_min(gas, cost), 3);
    check("example naive", start_naive(gas, cost), 3);
    check_ring("example", gas, cost);
    // sum -1: no start
    gas = '{2, 3, 4}; cost = '{3, 4, 3};
    check("none", start_one_pass(gas, cost), -1);
    check_ring("none", gas, cost);
    // sum 0, four good starts
    gas = '{3, 1, 2, 1, 2, 2, 1}; cost = '{1, 3, 1, 2, 2, 1, 2};
    good_starts(gas, cost, got);
    check("zero count", got.size(), 4);
    if (got.size() == 4) begin
      check("zero 0", got[0], 0); check("zero 1", got[1], 2); check("zero 2", got[2], 4); check("zero 3", got[3], 5);
    end
    check_ring("zero", gas, cost);
    // sum 3, starts 1, 3, 4
    gas = '{1, 3, 2, 3, 4}; cost = '{2, 1, 3, 2, 2};
    good_starts(gas, cost, got);
    check("more count", got.size(), 3);
    if (got.size() == 3) begin
      check("more 0", got[0], 1); check("more 1", got[1], 3); check("more 2", got[2], 4);
    end
    check_ring("more", gas, cost);
    // edge cases
    gas = '{1}; cost = '{2}; check_ring("one dry", gas, cost);
    gas = '{2}; cost = '{2}; check_ring("one even", gas, cost);
    gas = '{0, 0, 0}; cost = '{0, 0, 0}; check_ring("zeros", gas, cost);
    gas = '{1, 0}; cost = '{0, 1}; check_ring("tie", gas, cost);
    gas = '{0, 1}; cost = '{1, 0}; check_ring("tie 2", gas, cost);
    // random rings
    for (int r = 0; r < 3000; r++) begin
      n = $urandom_range(9, 1);
      gas = new[n];
      cost = new[n];
      foreach (gas[i]) begin
        gas[i] = $urandom_range(6, 0);
        cost[i] = $urandom_range(6, 0);
      end
      check_ring($sformatf("run %0d", r), gas, cost);
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
