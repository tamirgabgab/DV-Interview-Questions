module tb;
  //@page function automatic string remove_pair
  //@page function automatic bit is_valid(

  int errors = 0;

  // Reference: count the strings of length <= 6 and compare both solutions on all of them
  function automatic string from_digits(int code, int n);
    string chars = "()[]{}";
    string s = "";
    repeat (n) begin
      s = {s, chars.substr(code % 6, code % 6)};
      code /= 6;
    end
    return s;
  endfunction

  initial begin
    string valid[$]   = '{"", "()", "()[]{}", "{[()]}", "([]{})", "(((())))"};
    string invalid[$] = '{"(]", "([)]", "(((", "())", ")(", "]", "(("};
    int    total, n_valid;
    string s;

    foreach (valid[i])   if (!is_valid(valid[i]) || !is_valid_brute(valid[i])) errors++;
    foreach (invalid[i]) if (is_valid(invalid[i]) || is_valid_brute(invalid[i])) errors++;

    // All strings up to length 6: both solutions agree, and the number of valid ones
    // matches 3^k * Catalan(k) for length 2k (1, 3, 18, 135 for k = 0..3)
    for (int n = 0; n <= 6; n++) begin
      total = 1;
      repeat (n) total *= 6;
      n_valid = 0;
      for (int code = 0; code < total; code++) begin
        s = from_digits(code, n);
        if (is_valid(s) != is_valid_brute(s)) errors++;
        n_valid += is_valid(s);
      end
      if (n_valid != ((n == 0) ? 1 : (n == 2) ? 3 : (n == 4) ? 18 : (n == 6) ? 135 : 0)) errors++;
    end

    // Deep nesting: 200 times "(" then 200 times ")"
    s = "";
    repeat (200) s = {"(", s, ")"};
    if (!is_valid(s) || !is_valid_brute(s)) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
