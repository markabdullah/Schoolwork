`// Part 2 skeleton

module part2
	(
		CLOCK_50,						//	On Board 50 MHz
		// Your inputs and outputs here
      KEY,
      SW,
		// The ports below are for the VGA output.  Do not change.
		VGA_CLK,   						//	VGA Clock
		VGA_HS,							//	VGA H_SYNC
		VGA_VS,							//	VGA V_SYNC
		VGA_BLANK_N,						//	VGA BLANK
		VGA_SYNC_N,						//	VGA SYNC
		VGA_R,   						//	VGA Red[9:0]
		VGA_G,	 						//	VGA Green[9:0]
		VGA_B   						//	VGA Blue[9:0]
	);

	input			CLOCK_50;				//	50 MHz
	input   [9:0]   SW;
	input   [3:0]   KEY;

	// Declare your inputs and outputs here
	// Do not change the following outputs
	output			VGA_CLK;   				//	VGA Clock
	output			VGA_HS;					//	VGA H_SYNC
	output			VGA_VS;					//	VGA V_SYNC
	output			VGA_BLANK_N;			//	VGA BLANK
	output			VGA_SYNC_N;				//	VGA SYNC
	output	[9:0]	VGA_R;   				//	VGA Red[9:0]
	output	[9:0]	VGA_G;	 				//	VGA Green[9:0]
	output	[9:0]	VGA_B;	   			//	VGA Blue[9:0]
	
	wire resetn;
	assign resetn = KEY[0];
	
	wire [1:0] go;
	assign go[1:0] = {~KEY[3], ~KEY[1]};
	
	// Create the colour, x, y and writeEn wires that are inputs to the controller.
	wire [2:0] colour;
	wire [7:0] x;
	wire [6:0] y;
	wire writeEn;
	wire ld_x;
	wire ld_y;

	// Create an Instance of a VGA controller - there can be only one!
	// Define the number of colours as well as the initial background
	// image file (.MIF) for the controller.
	vga_adapter VGA(
			.resetn(resetn),
			.clock(CLOCK_50),
			.colour(colour),	
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
		.data_in(SW[6:0]),
		.ld_x(ld_x),
		.ld_y(ld_y),
		.colour(SW[9:7]),
		.x(x),
		.y(y),
		.c(colour));
		
		
    // Instansiate FSM control
    // control c0(...);
	control c0(
		.clock(CLOCK_50),
		.reset(resetn),
		.go(go),
		.ld_x(ld_x),
		.ld_y(ld_y),
		.plot(writeEn));
    
endmodule




module datapath(
	clock,
	reset,
	data_in,
	ld_x,
	ld_y,
	colour,
	x,
	y,
	c);
	 
	input clock;
	input reset;
	input [6:0] data_in;
	input [2:0] colour;
	input ld_x, ld_y;
	output reg [7:0] x;
	output reg [6:0] y;
	output reg [2:0] c;
	
	reg [3:0] counter;
	reg [7:0] temp_x;
	reg [6:0] temp_y;
    
   //
	always @ (posedge clock) begin
		if (!reset) begin
			temp_x <= 8'd0; 
			temp_y <= 7'd0; 
			c <= 3'd0; 
      end
      else begin
			c <= colour;
			if (ld_x)
				temp_x <= {1'b0, data_in[6:0]};
         if (ld_y)
				temp_y <= data_in[6:0];
      end
	end
	
	//counter
	always @ (posedge clock) begin
		if(!reset) begin
			counter <= 0;
			x <= 0;
			y <= 0;
		end
		else begin
			counter <= counter + 1;
			x <= temp_x[7:0] + {6'b0, counter[3:2]};
			y <= temp_y[6:0] + {5'b0, counter[1:0]};
		end
	end
	
endmodule




module control(
    clock,
	 reset,
	 go,
	 ld_x,
	 ld_y,
	 plot);
	 
	 input clock;
	 input reset;
	 input [1:0] go;
	 output reg ld_x;
	 output reg ld_y;
	 output reg plot;

    reg [2:0] current_state, next_state; 
    
    localparam  S_LOAD_X        = 4'd0,
                S_LOAD_X_WAIT   = 4'd1,
                S_LOAD_Y        = 4'd2,
                S_LOAD_Y_WAIT   = 4'd3,
					 S_PLOT          = 4'd4;
    
    // Next state logic aka our state table
    always@(*)
    begin: state_table 
            case (current_state)
                S_LOAD_X: next_state = go[1] ? S_LOAD_X_WAIT : S_LOAD_X; // Loop in current state until value is input
                S_LOAD_X_WAIT: next_state = go[1] ? S_LOAD_X_WAIT : S_LOAD_Y; // Loop in current state until go signal goes low
                S_LOAD_Y: next_state = go[0] ? S_LOAD_Y_WAIT : S_LOAD_Y; // Loop in current state until value is input
                S_LOAD_Y_WAIT: next_state = go[0] ? S_LOAD_Y_WAIT : S_PLOT; // Loop in current state until go signal goes low
            default:	next_state = S_LOAD_X;
        endcase
    end // state_table
   

    // Output logic aka all of our datapath control signals
    always @(*)
    begin: enable_signals
        // By default make all our signals 0
        ld_x = 1'b0;
        ld_y = 1'b0;

        case (current_state)
            S_LOAD_X: begin
                ld_x = 1'b1;
					 plot = 1'b0;
                end
            S_LOAD_Y: begin
                ld_y = 1'b1;
					 plot = 1'b0;
                end		
				S_PLOT: begin 
                plot = 1'b1;
            end
		
        // default:    // don't need default since we already made sure all of our outputs were assigned a value at the start of the always block
        endcase
    end // enable_signals
   
    // current_state registers
    always@(posedge clock)
    begin: state_FFs
        if(!reset)
            current_state <= S_LOAD_X;
        else
            current_state <= next_state;
    end // state_FFS
endmodule
