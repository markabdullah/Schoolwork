//SW[7:0] data inputs - A and B
//KEY[2:0] data inputs - function
//LEDR[7:0] output display - ALUout
//HEX5-HEX0 output display

module ALU(LEDR, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, SW, KEY);
	input [7:0] SW;
	input [2:0] KEY;
	output [7:0] LEDR;
	output [6:0] HEX0;
	output [6:0] HEX1;
	output [6:0] HEX2;
	output [6:0] HEX3;
	output [6:0] HEX4;
	output [6:0] HEX5;
	
	
	wire [3:0] A = {SW[7], SW[6], SW[5], SW[4]};
	wire [3:0] B = {SW[3], SW[2], SW[1], SW[0]};
	
	wire [7:0] case0;
	wire [7:0] case1;
	
	ripplecarryadder adder0(
		.out(case0),
		.inA(A),
		.inB(4'b0001)
	);
	
	ripplecarryadder adder1(
		.out(case1),
		.inA(A),
		.inB(B)
	);
	
	wire [7:0] case2 = A + B;
	wire [7:0] case3 = {A | B, A ^ B}; 
	wire [7:0] case4 = (|(A | B)) ? 8'b00000001 : 8'b00000000;
	wire [7:0] case5 = {A, B};
	
	reg [7:0] ALUout;
	
	always @(*)
	begin
		case(KEY[2:0])
			3'b000: ALUout = case0;
			3'b001: ALUout = case1;
			3'b010: ALUout = case2;
			3'b011: ALUout = case3;
			3'b100: ALUout = case4;
			3'b101: ALUout = case5;
			default: ALUout = 8'b00000000;
		endcase
	end
	
	assign LEDR[7:0] = ALUout;
	
	
	segmentdecoder decoderA(
		.hex(HEX0[6:0]),
		.SW(SW[7:4])
	);
	
	segmentdecoder decoder1(
		.hex(HEX1[6:0]),
		.SW(4'b0000)
	);
	
	segmentdecoder decoderB(
		.hex(HEX2[6:0]),
		.SW(SW[3:0])
	);

	segmentdecoder decoder3(
		.hex(HEX3[6:0]),
		.SW(4'b0000)
	);
	
	segmentdecoder decoder5(
		.hex(HEX5[6:0]),
		.SW(ALUout[7:4])
	);
	
	segmentdecoder decoder4(
		.hex(HEX4[6:0]),
		.SW(ALUout[3:0])
	);
	
	
	
endmodule

module ripplecarryadder(out, inA, inB);
	input [3:0] inA;
	input [3:0] inB;
	output [7:0] out;
	wire c1;
	wire c2;
	wire c3;
	
	fulladder FA0(
		.S(out[0]),
		.cout(c1),
		.A(inA[0]),
		.B(inB[0]),
		.cin(0)
	);
	
	fulladder FA1(
		.S(out[1]),
		.cout(c2),
		.A(inA[1]),
		.B(inB[1]),
		.cin(c1)
	);
	
	fulladder FA2(
		.S(out[2]),
		.cout(c3),
		.A(inA[2]),
		.B(inB[2]),
		.cin(c2)
	);
	
	fulladder FA3(
		.S(out[3]),
		.cout(out[4]),
		.A(inA[3]),
		.B(inB[3]),
		.cin(c3)
	);
	
	assign out[5] = 0;
	assign out[6] = 0;
	assign out[7] = 0;
	
endmodule

module fulladder(S, cout, A, B, cin);
	input A; //first bit
	input B; //second bit
	input cin; //carry in bit
	output S; //sum value
	output cout; //carry out bit
	
	wire w0;
	xor xor0(w0, A, B);
	xor xor1(S, w0, cin);
	
	mux2to1 mux0(
      .x(B),
      .y(cin),
      .s(w0),
      .m(cout)
   );
	
	
endmodule

module mux2to1(x, y, s, m);
   input x; //selected when s is 0
   input y; //selected when s is 1
   input s; //select signal
   output m; //output
  
   assign m = s & y | ~s & x;
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
