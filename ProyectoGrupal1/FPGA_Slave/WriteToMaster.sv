module WriteToMaster(
    input SLK, rst, MOSI,
    input CS,
	 input bit15,
	 input bit14,
	 input bit13,
	 input bit12,
	 input bit11,
	 input bit10,
	 input bit9,
	 input bit8,
	 input bit7,
	 input bit6,
	 input bit5,
	 input bit4,
	 input bit3,
	 input bit2,
	 input bit1,
	 input bit0,
    output reg MISO
    
);
wire [15:0] bits;

assign bits[15] = bit0;
assign bits[14] = bit1;
assign bits[13] = bit2;
assign bits[12] = bit3;
assign bits[11] = bit4;
assign bits[10] = bit5;
assign bits[9] = bit6;
assign bits[8] = bit7;
assign bits[7] = bit8;
assign bits[6] = bit9;
assign bits[5] = bit10;
assign bits[4] = bit11;
assign bits[3] = bit12;
assign bits[2] = bit13;
assign bits[1] = bit14;
assign bits[0] = bit15;
logic d;
			
assign d = MOSI & CS & ~rst;

reg [3:0] counter;


always @ (posedge SLK & CS) begin
		MISO <= rst == 1 ? 255:d;
		counter<=counter+4'b0001;
end 

endmodule