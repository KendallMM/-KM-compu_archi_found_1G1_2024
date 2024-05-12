module Adder #(parameter N = 4)(
    input logic [N-1:0] num1,
    input logic [N-1:0] num2,
    output logic [N-1:0] sum,
    output logic cout
);

    logic cin = 1'b0;
    logic tempCarry;

    always_comb begin
        tempCarry = cin;
        for (int i = 0; i < N; i++) begin
            sum[i] = num1[i] ^ num2[i] ^ tempCarry;
            tempCarry = (num1[i] & num2[i]) | (num1[i] & tempCarry) | (num2[i] & tempCarry);
        end
        cout = tempCarry;   // Carry-out
    end

     assign zero = (&(num1 == 0) & &(num2 == num1)) ? 1'b1 : 1'b0;

endmodule