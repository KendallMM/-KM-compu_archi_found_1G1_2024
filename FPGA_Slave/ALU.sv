module ALU #(parameter WIDTH = 4) (
    input logic [WIDTH - 1:0] A, B,
    input logic [1:0] opcode,
    output logic [WIDTH*2 - 1:0] result,
    output logic N, Z, C, V,
    output logic [6:0]seg1, seg2
);

logic [WIDTH*2-1:0] addResult;
logic [WIDTH*2-1:0] subResult;
logic [WIDTH*2-1:0] andResult;
logic [WIDTH*2-1:0] orResult;

Adder #(WIDTH) adder(
    .num1(A), 
    .num2(B), 	
    .sum(addResult), 
    .cout());

Subtractor #(WIDTH) subtractor(
    .minuendo(A), 
    .sustraendo(B), 
    .diferencia(subResult));
	 
assign andResult = A & B;
assign orResult = A | B;


assign result = (opcode == 2'b00) ? addResult :
                (opcode == 2'b01) ? subResult :
                (opcode == 2'b10) ? andResult :
                (opcode == 2'b11) ? orResult :
                0;

assign N = (opcode == 2'b01 && (A < B)); // flag de negativo
assign Z = (result == 0); // flag de cero
assign C = (opcode == 2'b00) && ((result < A) || (result < B));  // flag de Carry
assign V = (opcode == 2'b00) && ((A && B && !result) || (!A && !B && result)); //flag de overflow


endmodule