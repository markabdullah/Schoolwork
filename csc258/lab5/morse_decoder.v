//input SW[2:0] 
//input KEY[1] load_n
//input KEY[0] reset
//output LEDR[0] 

module morse_decoder(LEDR, SW, KEY, CLOCK_50);
	output [9:0] LEDR;
	input [2:0] SW;
	input [1:0] KEY;
	input CLOCK_50;
	
	wire [27:0] count;
	wire [12:0] Q;
	wire shift;
	reg [12:0] morsecode;
	
	always @(*)
	begin
		case(SW[2:0])
			3'b000: morsecode = 13'b0000000010101;
			3'b001: morsecode = 13'b0000000000111;
			3'b010: morsecode = 13'b0000001110101;
			3'b011: morsecode = 13'b0000111010101;
			3'b100: morsecode = 13'b0000111011101;
			3'b101: morsecode = 13'b0011101010111;
			3'b110: morsecode = 13'b1110111010111;
			3'b111: morsecode = 13'b0010101110111;
		endcase
	end

	Shifter ss(
		.Q(Q),
		.load_val(morsecode),
		.load_n(KEY[1]),
		.shift(shift),
		.clock(CLOCK_50),
		.reset(KEY[0])
	);
	
	RateDivider2 rd(
		.out(count),
		.in(2), //set to 99,999,999 
		.enable(1),
		.clock(CLOCK_50),
		//.par_load(KEY[1]),
		.reset(KEY[0])
	);
	
	assign shift = (count == 1) ? 1 : 0;
	assign LEDR[0] = Q[0];
	
endmodule


module RateDivider2(out, in, enable, clock, reset);
	output reg [27:0] out;
	input [27:0] in;
	input enable;
	input clock;
	//input par_load;
	input reset;
	
	always @(posedge clock, negedge reset)
	begin
		if(reset == 0)
			out <= 0;
//		else if(par_load == 1)
//			out <= in;
		else if(enable == 1)
			begin 
				if(out == 0)
					out <= in;
				else
					out <= out - 1;
			end
	end
	
endmodule


module Shifter(Q, load_val, load_n, shift, clock, reset);
	output [12:0] Q;
	input [12:0] load_val;
	input load_n;
	input shift;
	input clock;
	input reset;
	
	ShifterBit S12(
		.out(Q[12]),
		.in(0),
		.load_val(load_val[12]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S11(
		.out(Q[11]),
		.in(Q[12]),
		.load_val(load_val[11]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
	
	ShifterBit S10(
		.out(Q[10]),
		.in(Q[11]),
		.load_val(load_val[10]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S9(
		.out(Q[9]),
		.in(Q[10]),
		.load_val(load_val[9]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S8(
		.out(Q[8]),
		.in(Q[9]),
		.load_val(load_val[8]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
		
	ShifterBit S7(
		.out(Q[7]),
		.in(Q[8]),
		.load_val(load_val[7]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
	
	ShifterBit S6(
		.out(Q[6]),
		.in(Q[7]),
		.load_val(load_val[6]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S5(
		.out(Q[5]),
		.in(Q[6]),
		.load_val(load_val[5]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
		
	ShifterBit S4(
		.out(Q[4]),
		.in(Q[5]),
		.load_val(load_val[4]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
		
	ShifterBit S3(
		.out(Q[3]),
		.in(Q[4]),
		.load_val(load_val[3]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S2(
		.out(Q[2]),
		.in(Q[3]),
		.load_val(load_val[2]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);
		
	ShifterBit S1(
		.out(Q[1]),
		.in(Q[2]),
		.load_val(load_val[1]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
		);

	ShifterBit S0(
		.out(Q[0]),
		.in(Q[1]),
		.load_val(load_val[0]),
		.shift(shift),
		.load_n(load_n),
		.clk(clock),
		.reset_n(reset)
	);
		
endmodule


module ShifterBit(out, in, load_val, shift, load_n, clk, reset_n);
	output out;
	input in, load_val, shift, load_n, clk, reset_n;
	
	wire shiftmuxout;
	wire load_nmuxout;
	
	assign shiftmuxout = shift & in | ~shift & out;
	assign load_nmuxout = load_n & shiftmuxout | ~load_n & load_val;
	
	flipflop F0(
		.Q(out),
		.D(load_nmuxout),
		.clk(clk),
		.reset_n(reset_n)
	);
endmodule


module flipflop(Q, D, clk, reset_n);
	output reg Q;
	input D, clk, reset_n;
	
	always @(posedge clk, negedge reset_n)
	begin
		if (reset_n == 1'b0)
			Q <= 0;
		else
			Q <= D;
	end
endmodule

