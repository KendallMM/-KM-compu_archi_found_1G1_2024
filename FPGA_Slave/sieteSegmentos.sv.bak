module sieteSegmentos(A,B,C,D,res, res2);
 input logic A;
 input logic B;
 input logic C;
 input logic D;
 output [6:0] res;
 reg [6:0] res;
 output [6:0] res2;
 reg [6:0] res2;


assign res[0] = ~((~B&~D)|(~A&C)|(A&~C)|(B&D));	//a
assign res[1] = ~((~B)|(~D&~C)|(A&~C)|(A&~D)|(~A&C&D)); //b
assign res[2] = ~((D)|(~A&B)|(A&C)|(~B&~C));	//c
assign res[3] = ~((~B&~D)|(A&~C)|(B&~C&D)|(~A&~B&C)|(A&B&D)|(~A&C&~D)); //d
assign res[4] = ~((~B&~D)|(A&~C&~D)|(~A&C&~D)); //e
assign res[5] = ~((A&C&~D)|(~A&B&~C)|(~B&~C&~D)|(A&~B&~C)|(B&C&~D)|(A&C&B)); //f
assign res[6] = ~((A&B)|(B&~C)|(A&~C)|(~A&C&~D)|(~A&~B&C)); //g
assign res2[0] = ~((~A)|(~B&~C));//a
assign res2[1] = 0; //b
assign res2[2] = 0;//c
assign res2[3] = ~((~A)|(~B&~C)); //d
assign res2[4] = ~((~A)|(~B&~C)); //e
assign res2[5] = ~((~A)|(~B&~C)); //f
assign res2[6] = 1; //g
							
endmodule