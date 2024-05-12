module SPI_slave(
	input logic MOSI, SS, sclk, rst,
	output logic MISO, 
	output reg [3:0] num1,
	output reg [3:0] num2,
	output reg [1:0] operacion,
	output reg [7:0] suma,
	output resetBits,
	output wire [6:0] display, 
	output wire [6:0] display2, 
	output wire [6:0] display3, 
	output wire [6:0] display4, 
	output pwm_out
);
	logic d;
	
	assign d = MOSI & SS & ~rst;
	
	assign resetBits=rst;
	assign MISO = rst == 1 ? 255:d;
	
	//Bits
	flipflop_SD  ff_num1bit0(
		.d(d), .clk(sclk), .rst(rst),
		.q(num1[0])
	);
	
	flipflop_SD  ff_num1bit1(
		.d(num1[0]), .clk(sclk), .rst(rst),
		.q(num1[1])
	);
	
	flipflop_SD  ff_num1bit2(
		.d(num1[1]), .clk(sclk), .rst(rst),
		.q(num1[2])
	);
	
	flipflop_SD  ff_num1bit3(
		.d(num1[2]), .clk(sclk), .rst(rst),
		.q(num1[3])
	);
	flipflop_SD  ff_num2bit0(
		.d(num1[3]), .clk(sclk), .rst(rst),
		.q(num2[0])
	);
	
	flipflop_SD  ff_num2bit1(
		.d(num2[0]), .clk(sclk), .rst(rst),
		.q(num2[1])
	);
	
	flipflop_SD  ff_num2bit2(
		.d(num2[1]), .clk(sclk), .rst(rst),
		.q(num2[2])
	);
	
	flipflop_SD  ff_num2bit3(
		.d(num2[2]), .clk(sclk), .rst(rst),
		.q(num2[3])
	);
	flipflop_SD  operacionBit1(
		.d(num2[3]), .clk(sclk), .rst(rst),
		.q(operacion[0])
	);
	
	flipflop_SD  operacionBit2(
		.d(operacion[0]), .clk(sclk), .rst(rst),
		.q(operacion[1])
	);
	
	
	sieteSegmentos operando1(.A(num1[3]), .B(num1[2]), .C(num1[1]), .D(num1[0]), .display(display), .display2(display2));
	sieteSegmentos operando2(.A(num2[3]), .B(num2[2]), .C(num2[1]), .D(num2[0]), .display(display3), .display2(display4));
	pwm motor (.Porcentaje(Bits), .SLK(sclk), .pwm(pwm_out) );
	
endmodule