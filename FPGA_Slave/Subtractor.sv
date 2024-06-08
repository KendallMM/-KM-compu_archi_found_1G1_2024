module Subtractor #(parameter N = 4)(
    input logic [N-1:0] minuendo,
    input logic [N-1:0] sustraendo,
    output logic [N-1:0] diferencia
);
    // se transforma el sustraendo a un número negativo

    logic[N:0] complemento_dos; 
    logic[N:0] temp_sum;
    logic cout;
    // complemento a dos; transformar un número de N bits, en su complemento, y sumarle número, dando como resultado, el número negativo.
    assign complemento_dos = ~sustraendo + 1;

    // Suma el minuendo (número al que se le va a restar), con el complemento, dando el resultado de la resta.
    Adder #(N) restAdder (
        .num1(minuendo),
        .num2(complemento_dos),
        .sum(temp_sum),
        .cout(cout)
    );
	 assign diferencia=(minuendo>sustraendo)?temp_sum[N-1:0]:(~temp_sum[N-1:0]+1);
endmodule