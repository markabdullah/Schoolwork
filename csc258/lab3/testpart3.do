vlib work
vlog -timescale 1ns/1ns ALU.v
vsim ALU
log {/*}
add wave {SW[7:0]}
add wave {LEDR[7:0]}
add wave {KEY[2:0]}
add wave {HEX0[6:0]}
add wave {HEX1[6:0]}
add wave {HEX2[6:0]}
add wave {HEX2[6:0]}
add wave {HEX4[6:0]}
add wave {HEX5[6:0]}

#force {SW[7]} 0 0, 1 80 -r 160
#force {SW[6]} 0 0, 1 40 -r 80
#force {SW[5]} 0 0, 1 20 -r 40
#force {SW[4]} 0 0, 1 10 -r 20

#KEY values
force {KEY[2]} 0 0, 1 40 -r 80
force {KEY[1]} 0 0, 1 20 -r 40
force {KEY[0]} 0 0, 1 10 -r 20

#first number
force {SW[7]} 0
force {SW[6]} 0
force {SW[5]} 1
force {SW[4]} 0

#second number
force {SW[3]} 0
force {SW[2]} 1
force {SW[1]} 0
force {SW[0]} 1

run 60ns





