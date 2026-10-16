module tb;
  //@page function automatic bit is_special
  //@page function automatic void find_special

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

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
