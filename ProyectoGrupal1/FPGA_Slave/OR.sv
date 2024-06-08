module OR(input logic a, b, output logic y);
    always_comb begin
        y = 0;
        if (a == 1)
            y = 1;
        else if (b == 1)
            y = 1;
    end
endmodule