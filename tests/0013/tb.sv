module tb;
  //@page function automatic bit is_special_4
  //@page function automatic void find_special_4

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

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
