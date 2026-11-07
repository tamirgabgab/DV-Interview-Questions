//@flags --timing
//@page module iban_check
//@page function automatic int iban_check_digits
//@page function automatic string israeli_iban
// Question 0099: the page's SystemVerilog. iban_check fed one character a clock against an
// independent reference (the moved IBAN written out as digits, then long division by 97):
// the registry examples and the double error of part c pass; made-up Israeli IBANs from
// israeli_iban pass, and every one of them with one character changed or two neighbours
// swapped fails; random strings with letters give the same remainder as the reference.
// iban_check_digits gives the registry examples' check digits.
module tb;
  logic clk = 0, rst_n = 0, valid = 0, first = 0, last = 0;
  logic [7:0] ch = 0;
  logic done, ok;
  logic [6:0] rem;
  int errors = 0;

  iban_check dut (.clk, .rst_n, .valid, .first, .last, .ch, .done, .ok, .rem);
  always #5 clk = ~clk;

  task automatic fail(string what);
    errors++;
    if (errors < 20) $display("%s", what);
  endtask

  // the reference: the first four characters moved to the end, every letter as two digits,
  // then the remainder of that decimal string by long division
  function automatic int ref_mod97(string s);
    string m, d;
    int r;
    m = {s.substr(4, s.len() - 1), s.substr(0, 3)};
    d = "";
    for (int i = 0; i < m.len(); i++)
      d = {d, (m[i] >= "A") ? $sformatf("%0d", m[i] - "A" + 10) : $sformatf("%c", m[i])};
    r = 0;
    for (int i = 0; i < d.len(); i++) r = (r * 10 + (d[i] - "0")) % 97;
    return r;
  endfunction

  // feed the module one character a clock (now and then with an idle clock between two)
  task automatic feed(string s, int gap, output int r, output bit good);
    for (int i = 0; i < s.len(); i++) begin
      @(negedge clk);
      valid = 1; first = i == 0; last = i == s.len() - 1; ch = s[i];
      if (gap > 0 && i % gap == 1) begin @(negedge clk); valid = 0; first = 0; last = 0; end
    end
    @(negedge clk); valid = 0; first = 0; last = 0;
    // done comes one clock after the clock that took the last character
    if (!(gap > 0 && (s.len() - 1) % gap == 1)) @(posedge clk);
    #1;
    if (!done) fail($sformatf("%s: no done", s));
    r = int'(rem);
    good = ok;
    @(posedge clk); #1;
    if (done) fail($sformatf("%s: done for two clocks", s));
  endtask

  function automatic string digits_of(int n, int len);
    string s = "";
    for (int i = 0; i < len; i++) s = {s, $sformatf("%0d", $urandom_range(9))};
    return s;
  endfunction

  initial begin
    string ex[$], s, t, alnum;
    int r, i;
    bit good;
    longint acct;
    ex = '{"IL620108000000099999999", "GB82WEST12345698765432", "DE89370400440532013000", "IL620108000000099999902"};
    alnum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    #12 rst_n = 1;

    foreach (ex[k]) begin
      feed(ex[k], k, r, good);
      if (!good || r != 1 || ref_mod97(ex[k]) != 1 || iban_mod97(ex[k]) != 1) fail($sformatf("%s: rem %0d", ex[k], r));
    end
    if (iban_check_digits(ex[0]) != 62 || iban_check_digits(ex[1]) != 82 || iban_check_digits(ex[2]) != 89)
      fail("the registry examples' check digits");
    if (israeli_iban(12, 345, 6789012) != "IL140123450000006789012") fail({"israeli_iban: ", israeli_iban(12, 345, 6789012)});
    if (israeli_iban(10, 800, 99999999) != "IL620108000000099999999") fail("israeli_iban of the registry example");

    // made-up Israeli IBANs: valid as built, and every single change / neighbour swap fails
    repeat (60) begin
      acct = {$urandom, $urandom} % 64'd10000000000000;
      s = israeli_iban($urandom_range(999), $urandom_range(999), acct);
      feed(s, 0, r, good);
      if (!good || ref_mod97(s) != 1) fail($sformatf("%s should be valid", s));
      i = 2 + $urandom_range(s.len() - 3);
      t = s;
      t[i] = 8'("0") + 8'((t[i] - "0" + 1 + $urandom_range(8)) % 10);
      feed(t, 0, r, good);
      if (good || r != ref_mod97(t)) fail($sformatf("%s: one character changed, rem %0d", t, r));
      i = 2 + $urandom_range(s.len() - 4);
      if (s[i] != s[i + 1]) begin
        t = s;
        t[i] = s[i + 1];
        t[i + 1] = s[i];
        feed(t, 0, r, good);
        if (good || r != ref_mod97(t)) fail($sformatf("%s: two neighbours swapped, rem %0d", t, r));
      end
    end

    // random strings with letters: the module, the page's function and the reference agree
    repeat (200) begin
      s = {alnum[10 + $urandom_range(25)], alnum[10 + $urandom_range(25)], digits_of(0, 2)};
      repeat (1 + $urandom_range(29)) s = {s, alnum[$urandom_range(35)]};
      feed(s, $urandom_range(3), r, good);
      if (r != ref_mod97(s) || r != iban_mod97(s) || good != (r == 1)) fail($sformatf("%s: rem %0d, ref %0d", s, r, ref_mod97(s)));
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
