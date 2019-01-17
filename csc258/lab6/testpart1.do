vlib work
vlog -timescale 1ns/1ns FSM.v
vsim FSM
log {/*}
add wave {KEY[0]} 
add wave {LEDR[9]} 
add wave {LEDR[2:0]} 
add wave {SW[1:0]}

force {KEY[0]} 0 0, 1 10 -r 20

force {SW[0]} 0 0, 1 20
force {SW[1]} 1 0, 0 120, 1 140

run 300ns





