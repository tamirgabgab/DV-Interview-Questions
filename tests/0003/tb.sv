// Simulator limitation (Verilator 5.020): cannot inline a function whose `ref` arguments are queue elements.
// The translation below is the page code plus a pragma that disables inlining.
//@translation-of function automatic void swap( 070a229b977e

module tb;
  function automatic void swap(ref int x, ref int y);
    /*verilator no_inline_task*/
    int t = x;
    x = y;
    y = t;
  endfunction

  function automatic void mystery(ref int A[$]);
    int n = A.size();
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        if (A[i] < A[j])
          swap(A[i], A[j]);
  endfunction

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
      // Built-in sort() is not used: Verilator 5.020 sorts signed ints as unsigned.
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
