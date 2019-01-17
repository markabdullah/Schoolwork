//SW[7:0] data inputs
//SW[8] cin
//LEDR[4] cout
//LEDR[3:0] output display

module ripplecarryadder(LEDR, SW);
	input [9:0] SW;
	output [9:0] LEDR;
	wire c1;
	wire c2;
	wire c3;
	
	fulladder FA0(
		.S(LEDR[0]),
		.cout(c1),
		.A(SW[0]),
		.B(SW[4]),
		.cin(SW[8])
	);
	
	fulladder FA1(
		.S(LEDR[1]),
		.cout(c2),
		.A(SW[1]),
		.B(SW[5]),
		.cin(c1)
	);
	
	fulladder FA2(
		.S(LEDR[2]),
		.cout(c3),
		.A(SW[2]),
		.B(SW[6]),
		.cin(c2)
	);
	
	fulladder FA3(
		.S(LEDR[3]),
		.cout(LEDR[4]),
		.A(SW[3]),
		.B(SW[7]),
		.cin(c3)
	);
	
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
	