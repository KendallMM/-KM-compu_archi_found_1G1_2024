
module pwm_tb();
	
	reg [3:0] Porcentaje;
	reg SLK;
	wire pwm;
	
	pwm test(.Porcentaje(Porcentaje), .SLK(SLK), .pwm(pwm));
	
	initial begin
		Porcentaje = 4'b0111;
		SLK = 0;
		repeat (1024*77)
			begin
				#77 SLK = ~SLK;
			end
	
	end

endmodule