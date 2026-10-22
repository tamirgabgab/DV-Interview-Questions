
module tb;
  //@page function automatic longint unsigned by_enumeration

  //@page function automatic string smallest_01_multiple

  //@page function automatic string smallest_ab_multiple

  // Remainder of a decimal string, so long answers need no big integers.
  function automatic int mod_of(string y, int x);
    int m = 0;
    for (int i = 0; i < y.len(); i++) m = (m * 10 + (y[i] - "0")) % x;
    return m;
  endfunction

  initial begin
    string y;
    int    errors = 0;
    for (int x = 1; x <= 300; x++) begin
      y = smallest_01_multiple(x);
      if (y[0] != "1" || mod_of(y, x) != 0) errors++;
      foreach (y[i]) if (y[i] != "0" && y[i] != "1") errors++;
      // Minimality: the enumeration is minimal by construction (fits 64 bits up to 19 digits)
      if (y.len() <= 18 && $sformatf("%0d", by_enumeration(x)) != y) errors++;
    end
    if (smallest_01_multiple(7) != "1001" || smallest_01_multiple(9999).len() != 36) errors++;

    // Two general digits a < b: the search agrees with the existence theorem, and an answer
    // is a multiple of x over {a, b} with at most x digits that does not start with 0.
    for (int a = 0; a <= 8; a++)
      for (int b = a + 1; b <= 9; b++)
        for (int x = 1; x <= 200; x++) begin
          y = smallest_ab_multiple(x, a, b);
          if ((y != "") != has_ab_solution(x, a, b)) errors++;
          if (y != "") begin
            if (y[0] == "0" || mod_of(y, x) != 0 || y.len() > x) errors++;
            foreach (y[i]) if (y[i] - "0" != a && y[i] - "0" != b) errors++;
          end
          if (a == 0 && b == 1 && y != smallest_01_multiple(x)) errors++;
        end
    if (smallest_ab_multiple(13, 3, 7) != "377" || smallest_ab_multiple(28, 1, 2) != "112" ||
        smallest_ab_multiple(9999, 3, 7) != "333333333333" || smallest_ab_multiple(2, 3, 7) != "") errors++;
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
