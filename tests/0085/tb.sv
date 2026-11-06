// Question 0085: the page's SystemVerilog. self_describing in base 10 (one number,
// 6210001000), in base 4 (1210 and 2020), and for every base from 2 to 16 against predicted
// (the list of part c) and against a direct count of every number found.
module tb;
  //@page function automatic int self_describing
  //@page function automatic void predicted

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

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
