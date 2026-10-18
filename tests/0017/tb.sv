module tb;
  //@page function automatic int find_duplicate_sort(
  //@page function automatic int find_duplicate_seen(
  //@page function automatic int find_duplicate_binary(
  //@page function automatic int find_duplicate_floyd(

  int errors = 0;

  function automatic int count_of(const ref int nums[], int v);
    int c;
    c = 0;
    foreach (nums[i]) if (nums[i] == v) c++;
    return c;
  endfunction

  // n + 1 values in 1..n: random, or one value repeated many times
  function automatic void random_case(ref int nums[], input int n);
    int v;
    nums = new[n + 1];
    if ($urandom_range(1, 0)) begin
      foreach (nums[i]) nums[i] = $urandom_range(n, 1);
    end else begin
      v = $urandom_range(n, 1);
      for (int i = 0; i < n; i++) nums[i] = ($urandom_range(2, 0) == 0) ? v : i + 1;
      nums[n] = v;
      nums.shuffle();
    end
  endfunction

  initial begin
    int nums[];
    int copy[];
    int r[4];
    nums = '{3, 9, 5, 6, 7, 8, 1, 1, 2, 4};
    if (find_duplicate_sort(nums) != 1 || find_duplicate_seen(nums) != 1 ||
        find_duplicate_binary(nums) != 1 || find_duplicate_floyd(nums) != 1) errors++;

    repeat (3000) begin
      random_case(nums, $urandom_range(60, 1));
      copy = nums;
      r[0] = find_duplicate_sort(nums);
      r[1] = find_duplicate_seen(nums);
      r[2] = find_duplicate_binary(nums);
      r[3] = find_duplicate_floyd(nums);
      foreach (r[j]) if (r[j] < 1 || r[j] >= nums.size() || count_of(nums, r[j]) < 2) errors++;
      if (nums != copy) errors++;          // const ref: the input is never changed
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
