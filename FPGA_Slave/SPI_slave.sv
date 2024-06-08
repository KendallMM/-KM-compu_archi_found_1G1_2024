 module SPI_slave(
    input logic MOSI, SS, sclk, rst,
    output logic MISO, n, z, c, v,
    output reg [3:0] num1,
    output reg [3:0] num2,
    output reg [1:0] operacion,
    output reg [7:0] resultado,
    output wire [6:0] display, 
    output wire [6:0] display2, 
    output wire [6:0] display3, 
    output wire [6:0] display4, 
    output wire pwm_out
);

    logic d;

    assign d = MOSI & SS & ~rst;

    assign MISO = rst == 1 ? 255 : d;

    // Flip-flops para los bits de num1
    always @(posedge sclk or posedge rst) begin
        if (rst)
            num1 <= 4'b0;
        else
            num1 <= {num1[2:0], MOSI};
    end

    // Flip-flops para los bits de num2
    always @(posedge sclk or posedge rst) begin
        if (rst)
            num2 <= 4'b0;
        else
            num2 <= {num2[2:0], num1[3]};
    end

    // Flip-flops para los bits de operacion
    always @(posedge sclk or posedge rst) begin
        if (rst)
            operacion <= 2'b0;
        else
            operacion <= {operacion[0], num2[3]};
    end

    // Display y PWM (suponiendo que están sincronizados correctamente)
    sieteSegmentos operando1(.A(num1[3]), .B(num1[2]), .C(num1[1]), .D(num1[0]), .display(display), .display2(display2));
    sieteSegmentos operando2(.A(num2[3]), .B(num2[2]), .C(num2[1]), .D(num2[0]), .display(display3), .display2(display4));
    pwm motor (.Velocidad(num1), .SLK(sclk), .pwm(pwm_out) );
	 ALU aluOp(.A(num1), .B(num2),.opcode(operacion),.result(resultado),.N(n), .Z(z), .C(c), .V(v));


endmodule