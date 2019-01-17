vlib work
vlog -timescale 1ns/1ns morse_decoder.v
vsim morse_decoder
log {/*}
add wave {CLOCK_50}
add wave {LEDR[0]}
add wave {SW[2:0]}
add wave {KEY[1:0]}
add wave {Q[12:0]}
add wave {shift}
add wave {count}


force {CLOCK_50} 0 0, 1 5 -r 10

force {SW[2]} 0
force {SW[1]} 0
force {SW[0]} 0
force {KEY[0]} 0 0, 1 10
force {KEY[1]} 1 0, 0 10, 1 20


run 300ns





