
module tb;
  //@page function automatic void swap(

  initial begin
    int a[$], expected[$];
    int errors = 0;
    int count[int];                // multiset of the input values
    a = '{3, 1, 4, 2};
    expected = '{1, 2, 3, 4};
    mystery(a);
    if (a != expected) errors++;
    // the corner cases of the verification follow-up, with their sorted results written out
    begin
      int corner[$][$] = '{'{}, '{7}, '{5, 5, 5, 5}, '{1, 2, 3, 4, 5}, '{5, 4, 3, 2, 1}, '{-3, 0, -3, 2, -8}};
      int sorted[$][$] = '{'{}, '{7}, '{5, 5, 5, 5}, '{1, 2, 3, 4, 5}, '{1, 2, 3, 4, 5}, '{-8, -3, -3, 0, 2}};
      foreach (corner[c]) begin
        a = corner[c];
        mystery(a);
        if (a != sorted[c]) begin errors++; $display("corner %0d: %p -> %p", c, corner[c], a); end
      end
    end
    repeat (500) begin
      a.delete();
      repeat ($urandom_range(0, 12)) a.push_back(int'($urandom_range(0, 40)) - 20);
      // The order is checked pairwise and the values as a multiset (sort() is not needed).
      count.delete();
      foreach (a[i]) count[a[i]]++;
      mystery(a);
      for (int i = 1; i < a.size(); i++) if (a[i-1] > a[i]) errors++;   // ascending
      foreach (a[i]) count[a[i]]--;                                     // same values
      foreach (count[v]) if (count[v] != 0) errors++;
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
