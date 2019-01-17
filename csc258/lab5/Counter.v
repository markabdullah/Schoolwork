//SW[1] Enable
//SW[0] Clear_b
//KEY[0] Clock

module Counter(LEDR, HEX0, HEX1, SW, KEY);
	input [9:0] SW;
	input [2:0] KEY;
	output [6:0] HEX0;
	output [6:0] HEX1;
	output [7:0] LEDR;
	
	wire [7:0] Q;
	
	CounterSub count(
		.Q(Q),
		.enable(SW[1]),
		.clock(KEY[0]),
		.clear_b(SW[0])
	);
	
	segmentdecoder sd0(
		.hex(HEX0[6:0]),
		.SW(Q[3:0])
	);
	
	segmentdecoder sd1(
		.hex(HEX1[6:0]),
		.SW(Q[7:4])
	);
	
	assign LEDR[7:0] = Q;
	
endmodule

module CounterSub(Q, enable, clock, clear_b);
	output [7:0] Q;
	input enable, clock, clear_b;
	
	wire q1, q2, q3, q4, q5, q6, q7;
	assign q1 = enable && Q[0];
	assign q2 = q1 && Q[1];
	assign q3 = q2 && Q[2];
	assign q4 = q3 && Q[3];
	assign q5 = q4 && Q[4];
	assign q6 = q5 && Q[5];
	assign q7 = q6 && Q[6];
	
	
	TFlipFlop f0(
		.Q(Q[0]),
		.enable(enable),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f1(
		.Q(Q[1]),
		.enable(q1),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f2(
		.Q(Q[2]),
		.enable(q2),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f3(
		.Q(Q[3]),
		.enable(q3),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f4(
		.Q(Q[4]),
		.enable(q4),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f5(
		.Q(Q[5]),
		.enable(q5),
		.clock(clock),
		.clear_b(clear_b)
	);

	TFlipFlop f6(
		.Q(Q[6]),
		.enable(q6),
		.clock(clock),
		.clear_b(clear_b)
	);
	
	TFlipFlop f7(
		.Q(Q[7]),
		.enable(q7),
		.clock(clock),
		.clear_b(clear_b)
	);
	
endmodule

module TFlipFlop(Q, enable, clock, clear_b);
	output reg Q;
	input enable, clock, clear_b;
	
	always @(posedge clock, negedge clear_b)
	begin
		if(clear_b == 0)
			Q <= 0;
		else
			Q <= enable ^ Q;
	end
endmodule

module segmentdecoder(hex, SW);
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

