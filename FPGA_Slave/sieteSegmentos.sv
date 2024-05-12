module sieteSegmentos(input A, B, C, D, output [6:0] display, output [6:0] display2);


assign display[0] = ~((~B&~D)|(~A&C)|(A&~C)|(B&D));	//a
assign display[1] = ~((~B)|(~D&~C)|(A&~C)|(A&~D)|(~A&C&D)); //b
assign display[2] = ~((D)|(~A&B)|(A&C)|(~B&~C));	//c
assign display[3] = ~((~B&~D)|(A&~C)|(B&~C&D)|(~A&~B&C)|(A&B&D)|(~A&C&~D)); //d
assign display[4] = ~((~B&~D)|(A&~C&~D)|(~A&C&~D)); //e
assign display[5] = ~((A&C&~D)|(~A&B&~C)|(~B&~C&~D)|(A&~B&~C)|(B&C&~D)|(A&C&B)); //f
assign display[6] = ~((A&B)|(B&~C)|(A&~C)|(~A&C&~D)|(~A&~B&C)); //g
assign display2[0] = ~((~A)|(~B&~C));//a
assign display2[1] = 0; //b
assign display2[2] = 0;//c
assign display2[3] = ~((~A)|(~B&~C)); //d
assign display2[4] = ~((~A)|(~B&~C)); //e
assign display2[5] = ~((~A)|(~B&~C)); //f
assign display2[6] = 1; //g
							
endmodule