// Question 0053: the page's covergroup in the simulator. get_inst_coverage() after one
// sample (24.2778 %), after a sweep of every op and value class (100 %: the ignored cells
// do not count), and on random transactions against a reference written here from the
// definitions of the bins; and the page's expected_closure against the exact values of
// the generator (inclusion-exclusion with fractions, tests/0053 checks the constants).
module tb;
  //@page typedef enum logic [2:0] {ADD
  //@page function automatic real expected_closure

  localparam real UNIFORM = 1393800.98300;
  localparam real DIST = 533.73978;
  localparam real EQUAL = 388.86481;

  int errors = 0;

  task automatic near(string what, real got, real want, real tol);
    if (got < want - tol || got > want + tol) begin errors++; $display("%s: got %f, expected %f", what, got, want); end
  endtask

  // the reference: which bin a value is in, and the hits of every item
  function automatic int vbin(logic [7:0] v);
    return v == 8'h00 ? 0 : v == 8'hFF ? 1 : v == 8'h80 ? 2 : 3;
  endfunction

  function automatic void cells(real pz, real pm, real ps, real pmid, ref real p[$]);
    real pv[4] = '{pz, pm, ps, pmid};
    p = {};
    for (int o = 0; o < 5; o++) for (int x = 0; x < 4; x++) for (int y = 0; y < 4; y++)
      if (!(o == 4 && (y == 1 || y == 2))) p.push_back(pv[x] * pv[y] / 5.0);
  endfunction

  initial begin
    alu_cg cg;
    bit h_op[5], h_a[4], h_b[4], h_c[2], h_x[5][4][4];
    real ref_cov, p[$];
    alu_op_e op;
    logic [7:0] a, b;
    logic c;
    int n, s_op, s_a, s_b, s_c, s_x;                      // initializers in the loop would run once (static)
    cg = new;
    cg.sample(ADD, 8'h00, 8'h00, 1'b0);
    near("one sample", cg.get_inst_coverage(), (20.0 + 25.0 + 25.0 + 50.0 + 100.0 / 72.0) / 5.0, 1e-4);
    for (int o = 0; o < 5; o++) foreach (h_a[i]) foreach (h_b[j]) begin
      logic [7:0] vals[4] = '{8'h00, 8'hFF, 8'h80, 8'h07};
      cg.sample(alu_op_e'(o), vals[i], vals[j], logic'((i + j) % 2));
    end
    near("full sweep", cg.get_inst_coverage(), 100.0, 1e-4);
    void'($urandom(53));
    for (int run = 0; run < 30; run++) begin
      cg = new;
      h_op = '{default: 0}; h_a = '{default: 0}; h_b = '{default: 0}; h_c = '{default: 0}; h_x = '{default: '{default: '{default: 0}}};
      n = $urandom_range(1, 80);
      for (int k = 0; k < n; k++) begin
        op = alu_op_e'($urandom_range(4));
        a = $urandom_range(3) == 0 ? 8'(($urandom_range(2) == 0) ? 8'h00 : ($urandom_range(1) ? 8'hFF : 8'h80)) : 8'($urandom);
        b = $urandom_range(3) == 0 ? 8'(($urandom_range(2) == 0) ? 8'h00 : ($urandom_range(1) ? 8'hFF : 8'h80)) : 8'($urandom);
        c = $urandom_range(1);
        cg.sample(op, a, b, c);
        h_op[op] = 1; h_a[vbin(a)] = 1; h_b[vbin(b)] = 1;
        if (op inside {ADD, SUB, SHL}) h_c[c] = 1;
        if (!(op == SHL && (vbin(b) == 1 || vbin(b) == 2))) h_x[op][vbin(a)][vbin(b)] = 1;
      end
      ref_cov = 0.0;
      begin
        s_op = 0; s_a = 0; s_b = 0; s_c = 0; s_x = 0;
        foreach (h_op[i]) s_op += h_op[i];
        foreach (h_a[i]) s_a += h_a[i];
        foreach (h_b[i]) s_b += h_b[i];
        foreach (h_c[i]) s_c += h_c[i];
        foreach (h_x[i, j, k]) s_x += h_x[i][j][k];
        ref_cov = 100.0 * (s_op / 5.0 + s_a / 4.0 + s_b / 4.0 + s_c / 2.0 + s_x / 72.0) / 5.0;
      end
      near($sformatf("random run %0d", run), cg.get_inst_coverage(), ref_cov, 1e-4);
    end
    cells(1.0 / 256, 1.0 / 256, 1.0 / 256, 253.0 / 256, p);
    near("closure, uniform", expected_closure(p), UNIFORM, 1e-6 * UNIFORM);
    cells(0.2, 0.2, 0.2, 0.4, p);
    near("closure, dist", expected_closure(p), DIST, 1e-6 * DIST);
    cells(0.25, 0.25, 0.25, 0.25, p);
    near("closure, equal", expected_closure(p), EQUAL, 1e-6 * EQUAL);
    if (errors == 0) $display("PASS"); else $display("FAIL: %0d errors", errors);
    $finish;
  end
endmodule
