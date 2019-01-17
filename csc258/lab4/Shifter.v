//SW[7:0] data input - load_val
//SW[9] data input - reset_n
//KEY[0] data input - Clock
//KEY[1] data input - load_n
//KEY[2] data input - shift
//KEY[3] data input - ASR
//LEDR[7:0] output display - Q


module Shifter(LEDR, KEY, SW);
	output [7:0] LEDR;
	input [9:0] SW;
	input [3:0] KEY;

	wire out7, out6, out5, out4, out3, out2, out1, out0;
	wire in7;
	
	assign in7 = KEY[3] & out7;
	
	ShifterBit S7(
		.out(out7),
		.in(in7),
		.load_val(SW[7]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
		);
	
	ShifterBit S6(
		.out(out6),
		.in(out7),
		.load_val(SW[6]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S5(
		.out(out5),
		.in(out6),
		.load_val(SW[5]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S4(
		.out(out4),
		.in(out5),
		.load_val(SW[4]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S3(
		.out(out3),
		.in(out4),
		.load_val(SW[3]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S2(
		.out(out2),
		.in(out3),
		.load_val(SW[2]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S1(
		.out(out1),
		.in(out2),
		.load_val(SW[1]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	ShifterBit S0(
		.out(out0),
		.in(out1),
		.load_val(SW[0]),
		.shift(KEY[2]),
		.load_n(KEY[1]),
		.clk(KEY[0]),
		.reset_n(SW[9])
	);
	
	assign LEDR[7:0] = {out7, out6, out5, out4, out3, out2, out1, out0};
		
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
	
	always @(posedge clk)
	begin
		if (reset_n == 1'b0)
			Q <= 0;
		else
			Q <= D;
	end
endmodule
