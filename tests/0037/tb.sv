// Question 0037: the page's sync_mtbf on the page numbers (19 s, 297 years, 1.4e11 years
// at 500 MHz), the ratio between consecutive depths (exp(T / tau)), and the edge cases.
module tb;
  //@page function automatic real sync_mtbf

  int errors = 0;
  localparam real YEAR = 365.25 * 86400.0;

  function automatic bit close(real a, real b, real rel = 1e-3);
    return (a > b ? a - b : b - a) <= rel * (b > 0 ? b : 1.0);
  endfunction

  initial begin
    real m1, m2, m3;
    m1 = sync_mtbf(500e6, 50e6, 100e-12, 50e-12, 0.3e-9, 1);
    m2 = sync_mtbf(500e6, 50e6, 100e-12, 50e-12, 0.3e-9, 2);
    m3 = sync_mtbf(500e6, 50e6, 100e-12, 50e-12, 0.3e-9, 3);
    $display("500 MHz: %0.3g s, %0.3g years, %0.3g years", m1, m2 / YEAR, m3 / YEAR);
    if (!close(m1, 19.3, 0.01)) begin errors++; $display("one flop expected ~19.3 s"); end
    if (!close(m2 / YEAR, 297.0, 0.01)) begin errors++; $display("two flops expected ~297 years"); end
    if (!close(m3 / YEAR, 1.44e11, 0.01)) begin errors++; $display("three flops expected ~1.44e11 years"); end
    if (!close(m2 / m1, $exp(2.0e-9 / 100e-12)) || !close(m3 / m2, $exp(2.0e-9 / 100e-12))) begin
      errors++; $display("each flop should multiply the MTBF by exp(T / tau)");
    end
    m1 = sync_mtbf(1e9, 50e6, 100e-12, 50e-12, 0.3e-9, 1);
    m3 = sync_mtbf(1e9, 50e6, 100e-12, 50e-12, 0.3e-9, 3);
    if (!close(m1, 0.439e-3, 0.01) || !close(m3 / 86400.0, 2.46, 0.01)) begin
      errors++; $display("1 GHz: expected 0.44 ms and 2.46 days, got %0.3g s and %0.3g days", m1, m3 / 86400.0);
    end
    if (sync_mtbf(1e9, 50e6, 100e-12, 50e-12, 1.2e-9, 1) != 0.0) begin errors++; $display("no time to resolve: expected 0"); end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
