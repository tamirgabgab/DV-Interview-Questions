// Question 0016: part c's josephus_chain and josephus_closed, as published, against a
// direct simulation of the circle (one stays, L - 1 leave) for every N up to 200 and L
// from 2 to 6.
//@page the recurrence, along N's chain only

function automatic int simulate(int n, int L);
  int people[$];
  int i;
  people.delete();
  for (int k = 0; k < n; k++) people.push_back(k);
  i = 0;
  while (people.size() > 1) begin
    for (int t = 0; t < L - 1 && people.size() > 1; t++) begin
      int j = (i + 1) % people.size();
      people.delete(j);
      if (j < i) i--;
    end
    i = (i + 1) % people.size();
  end
  return people[0];
endfunction

module tb;
  initial begin
    int errors = 0;
    for (int L = 2; L <= 6; L++)
      for (int n = 1; n <= 200; n++)
        if (josephus_chain(n, L) != simulate(n, L) || josephus_closed(n, L) != simulate(n, L)) begin
          if (errors < 5) $display("FAIL n=%0d L=%0d: chain %0d closed %0d sim %0d", n, L,
                                   josephus_chain(n, L), josephus_closed(n, L), simulate(n, L));
          errors++;
        end
    if (josephus_closed(20, 2) != 8 || josephus_closed(30, 3) != 18 || josephus_closed(20, 4) != 16) begin
      $display("FAIL page examples");
      errors++;
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
