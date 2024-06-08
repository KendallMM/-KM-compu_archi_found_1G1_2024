module sieteSegmentosHex(input A, B, C, D, output [6:0] display);


assign display[0] = ~((~B&~D)|(B&C)|(A&~D)|(~A&C)|(A&~B&~C)|(~A&B&D));	//a
assign display[1] = ~((~B&~D)|(~B&~C)|(~A&C&D)|(A&~C&D)|(~A&~C&~D));
assign display[2] = ~((A&~B)|(~C&D)|(~A&B)|(~A&D)|(~B&~C));
assign display[3] = ~((A&B&~D)|(~B&~C&~D)|(B&~C&D)|(~A&C&~D)|(A&~B&D)|(~A&~B&C));
assign display[4] = ~((~B&~D)|(C&~D)|(A&B)|(A&C));
assign display[5] = ~((A&~B)|(B&~D)|(A&C)|(~C&~D)|(~A&B&~C));
assign display[6] = ~((C&~D)|(A&~B)|(~B&C)|(A&D)|(~A&B&~C));

endmodule