module tb;
  //@page function automatic bit israel_cannot_win
  //@page function automatic int earliest_certain_loss

  int errors = 0;

  // Reference: call the check again after every announcement (O(k^2), obviously right)
  function automatic int earliest_reference(int israel_total, country_t above[$], int points_left);
    int  jury_left[$];
    int  left;
    bit  passed;
    for (int k = 0; k <= above.size(); k++) begin
      jury_left.delete();
      left   = points_left;
      passed = 0;
      for (int i = 0; i < k; i++) begin
        left -= above[i].public_pts;
        if (above[i].jury + above[i].public_pts > israel_total) passed = 1;
      end
      for (int i = k; i < above.size(); i++) jury_left.push_back(above[i].jury);
      if (passed || israel_cannot_win(israel_total, jury_left, left)) return k;
    end
    return -1;
  endfunction

  initial begin
    country_t above[$];
    int       jury[$];
    int       israel_total, points_left;

    above = '{'{"Poland", 133, 17}, '{"Italy", 134, 147}, '{"Finland", 141, 138},
              '{"France", 144, 14}, '{"Australia", 165, 122}, '{"Denmark", 165, 78},
              '{"Bulgaria", 204, 312}};
    if (earliest_certain_loss(343, above, 828) != 4) errors++;
    jury = '{133, 134, 141, 144, 165, 165, 204};
    if (israel_cannot_win(343, jury, 828)) errors++;
    jury = '{165, 165, 204};
    if (israel_cannot_win(343, jury, 495)) errors++;
    if (!israel_cannot_win(343, jury, 512)) errors++;
    jury = '{344};
    if (!israel_cannot_win(343, jury, 0)) errors++;

    repeat (3000) begin
      israel_total = $urandom_range(50, 400);
      above.delete();
      points_left = 0;
      repeat ($urandom_range(0, 8)) begin
        country_t c;
        c.country    = "c";
        c.jury       = $urandom_range(0, israel_total + 20);
        c.public_pts = $urandom_range(0, 300);
        points_left += c.public_pts;
        above.push_back(c);
      end
      if (earliest_certain_loss(israel_total, above, points_left)
          != earliest_reference(israel_total, above, points_left)) errors++;
    end

    if (errors == 0) $display("PASS");
    else $display("FAIL errors=%0d", errors);
    $finish;
  end
endmodule
