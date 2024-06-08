`timescale 1ns / 1ps

module ALU_tb;

// Parameters
parameter WIDTH = 4;
parameter CLK_PERIOD = 10; // Clock period in ns

// Inputs
reg [WIDTH-1:0] A, B;
reg [1:0] opcode;
reg clk;

// Outputs
wire [WIDTH*2-1:0] result;
wire N, Z, C, V;
wire [6:0] seg1, seg2;

// Instantiate the ALU module
ALU #(WIDTH) uut (
    .A(A),
    .B(B),
    .opcode(opcode),
    .result(result),
    .N(N),
    .Z(Z),
    .C(C),
    .V(V),
    .seg1(seg1),
    .seg2(seg2)
);

// Clock generation
always #((CLK_PERIOD / 2)) clk = ~clk;

// Test stimulus
initial begin
    // Reset
    A <= 4'b0000;
    B <= 4'b0000;
    opcode <= 2'b00;
    #20;

    // Test subtraction resulting in 0
    A <= 4'b0101;
    B <= 4'b0101;
    opcode <= 2'b01;
    #20;

    // Test addition with carry
    A <= 4'b1111;
    B <= 4'b0001;
    opcode <= 2'b00;
    #20;

    // Test addition with overflow
    A <= 4'b0111;
    B <= 4'b0111;
    opcode <= 2'b00;
    #20;

    // Test negative subtraction
    A <= 4'b0100;
    B <= 4'b1101;
    opcode <= 2'b01;
    #20;

    // Test logical OR operation
    A <= 4'b1010;
    B <= 4'b0011;
    opcode <= 2'b11;
    #20;

    $stop; // Stop simulation
end

// Display output flags and result
always @(posedge clk) begin
    $display("Result: %h, N: %b, Z: %b, C: %b, V: %b", result, N, Z, C, V);
end

endmodule
