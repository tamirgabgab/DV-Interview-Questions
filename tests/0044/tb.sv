// Question 0044: the page's f (part a) against a digit count on every x in every base from
// 2 to 16 with 1 to 4 digits, and part b's module as published: its hash ends with two keys,
// hash[0] = 10 and hash[495] = 990. The module calls $finish at time 0, so the checks run
// in the final block of tb.
//@page explicit init on every call
//@page module kaprekar_hash

function automatic int by_count(int x, int b, int n);
  int cnt[16], asc, desc;
  // explicit init: Verilator 5.020 kept this array between calls without it
  foreach (cnt[d]) cnt[d] = 0;
  asc = 0;
  desc = 0;
  for (int i = 0; i < n; i++) begin
    cnt[x % b]++;
    x = x / b;
  end
  for (int d = 0; d < b; d++)
    repeat (cnt[d]) asc = asc * b + d;
  for (int d = b - 1; d >= 0; d--)
    repeat (cnt[d]) desc = desc * b + d;
  return desc - asc;
endfunction

module tb;
  kaprekar_hash u();

  final begin
    int errors = 0, top;
    if (f(5, 10, 3) != 495 || f(211, 10, 3) != 99) begin
      $display("FAIL page examples");
      errors++;
    end
    for (int b = 2; b <= 16; b++)
      for (int n = 1; n <= 4; n++) begin
        top = 1;
        repeat (n) top *= b;
        for (int x = 0; x < top; x++)
          if (f(x, b, n) != by_count(x, b, n)) begin
            if (errors < 5) $display("FAIL f(%0d, %0d, %0d) = %0d, expected %0d", x, b, n,
                                     f(x, b, n), by_count(x, b, n));
            errors++;
          end
      end
    if (u.hash.num() != 2 || !u.hash.exists(0) || !u.hash.exists(495) ||
        u.hash[0] != 10 || u.hash[495] != 990) begin
      $display("FAIL hash: %0d keys", u.hash.num());
      errors++;
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
  end
endmodule
