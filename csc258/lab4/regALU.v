//SW[3:0] data input - A
//SW[7:5] data input - ALU function input
//SW[9] data input - reset
//KEY[0] data input - Clock
//LEDR[7:0] output display - regALUout
//HEX0 output display - A
//HEX5-HEX4 output display - out


module regALU(LEDR, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, SW, KEY);
	input [9:0] SW;
	input [9:0] KEY;
	output [9:0] LEDR;
	output [6:0] HEX0;
	output [6:0] HEX1;
	output [6:0] HEX2;
	output [6:0] HEX3;
	output [6:0] HEX4;
	output [6:0] HEX5;
	
	reg [7:0] ALUout;
	reg [7:0] regALUout;
	
	wire [3:0] A = SW[3:0];
	wire [3:0] B = regALUout[3:0];
	wire clock = KEY[0];
	wire reset = SW[9];
	
	wire [7:0] case0;
	wire [7:0] case1;
	wire [7:0] case2 = A + B;
	wire [7:0] case3 = {A | B, A ^ B}; 
	wire [7:0] case4 = (|(A | B)) ? 8'b00000001 : 8'b00000000;
	wire [7:0] case5 = B << A;
	wire [7:0] case6 = B >> A;
	wire [7:0] case7 = A * B;
	
	ripplecarryadder adder0(
		.out(case0),
		.inA(A),
		.inB(4'b0001)
	);
	
	ripplecarryadder adder1(
		.out(case1),
		.inA(A),
		.inB(regALUout[3:0])
	);
		
	always @(*)
	begin
		case(SW[7:5])
			3'b000: ALUout = case0;
			3'b001: ALUout = case1;
			3'b010: ALUout = case2;
			3'b011: ALUout = case3;
			3'b100: ALUout = case4;
			3'b101: ALUout = case5;
			3'b110: ALUout = case6;
			3'b111: ALUout = case7;
			default: ALUout = 8'b00000000;
		endcase
	end
	
	always @(posedge clock)
	begin
		if(reset == 1'b0)
			regALUout <= 8'b00000000;
		else
			regALUout <= ALUout;
	end
	
	assign LEDR[7:0] = regALUout;
	
	segmentdecoder decoderA(
		.hex(HEX0[6:0]),
		.SW(SW[3:0])
	);
	
	segmentdecoder decoder1(
		.hex(HEX1[6:0]),
		.SW(4'b0000)
	);
	
	segmentdecoder decoder2(
		.hex(HEX2[6:0]),
		.SW(4'b0000)
	);

	segmentdecoder decoder3(
		.hex(HEX3[6:0]),
		.SW(4'b0000)
	);
	
	segmentdecoder decoder5(
		.hex(HEX5[6:0]),
		.SW(regALUout[7:4])
	);
	
	segmentdecoder decoder4(
		.hex(HEX4[6:0]),
		.SW(regALUout[3:0])
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
		.cin(1'b0)
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
