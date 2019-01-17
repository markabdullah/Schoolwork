vlib work
vlog -timescale 1ns/1ns poly_function.v
vsim poly_function
log {/*}
add wave {CLOCK_50}
add wave {KEY[1:0]} 
add wave {SW[7:0]}
add wave {LEDR[7:0]} 

force {CLOCK_50} 0 0, 1 1 -r 2

force {KEY[0]} 0 0, 1 15, 0 95, 1 105

force {SW[7]} 0 0
force {SW[6]} 0 0
force {SW[5]} 0 0
force {SW[4]} 0 0
force {SW[3]} 0 0
force {SW[2]} 0 0, 1 130 
force {SW[1]} 1 0, 0 150
force {SW[0]} 0 0, 1 110, 0 130, 1 150

force {KEY[1]} 1 0, 0 10 -r 20

run 300ns





