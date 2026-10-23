module tb;
  //@page function automatic bit is_special_4
  //@page function automatic void find_special_4
  //@page function automatic int kaprekar4_step_b

  int errors = 0;

  // Reference: count how many times each digit appears, then build both numbers
  function automatic bit reference(int x);
    int cnt[10] = '{default: 0};
    int largest = 0, smallest = 0;
    cnt[x / 1000]++;
    cnt[(x / 100) % 10]++;
    cnt[(x / 10) % 10]++;
    cnt[x % 10]++;
    for (int v = 9; v >= 0; v--) repeat (cnt[v]) largest = 10 * largest + v;
    for (int v = 0; v <= 9; v++) repeat (cnt[v]) smallest = 10 * smallest + v;
    return largest - smallest == x;
  endfunction

  initial begin
    int special[$];

    if (is_special_4(3524) || is_special_4(95) || is_special_4(1000) || is_special_4(7777)) errors++;
    if (!is_special_4(0) || !is_special_4(6174)) errors++;

    for (int x = 0; x <= 9999; x++)
      if (is_special_4(x) != reference(x)) errors++;

    find_special_4(special);
    if (special.size() != 2 || special[0] != 0 || special[1] != 6174) errors++;

    // the bonus: base B. The step against the base-10 function on every number; in every base from
    // 2 to 16 every number's difference has the digits of the proof, and the fixed points found by
    // running every number are exactly kaprekar4_fixed_b's; the family B = 5k up to 50 by its digits.
    for (int x = 0; x <= 9999; x++)
      if ((kaprekar4_step_b(x, 10) == x) != is_special_4(x)) begin errors++; $display("base 10 step disagrees at %0d", x); end
    for (int B = 2; B <= 16; B++) begin
      int x1, x2, n, y, a, b, c, d, t, p, q, found;   // no initialisers: this is a static block
      int got[$];
      n = kaprekar4_fixed_b(B, x1, x2);
      got.delete();                                    // static too: empty it for every base
      for (int x = 0; x < B * B * B * B; x++) begin
        a = x / (B * B * B); b = (x / (B * B)) % B; c = (x / B) % B; d = x % B;
        if (a < b) begin t = a; a = b; b = t; end
        if (c < d) begin t = c; c = d; d = t; end
        if (a < c) begin t = a; a = c; c = t; end
        if (b < d) begin t = b; b = d; d = t; end
        if (b < c) begin t = b; b = c; c = t; end
        p = a - d; q = b - c;
        y = kaprekar4_step_b(x, B);
        if (y != p * (B * B * B - 1) + q * (B * B - B)) begin errors++; $display("base %0d: step(%0d) = %0d", B, x, y); end
        if (p > 0 && q == 0 && (y / (B * B * B) != p - 1 || (y / (B * B)) % B != B - 1 || (y / B) % B != B - 1 || y % B != B - p)) begin errors++; $display("base %0d: digits of %0d (q = 0)", B, y); end
        if (p > 0 && q > 0 && (y / (B * B * B) != p || (y / (B * B)) % B != q - 1 || (y / B) % B != B - q - 1 || y % B != B - p)) begin errors++; $display("base %0d: digits of %0d", B, y); end
        if (p > 0 && y == x) got.push_back(x);
      end
      found = (got.size() == n);
      if (n >= 1 && (got.size() < 1 || got[0] != x1)) found = 0;
      if (n == 2 && (got.size() < 2 || got[1] != x2)) found = 0;
      if (!found) begin errors++; $display("base %0d: %0d fixed points found, %0d expected", B, got.size(), n); end
    end
    for (int k = 1; k <= 10; k++) begin
      int B, x1, x2, n;
      B = 5 * k;
      n = kaprekar4_fixed_b(B, x1, x2);
      if (n != 1 || kaprekar4_step_b(x1, B) != x1 || x1 / (B * B * B) != 3 * k || (x1 / (B * B)) % B != k - 1 || (x1 / B) % B != 4 * k - 1 || x1 % B != 2 * k) begin
        errors++; $display("family B = %0d: %0d", B, x1);
      end
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
