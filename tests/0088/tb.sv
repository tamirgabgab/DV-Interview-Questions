// Question 0088: the page's SystemVerilog. ducci_step and steps_to_zero on every start of 4
// numbers below 6 against a step written here, always_zero for n from 2 to 64 against the
// power-of-2 test, and ducci_orbit on every start of 3 and of 5 numbers below 4 against a
// search written here (the round each state is first seen). The numbers of the page: 2, 6,
// 11, 4 in 6 rounds; 0, 7, 20, 44 in 13; 0, 0, 1 and 1, 2, 3 cycles of 3; 1 to 5 a cycle
// of 15 after 2 rounds.
module tb;
  //@page function automatic void ducci_step
  //@page function automatic longint unsigned parity_step
  //@page function automatic int ducci_orbit

  int errors = 0;

  // the reference: one round into a new queue
  function automatic void ref_step(int v[$], output int w[$]);
    w = {};
    foreach (v[i]) w.push_back((v[i] > v[(i + 1) % v.size()]) ? v[i] - v[(i + 1) % v.size()] : v[(i + 1) % v.size()] - v[i]);
  endfunction

  function automatic string key_of(int v[$]);
    string k = "";
    foreach (v[i]) k = {k, $sformatf("%0d.", v[i])};
    return k;
  endfunction

  // the reference orbit: (tail, period) by a list of the states seen
  function automatic void ref_orbit(int v0[$], output int tail, output int period);
    string keys[$];
    int v[$], w[$], found;
    v = v0;
    while (1) begin
      found = -1;
      foreach (keys[i]) if (keys[i] == key_of(v)) found = i;
      if (found >= 0) begin tail = found; period = keys.size() - found; return; end
      keys.push_back(key_of(v));
      ref_step(v, w);
      v = w;
    end
  endfunction

  function automatic int ref_steps(int v0[$]);
    int t, p;
    ref_orbit(v0, t, p);
    return t;   // for 4 numbers the cycle is all zeros
  endfunction

  initial begin
    int v[$], w[$], u[$], got, tail, rt, rp;

    // ducci_step and steps_to_zero, every start of 4 numbers below 6
    for (int a = 0; a < 6; a++) for (int b = 0; b < 6; b++) for (int c = 0; c < 6; c++) for (int d = 0; d < 6; d++) begin
      v = '{a, b, c, d};
      u = v;
      ducci_step(u);
      ref_step(v, w);
      if (u != w) begin errors++; $display("step %0d %0d %0d %0d", a, b, c, d); end
      if (steps_to_zero(v) != ref_steps(v)) begin errors++; $display("steps_to_zero %0d %0d %0d %0d", a, b, c, d); end
    end
    v = '{2, 6, 11, 4};
    if (steps_to_zero(v) != 6) begin errors++; $display("2, 6, 11, 4: %0d", steps_to_zero(v)); end
    v = '{0, 7, 20, 44};
    if (steps_to_zero(v) != 13) begin errors++; $display("0, 7, 20, 44: %0d", steps_to_zero(v)); end

    // always_zero: exactly the powers of 2
    for (int n = 2; n <= 64; n++)
      if (always_zero(n) != ((n & (n - 1)) == 0)) begin errors++; $display("always_zero %0d", n); end

    // ducci_orbit, every start of 3 and of 5 numbers below 4
    for (int x = 0; x < 64; x++) begin
      v = '{x % 4, (x / 4) % 4, x / 16};
      got = ducci_orbit(v, tail);
      ref_orbit(v, rt, rp);
      if (got != rp || tail != rt) begin errors++; $display("orbit3 %0d", x); end
    end
    for (int x = 0; x < 1024; x++) begin
      v = '{x % 4, (x / 4) % 4, (x / 16) % 4, (x / 64) % 4, x / 256};
      got = ducci_orbit(v, tail);
      ref_orbit(v, rt, rp);
      if (got != rp || tail != rt) begin errors++; $display("orbit5 %0d", x); end
    end
    v = '{0, 0, 1};
    got = ducci_orbit(v, tail);
    if (got != 3 || tail != 1) begin errors++; $display("0, 0, 1: %0d after %0d", got, tail); end
    v = '{1, 2, 3, 4, 5};
    got = ducci_orbit(v, tail);
    $display("1 to 5: a cycle of %0d after %0d rounds", got, tail);
    if (got != 15 || tail != 2) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
