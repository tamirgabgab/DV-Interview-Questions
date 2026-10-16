
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
