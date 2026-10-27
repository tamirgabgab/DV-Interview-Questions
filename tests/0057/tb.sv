//@flags --timing
// Question 0057: the page's tag_xor, tag_xor2 and tag_sums (W = 5, 32 tags) on random runs:
// requests 0..31 in order, the responses shuffled and each one sent once its request is out
// (a request and a response often in the same cycle), with one tag dropped, two dropped, or
// one dropped and one doubled; then the page's missing_k on queues with up to four dropped.
//@page module tag_xor #
//@page module tag_xor2 #
//@page module tag_sums
//@page function automatic void missing_k

module tb;
  localparam int W = 5, N = 1 << W;
  logic clk = 0, rst_n = 0;
  always #5 clk = ~clk;
  logic req_valid = 0, rsp_valid = 0;
  logic [W-1:0] req_tag = '0, rsp_tag = '0;
  logic [W-1:0] miss1, miss_a, miss_b, miss, dup;
  int out;
  int errors = 0;

  tag_xor  #(.W(W)) u1 (.clk, .rst_n, .req_valid, .req_tag, .rsp_valid, .rsp_tag, .missing(miss1), .out);
  tag_xor2 #(.W(W)) u2 (.clk, .rst_n, .req_valid, .req_tag, .rsp_valid, .rsp_tag, .miss_a, .miss_b);
  tag_sums #(.W(W)) u3 (.clk, .rst_n, .req_valid, .req_tag, .rsp_valid, .rsp_tag, .miss, .dup);

  // one run: every tag requested once; the responses are ret[] (shuffled here)
  task automatic drive(int ret[$]);
    int next = 0;
    ret.shuffle();
    @(negedge clk); rst_n = 0; #1 rst_n = 1;
    while (next < N || ret.size() > 0) begin
      @(negedge clk);
      req_valid = next < N;
      req_tag = W'(next);
      // the first response whose request is already out (or goes out this cycle)
      rsp_valid = 0;
      foreach (ret[i]) if (ret[i] <= next && $urandom_range(0, 2) != 0) begin
        rsp_valid = 1; rsp_tag = W'(ret[i]); ret.delete(i); break;
      end
      if (next < N) next++;
    end
    @(negedge clk); req_valid = 0; rsp_valid = 0;
    @(negedge clk);
  endtask

  initial begin
    int ret[$], sent[$], got[$], a, b, k;
    int drop[$];
    repeat (2) @(posedge clk);
    for (int r = 0; r < 60; r++) begin
      a = $urandom_range(0, N - 1);
      do b = $urandom_range(0, N - 1); while (b == a);
      // one missing
      ret = {}; for (int t = 0; t < N; t++) if (t != a) ret.push_back(t);
      drive(ret);
      if (out != 1 || miss1 != W'(a)) begin errors++; $display("one: out %0d tag %0d, want %0d", out, miss1, a); end
      // two missing
      ret = {}; for (int t = 0; t < N; t++) if (t != a && t != b) ret.push_back(t);
      drive(ret);
      if (out != 2 || !((miss_a == W'(a) && miss_b == W'(b)) || (miss_a == W'(b) && miss_b == W'(a)))) begin
        errors++; $display("two: %0d %0d, want %0d %0d", miss_a, miss_b, a, b);
      end
      // one missing, one twice
      ret = {}; for (int t = 0; t < N; t++) if (t != a) ret.push_back(t);
      ret.push_back(b);
      drive(ret);
      if (out != 0 || miss != W'(a) || dup != W'(b)) begin errors++; $display("sums: %0d %0d, want %0d %0d", miss, dup, a, b); end
    end
    // k missing, on queues
    for (int r = 0; r < 200; r++) begin
      k = $urandom_range(1, 4);
      drop = {};
      while (drop.size() < k) begin a = $urandom_range(0, N - 1); if (!(a inside {drop})) drop.push_back(a); end
      sent = {}; ret = {};
      for (int t = 0; t < N; t++) begin sent.push_back(t); if (!(t inside {drop})) ret.push_back(t); end
      ret.shuffle();
      missing_k(sent, ret, k, N, got);
      drop.sort();
      if (got.size() != k) begin errors++; $display("k=%0d: %0d found", k, got.size()); end
      else foreach (got[i]) if (got[i] != drop[i]) begin errors++; $display("k=%0d: %0d vs %0d", k, got[i], drop[i]); end
    end
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
