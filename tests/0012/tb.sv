module tb;
  //@page function automatic bit is_special
  //@page function automatic void find_special
  //@page function automatic int kaprekar_step_b

  int errors = 0;

  // Reference: count how many times each digit appears, then build both numbers
  function automatic bit reference(int x);
    int cnt[10] = '{default: 0};
    int largest = 0, smallest = 0;
    cnt[x / 100]++;
    cnt[(x / 10) % 10]++;
    cnt[x % 10]++;
    for (int v = 9; v >= 0; v--) repeat (cnt[v]) largest = 10 * largest + v;
    for (int v = 0; v <= 9; v++) repeat (cnt[v]) smallest = 10 * smallest + v;
    return largest - smallest == x;
  endfunction

  initial begin
    int special[$];

    if (is_special(352) || is_special(7) || is_special(45) || is_special(111)) errors++;
    if (!is_special(0) || !is_special(495)) errors++;

    for (int x = 0; x <= 999; x++)
      if (is_special(x) != reference(x)) errors++;

    find_special(special);
    if (special.size() != 2 || special[0] != 0 || special[1] != 495) errors++;

    // part c: base b. The step against the base-10 function, the attractor of every base from 2 to
    // 16 (a fixed point, or a 2-cycle, that every number with two different digits reaches), the
    // digits of the result (d - 1, b - 1, b - d), and the base-7 example 610 -> 561 -> 462 -> 363.
    for (int x = 0; x <= 999; x++)
      if ((kaprekar_step_b(x, 10) == x) != is_special(x)) begin errors++; $display("base 10 step disagrees at %0d", x); end
    for (int b = 2; b <= 16; b++) begin
      int x1, x2, n, y, d, lo, mid, hi, v;   // no initializers: in a static block they would run only once
      n = kaprekar_attractor_b(b, x1, x2);
      if (n == 1 && kaprekar_step_b(x1, b) != x1) begin errors++; $display("base %0d: %0d is not a fixed point", b, x1); end
      if (n == 2 && (kaprekar_step_b(x1, b) != x2 || kaprekar_step_b(x2, b) != x1)) begin errors++; $display("base %0d: %0d <-> %0d is not a cycle", b, x1, x2); end
      for (int x = 0; x < b * b * b; x++) begin
        lo = x / (b * b); mid = (x / b) % b; hi = x % b;
        if (lo > mid) begin v = lo; lo = mid; mid = v; end
        if (mid > hi) begin v = mid; mid = hi; hi = v; end
        if (lo > mid) begin v = lo; lo = mid; mid = v; end
        d = hi - lo;
        y = kaprekar_step_b(x, b);
        if (y != d * (b * b - 1)) begin errors++; $display("base %0d: step(%0d) = %0d, expected %0d", b, x, y, d * (b * b - 1)); end
        if (d > 0 && (y / (b * b) != d - 1 || (y / b) % b != b - 1 || y % b != b - d)) begin errors++; $display("base %0d: digits of %0d wrong", b, y); end
        v = x;
        for (int i = 0; i < 40 && v != 0 && v != x1 && !(n == 2 && v == x2); i++) v = kaprekar_step_b(v, b);
        if (!(v == 0 || v == x1 || (n == 2 && v == x2))) begin errors++; $display("base %0d: %0d does not reach the attractor", b, x); end
        if (v == 0 && d != 0) begin errors++; $display("base %0d: %0d fell to 0 with d = %0d", b, x, d); end
      end
    end
    if (kaprekar_step_b(301, 7) != 288 || kaprekar_step_b(288, 7) != 240 || kaprekar_step_b(240, 7) != 192 || kaprekar_step_b(192, 7) != 144 || kaprekar_step_b(144, 7) != 192) begin
      errors++; $display("base 7 example wrong");
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
