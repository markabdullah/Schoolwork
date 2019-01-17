vlib work
vlog -timescale 1ns/1ns ripplecarryadder.v
vsim ripplecarryadder
log {/*}
add wave {SW[8:0]}
add wave {LEDR[4:0]}

force {SW[8]} 0

#first number
force {SW[7]} 0 0, 1 80 -r 160
force {SW[6]} 0 0, 1 40 -r 80
force {SW[5]} 0 0, 1 20 -r 40
force {SW[4]} 0 0, 1 10 -r 20

#second number
force {SW[3]} 1
force {SW[2]} 0
force {SW[1]} 0
force {SW[0]} 1

run 160ns





