//@flags --timing
//@page function automatic bit iban_valid
//@page module iban_checker
//@page function automatic int iban_check_digits
// Question 0099: the page's SystemVerilog against an independent reference (the moved IBAN
// written out as digits, then long division by 97). iban_checker is fed the IBAN a digit a
// clock (every letter as its two digits, now and then an idle clock) and its ok at the last
// digit is checked: the registry examples and the double error of part d pass; made-up IBANs
// built with iban_check_digits pass, and each with one character changed or two neighbours
// swapped fails; random strings with letters agree with the reference. iban_mod97 and
// iban_valid of part a, and iban_check_digits of part c, on the same strings.
module tb;
  logic clk = 0, rst_n = 0, start = 0, valid = 0, last = 0;
  logic [3:0] d = 0;
  logic ok;
  int errors = 0;

  iban_checker dut (.clk, .rst_n, .start, .valid, .last, .d, .ok);
  always #5 clk = ~clk;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // the reference: the first four characters moved to the end, every letter as two digits,
  // then the remainder of that decimal string by long division
  function automatic int ref_mod97(string s);
    string m, dd;
    int r;
    m = {s.substr(4, s.len() - 1), s.substr(0, 3)};
    dd = "";
    for (int i = 0; i < m.len(); i++)
      dd = {dd, (m[i] >= "A") ? $sformatf("%0d", m[i] - "A" + 10) : $sformatf("%c", m[i])};
    r = 0;
    for (int i = 0; i < dd.len(); i++) r = (r * 10 + (dd[i] - "0")) % 97;
    return r;
  endfunction

  // the digits as they arrive: the IBAN as written, every letter as its two digits
  function automatic string as_digits(string s);
    string out = "";
    for (int i = 0; i < s.len(); i++)
      out = {out, (s[i] >= "A") ? $sformatf("%0d", s[i] - "A" + 10) : $sformatf("%c", s[i])};
    return out;
  endfunction

  // feed the checker one digit a clock (an idle clock now and then) and read ok at the last
  task automatic feed(string s, int gap, output bit good);
    string ds = as_digits(s);
    good = 0;
    for (int i = 0; i < ds.len(); i++) begin
      @(negedge clk);
      if (gap > 0 && i % gap == 1) begin valid = 0; start = 0; last = 0; @(negedge clk); end
      valid = 1; start = i == 0; last = i == ds.len() - 1; d = 4'(ds[i] - "0");
      #1;
      if (last) good = ok;
      else if (ok) fail($sformatf("%s: ok before the last digit", s));
    end
    @(negedge clk); valid = 0; start = 0; last = 0;
  endtask

  function automatic string digits_of(int len);
    string s = "";
    for (int i = 0; i < len; i++) s = {s, $sformatf("%0d", $urandom_range(9))};
    return s;
  endfunction

  initial begin
    string ex[$], s, t, alnum;
    int i;
    bit good;
    ex = '{"IL620108000000099999999", "GB82WEST12345698765432", "DE89370400440532013000", "IL620108000000099999902"};
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    #12 rst_n = 1;

    foreach (ex[k]) begin
      feed(ex[k], k, good);
      if (!good || ref_mod97(ex[k]) != 1 || iban_mod97(ex[k]) != 1 || !iban_valid(ex[k])) fail({ex[k], " should be valid"});
    end
    if (iban_check_digits(ex[0]) != 62 || iban_check_digits(ex[1]) != 82 || iban_check_digits(ex[2]) != 89)
      fail("the registry examples' check digits");

    // made-up IBANs: valid as built, and every one with a change or a swap fails
    repeat (60) begin
      s = {"IL00", digits_of(19)};
      s = {"IL", $sformatf("%02d", iban_check_digits(s)), s.substr(4, s.len() - 1)};
      feed(s, 0, good);
      if (!good || ref_mod97(s) != 1) fail($sformatf("%s should be valid", s));
      i = 4 + $urandom_range(s.len() - 5);
      t = s;
      t[i] = 8'("0") + 8'((t[i] - "0" + 1 + $urandom_range(8)) % 10);
      feed(t, 0, good);
      if (good || ref_mod97(t) == 1) fail($sformatf("%s: one character changed, still ok", t));
      i = 4 + $urandom_range(s.len() - 6);
      if (s[i] != s[i + 1]) begin
        t = s;
        t[i] = s[i + 1];
        t[i + 1] = s[i];
        feed(t, 0, good);
        if (good) fail($sformatf("%s: two neighbours swapped, still ok", t));
      end
    end

    // random strings with letters: the checker, the page's functions and the reference agree
    repeat (300) begin
      s = {alnum[10 + $urandom_range(25)], alnum[10 + $urandom_range(25)], digits_of(2)};
      repeat (1 + $urandom_range(29)) s = {s, alnum[$urandom_range(35)]};
      feed(s, $urandom_range(3), good);
      if (good != (ref_mod97(s) == 1) || iban_mod97(s) != ref_mod97(s) || iban_valid(s) != (ref_mod97(s) == 1))
        fail($sformatf("%s: ok %0d, ref %0d", s, good, ref_mod97(s)));
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
