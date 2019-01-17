//NotNot Game
//Mark Abdullah and Andreea Buzila

module NotNot
	(
		CLOCK_50,						//	On Board 50 MHz
		// Your inputs and outputs here
        KEY,
        SW,
		  HEX5,
		  HEX4,
		  HEX3,
		  HEX2,
		  HEX1,
		  HEX0,
		  LEDR,
		  
		  
		// The ports below are for the VGA output.  Do not change.
		VGA_CLK,   						//	VGA Clock
		VGA_HS,							//	VGA H_SYNC
		VGA_VS,							//	VGA V_SYNC
		VGA_BLANK_N,						//	VGA BLANK
		VGA_SYNC_N,						//	VGA SYNC
		VGA_R,   						//	VGA Red[9:0]
		VGA_G,	 						//	VGA Green[9:0]
		VGA_B,   						//	VGA Blue[9:0]
		PS2_DAT, 						// PS2 data line
		PS2_CLK							//PS2 clock
	);

	input			CLOCK_50;				//	50 MHz
	input   [9:0]   SW;
	input   [3:0]   KEY;
	output  [6:0]   HEX5;
	output  [6:0]   HEX4;
	output  [6:0]   HEX3;
	output  [6:0]   HEX2;
	output  [6:0]   HEX1;
	output  [6:0]   HEX0;
	output  [9:0]   LEDR;
	inout 		PS2_DAT;
	inout 		PS2_CLK;
	

	// Declare your inputs and outputs here
	// Do not change the following outputs
	output			VGA_CLK;   				//	VGA Clock
	output			VGA_HS;					//	VGA H_SYNC
	output			VGA_VS;					//	VGA V_SYNC
	output			VGA_BLANK_N;			//	VGA BLANK
	output			VGA_SYNC_N;				//	VGA SYNC
	output	[9:0]	VGA_R;   				//	VGA Red[9:0]
	output	[9:0]	VGA_G;	 				//	VGA Green[9:0]
	output	[9:0]	VGA_B;   				//	VGA Blue[9:0]
	
	wire resetn;
	assign resetn = KEY[0];
	
	// Create the colour, x, y and writeEn wires that are inputs to the controller.
	wire [2:0] colour1;
	wire [2:0] colour2;
	wire [3:0] key_answer;
	wire [7:0] x;
	wire [6:0] y;
	wire [7:0] x_in;
	wire [6:0] y_in;
	wire [5:0] counter;
	wire [1:0] go;
	wire countercase;
	wire writeEn;
	wire draw;
	wire start_timer;

	// Create an Instance of a VGA controller - there can be only one!
	// Define the number of colours as well as the initial background
	// image file (.MIF) for the controller.
	vga_adapter VGA(
			.resetn(resetn),
			.clock(CLOCK_50),
			.colour(colour2),
			.x(x),
			.y(y),
			.plot(writeEn),
			/* Signals for the DAC to drive the monitor. */
			.VGA_R(VGA_R),
			.VGA_G(VGA_G),
			.VGA_B(VGA_B),
			.VGA_HS(VGA_HS),
			.VGA_VS(VGA_VS),
			.VGA_BLANK(VGA_BLANK_N),
			.VGA_SYNC(VGA_SYNC_N),
			.VGA_CLK(VGA_CLK));
		defparam VGA.RESOLUTION = "160x120";
		defparam VGA.MONOCHROME = "FALSE";
		defparam VGA.BITS_PER_COLOUR_CHANNEL = 1;
		defparam VGA.BACKGROUND_IMAGE = "black.mif";
			
	// Put your code here. Your code should produce signals x,y,colour and writeEn/plot
	// for the VGA controller, in addition to any other functionality your design may require.
    
    // Instansiate datapath
	// datapath d0(...);
	
	datapath d0(
		.clock(CLOCK_50),
		.reset(resetn),
		.draw(draw),
		.key_in(key_in),
		.key_answer(key_answer[3:0]),
		.counter(counter),
		.counter_case(countercase),
		.colour_in(colour1),
		.x_in(x_in),
		.y_in(y_in),
		.start_timer(start_timer),
		.go(go),
		.colour_out(colour2),
		.x_out(x),
		.y_out(y),
		.plot(writeEn),
		.HEX2(HEX2),
		.HEX1(HEX1),
		.HEX0(HEX0),
		.LEDR(LEDR)
		);
		
		
	control c0(
		.clock(CLOCK_50),
		.reset(resetn),
		.go(go),
		.key_answer(key_answer[3:0]),
		.counter(counter),
		.counter_case(countercase),
		.colour(colour1),
		.x(x_in),
		.y(y_in),
		.draw(draw),
		.start_timer(start_timer),
		.HEX5(HEX5),
		.HEX4(HEX4),
		.HEX3(HEX3)
		);

    // Instansiate FSM control
    // control c0(...);
	 
	 wire w, a, s, d, up, down, left, right, space, enter;
	 wire [3:0] key_in;
	 
	 
	 keyboard_tracker #(.PULSE_OR_HOLD(0)) kt (
		.clock(CLOCK_50),
		.reset(resetn),
		.PS2_CLK(PS2_CLK),
		.PS2_DAT(PS2_DAT),
		.w(w),
		.a(a),
		.s(s),
		.d(d),
		.left(key_in[1]),
		.right(key_in[0]),
		.up(key_in[3]),
		.down(key_in[2]),
		.space(space),
		.enter(enter)
	 );
	
//	segdecoder sd2(
//		.hex(HEX2[6:0]),
//		.SW(key_in)
//	);
	
endmodule



module datapath(
	clock,
	reset,
	draw,
	key_in,
	key_answer,
	counter,
	counter_case,
	colour_in,
	x_in,
	y_in,
	start_timer,
	go,
	colour_out,
	x_out,
	y_out,
	plot,
	HEX2,
	HEX1,
	HEX0,
	LEDR);
	 
	input clock;
	input reset;
	input draw;
	input [3:0] key_in;
	input [3:0] key_answer;
	input [5:0] counter;
	input counter_case;
	input [2:0] colour_in;
	input [7:0] x_in;
	input [6:0] y_in;
	input start_timer;
	output [6:0] HEX2;
	output [6:0] HEX1;
	output [6:0] HEX0;
	output [9:0] LEDR;
	output reg [1:0] go;
	output reg [2:0] colour_out;
	output reg [7:0] x_out;
	output reg [6:0] y_out;
	output reg plot;
	
	
	reg counterregold;
	reg key_in_old;
	reg [5:0] counterreg;
	reg [7:0] score_counter = 0;
	reg [25:0] timer_dividor;
	reg [3:0] timer;
	
	

	//drawing pixels
	always @ (posedge clock) begin
		colour_out <= colour_in;
		if(!reset) begin
			counterreg <= 0;
			x_out <= 0;
			y_out <= 0;
			plot <= 0;
		end
		else if(counter_case == 0 && counterreg > 0) begin
			x_out <= x_in + {5'd0, counterreg[5:3]};
			y_out <= y_in + {4'd0, counterreg[2:0]};
			counterreg <= counterreg - 6'd1;
		end
		else if(counter_case == 1 && counterreg > 0) begin
			if(key_in == 4'b1000) begin
				y_out <= y_in - 7'd3;
				x_out <= x_in;
			end
			if(key_in == 4'b0100) begin
				y_out <= y_in + 7'd3;
				x_out <= x_in;
			end
			if(key_in == 4'b0010) begin
				y_out <= y_in;
				x_out <= x_in - 7'd3;
			end
			if(key_in == 4'b0001) begin
				y_out <= y_in;
				x_out <= x_in + 7'd3;
			end
			counterreg <= counterreg - 6'd1;
		end
		else if(draw == 1) begin
			counterreg <= counter;
			x_out <= x_in;
			y_out <= y_in;
			plot <= 1;
		end
		else if(counter_case == 0 && counterreg == 0)begin
			plot <= 0;
		end
//		if(counterreg == 0 && counterregold == 1)begin
//			plot <= 1;
//		end
//		counterregold <= |counterreg;
	end
	
	
	//go, set to 1 on correct answer, 2 on wrong answer
	always @ (posedge clock) begin
		if(|key_in == 1 && key_in_old == 0) begin 
			if(|(key_in & key_answer)) begin
				go <= 1;
				score_counter <= score_counter + 8'd1;
			end
			else begin
				go <= 2;
				score_counter <= 0;
			end
		end
		else begin 
			go <= 0;
		end
		key_in_old <= |key_in;
	end
	
	//Rate divider for LEDR timer
	 always @(posedge clock)
	 begin
		if(!reset) begin
			timer <= 0;
			timer_dividor <= 50000000;
		end
		else if(start_timer == 1) begin 
			timer <= 10;
			timer_dividor <= 50000000;
		end
		else
			timer_dividor <= timer_dividor - 1;
		if (timer_dividor == 0 && timer > 0)
			timer <= timer - 1;
	 end
	 
	 assign LEDR[9] = timer > 9;
	 assign LEDR[8] = timer > 8;
	 assign LEDR[7] = timer > 7;
	 assign LEDR[6] = timer > 6;
	 assign LEDR[5] = timer > 5;
	 assign LEDR[4] = timer > 4;
	 assign LEDR[3] = timer > 3;
	 assign LEDR[2] = timer > 2;
	 assign LEDR[1] = timer > 1;
	 assign LEDR[0] = timer > 0;
	
	segdecoder sd2(
		.hex(HEX2[6:0]),
		.SW(score_counter[3:0])
	);
	
	segdecoder sd1(
		.hex(HEX1[6:0]),
		.SW(key_answer)
	);
	
	segdecoder sd0(
		.hex(HEX0[6:0]),
		.SW(key_in)
	);
	
	
//	segdecoder sd1(
//		.hex(HEX1[6:0]),
//		.SW(score_counter[7:4])
//	);
//	
//	segdecoder sd0(
//		.hex(HEX0[6:0]),
//		.SW(score_counter[3:0])
//	);
endmodule




module control(
    clock,
	 reset,
	 go,
	 key_answer,
	 counter,
	 counter_case,
	 colour,
	 x,
	 y,
	 draw,
	 start_timer,
	 HEX5,
	 HEX4,
	 HEX3);
	 
	 input clock;
	 input reset;
	 input [1:0] go;
	 output reg [3:0] key_answer; //up down left right
	 output reg [1:0] counter_case;
	 output reg [5:0] counter;
	 output reg [2:0] colour; //rgb
	 output reg [7:0] x; 
	 output reg [6:0] y;
	 output reg draw;
	 output reg start_timer;
	 output [6:0] HEX5;
	 output [6:0] HEX4;
	 output [6:0] HEX3;

    reg [3:0] current_state, next_state, random_state;
	 reg [19:0] plot_timer;
    
    localparam  S_RESET       = 4'd0,
					 S_WAIT			= 4'd1,
					 S_LOSE			= 4'd2,
					 S_START			= 4'd3,
					 S_DRED			= 4'd4,
					 S_DGREEN		= 4'd5,
					 S_DBLUE			= 4'd6,
					 S_DYELLOW		= 4'd7,
                S_RED   		= 4'd8,
                S_GREEN     	= 4'd9,
                S_BLUE			= 4'd10,
					 S_YELLOW		= 4'd11;
    
    // Next state logic aka our state table
    always@(*)
    begin: state_table 
            case (current_state)
					 S_START: next_state = (draw_counter == 0) ? S_DRED : S_START;
                S_RESET: next_state = (go == 1) ? S_WAIT : S_RESET;
					 S_WAIT: next_state = (go == 0) ? random_state : S_WAIT; // change to random state here
					 S_LOSE: next_state = (go == 1) ? S_RESET : next_state;
					 S_DRED: next_state = (draw_counter == 0) ? S_DGREEN : S_DRED;
					 S_DGREEN: next_state = (draw_counter == 0) ? S_DBLUE : S_DGREEN;
					 S_DBLUE: next_state = (draw_counter == 0) ? S_DYELLOW : S_DBLUE;
					 S_DYELLOW: next_state = (draw_counter == 0) ? S_RESET : S_DYELLOW;

					 S_RED: begin 
						if(go == 1) begin
							next_state = S_WAIT;
						end
						else if(go == 2) begin
							next_state = S_LOSE;
						end
					 end
					 S_GREEN: begin 
						if(go == 1) begin
							next_state = S_WAIT;
						end
						else if(go == 2) begin
							next_state = S_LOSE;
						end
					 end
					 S_BLUE: begin 
						if(go == 1) begin
							next_state = S_WAIT;
						end
						else if(go == 2) begin
							next_state = S_LOSE;
						end
					 end
					 S_YELLOW: begin 
						if(go == 1) begin
							next_state = S_WAIT;
						end
						else if(go == 2) begin
							next_state = S_LOSE;
						end
					 end
            default: next_state = S_START;
        endcase
    end // state_table
   

    // Output logic aka all of our datapath control signals
    always @(*)
    begin: enable_signals
        // By default make all our signals 0
		  draw = 0;
		  start_timer = 0;
        case (current_state)
				S_RESET: begin
               key_answer = 4'b1000;
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b111;
					x = 70;
					y = 50;
					draw = 1;
               start_timer = 0;
					end
				S_WAIT: begin
					counter = 1;
					counter_case = 1;
					colour = 3'b000;
					x = 73;
					y = 53;
					draw = 1;
               start_timer = 0;
					end
				S_LOSE: begin
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b111;
					x = 70;
					y = 50;
					draw = 1;
					start_timer = 0;
               end
				S_DRED: begin
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b100;
					x = 70;
					y = 0;
					draw = 1;
					start_timer = 0;
               end
				S_DGREEN: begin
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b010;
					x = 150;
					y = 50;
					draw = 1;
					start_timer = 0;
               end
				S_DBLUE: begin 
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b001;
					x = 0;
					y = 50;
					draw = 1;
					start_timer = 0;
					end
				S_DYELLOW: begin 
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b110;
					x = 70;
					y = 110;
					draw = 1;
					start_timer = 0;
					end
            S_RED: begin
               key_answer = 4'b1000;
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b100;
					x = 70;
					y = 50;
					draw = 1;
					start_timer = 1;
               end
            S_GREEN: begin
					key_answer = 4'b0001;
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b010;
					x = 70;
					y = 50;
					draw = 1;
					start_timer = 1;
               end		
				S_BLUE: begin 
               key_answer = 4'b0010;
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b001;
					x = 70;
					y = 50;
					draw = 1;
					start_timer = 1;
					end
				S_YELLOW: begin 
					key_answer = 4'b0100;
					counter = 6'b111111;
					counter_case = 0;
					colour = 3'b110;
					x = 70;
					y = 50;
					draw = 1;
					start_timer = 1;
					end
        default: begin
               key_answer = 0;
					counter = 0;
					counter_case = 0;
					colour = 0;
					x = 0;
					y = 0;
					draw = 0;
					start_timer = 0;
            end
        endcase
    end // enable_signals
   
    // current_state registers
    always@(posedge clock)
    begin: state_FFs
        if(!reset)
            current_state <= S_START;
        else
            current_state <= next_state;
    end // state_FFS
	 
	 reg [7:0] draw_counter = 1;
	 
	 //counter for drawing background squares
	 always@(posedge clock)
    begin
		  if(!reset)
            draw_counter <= 70; 
        else if(draw_counter == 0)
            draw_counter <= 70;
        else
            draw_counter <= draw_counter - 1;
    end
	 
	 //Use counter to generate next random state
    always@(posedge clock)
    begin
		  if(!reset)
            random_state <= 8;
        else if(random_state == 11)
            random_state <= 8;
        else
            random_state <= random_state + 1;
    end // state_FFS
	 
	 
	 //Rate divider for plot signal
//	 always @(posedge clock)
//	 begin
//		plot <= 0;
//		if(!reset) begin
//			plot <= 0;
//			plot_timer <= 833333;
//		end
//		else if(plot_timer == 0) begin 
//			plot_timer <= 833333;
//			plot <= 1;
//		end
//		else
//			plot_timer <= plot_timer - 1;
//	 end
//	 
	 
	segdecoder sd5(
		.hex(HEX5[6:0]),
		.SW(current_state)
	);
	
	segdecoder sd4(
		.hex(HEX4[6:0]),
		.SW(next_state)
	);
	
	segdecoder sd3(
		.hex(HEX3[6:0]),
		.SW({2'b00, go[1:0]})
	);

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
