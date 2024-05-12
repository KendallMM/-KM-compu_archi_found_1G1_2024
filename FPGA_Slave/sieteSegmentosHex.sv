module sieteSegmentosHex(input A, B, C, D, output [6:0] display, output [6:0] display2);


assign display[0] = ~((~A&~B));	//a
assign display[1] = ~((~A&B)); //b
assign display[2] = ~((A&~B));	//c
assign display[3] = ~((~A&~B)); //d
assign display[4] = ~((~A&~B)); //e
assign display[5] = ~((~A&~B)); //f
assign display[6] = ~((~A&~B)); //g
assign display2[0] = ~((~A&~B));//a
assign display2[1] = 0; //b
assign display2[2] = 0;//c
assign display2[3] = ~((~A)|(~B&~C)); //d
assign display2[4] = ~((~A)|(~B&~C)); //e
assign display2[5] = ~((~A)|(~B&~C)); //f
assign display2[6] = 1; //g
							
endmodule