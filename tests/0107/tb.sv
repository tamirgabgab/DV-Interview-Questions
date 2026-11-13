// Question 0107: the page's largest_number, largest_brute and smallest_number on the page's
// examples, the edge cases (all zeros, one number, equal numbers, 12 and 1212, numbers past
// 32 bits of result) and random lists, against a brute force over every order written here.
module tb;
  //@page function automatic bit goes_first
  //@page function automatic void try_orders
  //@page function automatic string smallest_number

  int errors = 0;

  function automatic void check(string what, string got, string want);
    if (got != want) begin errors++; $display("%s: %s, expected %s", what, got, want); end
  endfunction

  // every order from position k on; the smallest concatenation that does not start with 0
  function automatic void small_orders(ref string s[$], input int k, ref string best);
    string t, cand = "";
    if (k == s.size()) begin
      foreach (s[i]) cand = {cand, s[i]};
      if (cand[0] != "0" && (best == "" || cand < best)) best = cand;
      return;
    end
    for (int i = k; i < s.size(); i++) begin
      t = s[k]; s[k] = s[i]; s[i] = t;
      small_orders(s, k + 1, best);
      t = s[k]; s[k] = s[i]; s[i] = t;
    end
  endfunction

  function automatic string smallest_ref(int nums[]);
    string s[$], best = "";
    foreach (nums[i]) s.push_back($sformatf("%0d", nums[i]));
    small_orders(s, 0, best);
    return best == "" ? "0" : best;
  endfunction

  function automatic void check_list(string what, int nums[]);
    string big = largest_brute(nums);
    check({what, " largest"}, largest_number(nums), big);
    check({what, " smallest"}, smallest_number(nums), smallest_ref(nums));
  endfunction

  initial begin
    int nums[], pool[] = '{0, 1, 2, 3, 9, 10, 11, 12, 20, 21, 30, 34, 100, 101, 110, 121, 1001, 1010, 1212, 2121, 99, 98, 989};
    int n;
    void'($urandom(107));
    // the statement and part a
    nums = '{3, 30, 34, 5, 9};
    check("example", largest_number(nums), "9534330");
    check("example brute", largest_brute(nums), "9534330");
    check("example smallest", smallest_number(nums), "3033459");
    check_list("example", nums);
    nums = '{3, 30};        check("3 30", largest_number(nums), "330");
    nums = '{12, 1212};     check("12 1212", largest_number(nums), "121212"); check("12 1212 min", smallest_number(nums), "121212");
    nums = '{1212, 12};     check("1212 12", largest_number(nums), "121212");
    nums = '{0, 0};         check("0 0", largest_number(nums), "0"); check("0 0 brute", largest_brute(nums), "0"); check("0 0 min", smallest_number(nums), "0");
    nums = '{0};            check("0", largest_number(nums), "0"); check("0 min", smallest_number(nums), "0");
    nums = '{7};            check("7", largest_number(nums), "7"); check("7 min", smallest_number(nums), "7");
    nums = '{5, 5, 5};      check("555", largest_number(nums), "555"); check("555 min", smallest_number(nums), "555");
    nums = '{10, 2};        check("10 2", largest_number(nums), "210"); check("10 2 min", smallest_number(nums), "102");
    nums = '{2147483647, 2147483646}; check("int max", largest_number(nums), "21474836472147483646");
    // part c: the lead's cases, the shortcut's failure, the tie
    nums = '{0, 1, 10};     check("0 1 10", smallest_number(nums), "1001");
    nums = '{0, 0, 1};      check("0 0 1", smallest_number(nums), "100");
    nums = '{20, 1, 0};     check("20 1 0", smallest_number(nums), "1020");
    nums = '{0, 2, 21};     check("0 2 21", smallest_number(nums), "2021");
    nums = '{0, 11, 1};     check("0 11 1", smallest_number(nums), "1011");
    nums = '{0, 0, 0, 5};   check("5000", smallest_number(nums), "5000");
    // random lists against the brute force
    for (int t = 0; t < 400; t++) begin
      n = 1 + $urandom_range(5);
      nums = new[n];
      foreach (nums[i]) nums[i] = $urandom_range(9) < 7 ? pool[$urandom_range(pool.size() - 1)] : $urandom_range(2000);
      check_list($sformatf("random %0d", t), nums);
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
