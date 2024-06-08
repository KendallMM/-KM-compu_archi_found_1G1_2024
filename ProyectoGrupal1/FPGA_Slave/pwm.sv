module pwm (input [3:0] Velocidad,
	input SLK,
   output reg pwm
   
);


reg [3:0] counter; //0-9


initial begin
		counter = 0;
end


	always @ (posedge SLK) begin
		
		pwm <= Velocidad >= counter ;
		
		counter <= counter + 1;
      
   end 
	
	

endmodule 