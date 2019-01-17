//input SW[1:0] controls ratedivider
//input SW[2] enable
//input SW[3] par_load
//input SW[4] reset
//output HEX0

module Flasher(HEX0, LEDR, CLOCK_50, SW);
	output [6:0] HEX0;
	output [3:0] LEDR;
	input [4:0] SW;
	input CLOCK_50;
	
	reg [27:0] q;
	wire [27:0] count;
	wire [3:0] hexval;
	wire enable;
	
	always @(*)
	begin
		case(SW[1:0])
			2'b00: q <= 2;
			2'b01: q <= 49999999;
			2'b10: q <= 99999999;
			2'b11: q <= 199999999;
		endcase
	end
	
	RateDivider rd(
		.out(count),
		.in(q),
		.enable(SW[2]),
		.clock(CLOCK_50),
		.par_load(SW[3]),
		.reset(SW[4])
	);
	
	assign enable = (count == 1) ? 1 : 0;
	
	DisplayCounter dc(
		.out(hexval),
		.enable(enable),
		.clock(CLOCK_50),
		.reset(SW[4])
	);
	
	segmentdecoder sd1(
		.hex(HEX0[6:0]),
		.SW(hexval[3:0])
	);
	
	assign LEDR[3:0] = hexval;

endmodule

module RateDivider(out, in, enable, clock, par_load, reset);
	output reg [27:0] out;
	input [27:0] in;
	input enable;
	input clock;
	input par_load;
	input reset;
	
	always @(posedge clock)
	begin
		if(reset == 0)
			out <= 0;
		else if(par_load == 1)
			out <= in;
		else if(enable == 1)
			begin 
				if(out == 0)
					out <= in;
				else
					out <= out - 1;
			end
	end
	
endmodule

module DisplayCounter(out, enable, clock, reset);
	output reg [3:0] out;
	input enable;
	input clock;
	input reset;
	
	always @(posedge clock)
	begin
		if(reset == 0)
			out <= 0;
		else if(enable == 1)
			begin 
				if(out == 4'b1111)
					out <= 0;
				else
					out <= out + 1;
			end
	end
	
endmodule
 

module segdecoder(hex, SW);
	input [3:0] SW;
   output [6:0]hex;
	
	assign hex[0] = ~SW[3] & ~SW[2] & ~SW[1] & SW[0] | ~SW[3] & SW[2] & ~SW[1] & ~SW[0] | SW[3] & SW[2] & ~SW[1] & SW[0] | SW[3] & ~SW[2] & SW[1] & SW[0];
	assign hex[1] = ~SW[3] & SW[2] & ~SW[1] & SW[0] | SW[2] & SW[1] & ~SW[0] | SW[3] & SW[1] & SW[0] | SW[3] & SW[2] & ~SW[0];
	assign hex[2] = ~SW[3] & ~SW[2] & SW[1] & ~SW[0] | SW[3] & SW[2] & ~SW[0] | SW[3] & SW[2] & SW[1];
	assign hex[3] = ~SW[3] & SW[2] & ~SW[1] & ~SW[0] | SW[3] & ~SW[2] & SW[1] & ~SW[0] | ~SW[2] & ~SW[1] & SW[0] | SW[2] & SW[1] & SW[0];
	assign hex[4] = ~SW[3] & SW[2] & ~SW[1] | ~SW[2] & ~SW[1] & SW[0] | ~SW[3] & SW[0];
	assign hex[5] = SW[3] & SW[2] & ~SW[1] & SW[0] | ~SW[3] & SW[1] & SW[0] | ~SW[3] & ~SW[2] & SW[0] | ~SW[3] & ~SW[2] & SW[1];
	assign hex[6] = SW[3] & SW[2] & ~SW[1] & ~SW[0] | ~SW[3] & SW[2] & SW[1] & SW[0] | ~SW[3] & ~SW[2] & ~SW[1];
	
endmodule
