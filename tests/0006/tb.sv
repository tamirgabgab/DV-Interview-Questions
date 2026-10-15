module tb;
  //@page typedef struct
  //@page function automatic trade_t max_long_fast
  //@page function automatic trade_t max_profit_brute
  //@page function automatic trade_t max_profit_fast

  int errors = 0;

  function automatic void check_trade(int prices[$], trade_t t);
    int gain;
    if (t.kind == "") begin
      if (t.profit != 0 || t.open_i != -1 || t.close_i != -1) errors++;
      return;
    end
    gain = prices[t.close_i] - prices[t.open_i];
    if (t.open_i >= t.close_i || t.profit <= 0) errors++;
    if (t.profit != ((t.kind == "long") ? gain : -gain)) errors++;
  endfunction

  initial begin
    int     prices[$];
    trade_t brute, fast;
    prices = '{5, 8, 3, 9, 2, 6};
    fast = max_profit_fast(prices);
    if (fast.profit != 7 || fast.kind != "short" || fast.open_i != 3 || fast.close_i != 4) errors++;
    if (max_long_fast(prices).profit != 6) errors++;

    repeat (3000) begin
      prices.delete();
      repeat ($urandom_range(0, 10)) prices.push_back($urandom_range(1, 20));
      brute = max_profit_brute(prices);
      fast  = max_profit_fast(prices);
      if (brute.profit != fast.profit) errors++;
      check_trade(prices, brute);
      check_trade(prices, fast);
      if (max_long_brute(prices).profit != max_long_fast(prices).profit) errors++;
    end
    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
