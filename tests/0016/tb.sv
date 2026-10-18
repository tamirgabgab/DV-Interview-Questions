module tb;
  //@page function automatic int josephus_sim(
  //@page function automatic int josephus_formula(
  //@page function automatic int josephus_sim_k(

  int errors = 0;

  // Independent reference: a dynamic array and an index, every k-th leaves
  function automatic int reference(int n, int k);
    int people[$];
    int i;
    for (int p = 1; p <= n; p++) people.push_back(p);
    i = 0;
    while (people.size() > 1) begin
      i = (i + k - 1) % people.size();
      people.delete(i);
    end
    return people[0];
  endfunction

  initial begin
    if (josephus_sim(5) != 3 || josephus_sim(10) != 5 || josephus_formula(41) != 19) errors++;
    if (josephus_k(41, 3) != 31 || josephus_sim_k(41, 3) != 31 || josephus_k(7, 3) != 4) errors++;

    for (int n = 1; n <= 1024; n++) begin
      if (josephus_sim(n) != reference(n, 2)) errors++;
      if (josephus_formula(n) != josephus_sim(n) || josephus_bits(n) != josephus_sim(n)) errors++;
    end
    for (int n = 1; n <= 80; n++)
      for (int k = 1; k <= 9; k++)
        if (josephus_sim_k(n, k) != reference(n, k) || josephus_k(n, k) != reference(n, k)) errors++;
    // Large n: the formula needs no simulation; a power of 2 always gives 1
    if (josephus_formula(1 << 30) != 1 || josephus_bits((1 << 30) + 5) != 11) errors++;

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
