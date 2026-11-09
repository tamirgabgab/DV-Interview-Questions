// Question 0085: the page's SystemVerilog. self_describing in base 10 (one number,
// 6210001000), in base 4 (1210 and 2020), and for every base from 2 to 16 against predicted
// (the list of part c) and against a direct count of every number found; the follow-up's
// class self_desc, whose randomize() finds 6210001000 in base 10, 1210 or 2020 in base 4,
// 3211000 in base 7, and fails in base 6.
module tb;
  //@page function automatic int self_describing
  //@page function automatic void predicted
  //@page class self_desc

  int errors = 0;

  // 1 when the string of digits s (0-9, A-F) describes itself
  function automatic bit describes(string s);
    int b = s.len(), v[16], c;
    for (int j = 0; j < b; j++) v[j] = (s[j] >= "A") ? s[j] - "A" + 10 : s[j] - "0";
    for (int k = 0; k < b; k++) begin
      c = 0;
      for (int j = 0; j < b; j++) if (v[j] == k) c++;
      if (c != v[k]) return 0;
    end
    return 1;
  endfunction

  // the digits of a solved self_desc as a string
  function automatic string digits(bit [4:0] d[]);
    string HEX = "0123456789ABCDEF";
    digits = "";
    foreach (d[j]) digits = {digits, HEX.substr(d[j], d[j])};
  endfunction

  task automatic solver();
    self_desc #(10) s10 = new;
    self_desc #(4) s4 = new;
    self_desc #(6) s6 = new;
    self_desc #(7) s7 = new;
    string s;
    repeat (2) begin
      if (!s10.randomize()) begin errors++; $display("solver: base 10 failed"); end
      else if (digits(s10.d) != "6210001000") begin errors++; $display("solver: base 10 gave %s", digits(s10.d)); end
    end
    repeat (4) begin
      if (!s4.randomize()) begin errors++; $display("solver: base 4 failed"); end
      else begin
        s = digits(s4.d);
        if (s != "1210" && s != "2020") begin errors++; $display("solver: base 4 gave %s", s); end
      end
    end
    if (!s7.randomize() || digits(s7.d) != "3211000") begin errors++; $display("solver: base 7"); end
    if (s6.randomize()) begin errors++; $display("solver: base 6 gave %s", digits(s6.d)); end
    $display("solver: %s", digits(s10.d));
  endtask

  initial begin
    string found[$], want[$];
    int n;

    n = self_describing(10, found);
    $display("base 10: %0d: %s", n, n ? found[0] : "-");
    if (n != 1 || found[0] != "6210001000") begin errors++; $display("expected 6210001000 only"); end
    n = self_describing(4, found);
    if (n != 2 || found[0] != "1210" || found[1] != "2020") begin errors++; $display("base 4: expected 1210 and 2020"); end

    for (int b = 2; b <= 16; b++) begin
      n = self_describing(b, found);
      predicted(b, want);
      if (found.size() != want.size()) begin errors++; $display("base %0d: %0d found, %0d predicted", b, found.size(), want.size()); end
      else
        foreach (found[k]) begin
          if (found[k] != want[k]) begin errors++; $display("base %0d: %s found, %s predicted", b, found[k], want[k]); end
          if (!describes(found[k]) || found[k].len() != b) begin errors++; $display("base %0d: %s does not describe itself", b, found[k]); end
        end
      $display("base %2d: %0d", b, n);
    end

    solver();

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
