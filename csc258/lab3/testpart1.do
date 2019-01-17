vlib work
vlog -timescale 1ns/1ns mux7to1.v
vsim mux7to1
log {/*}
add wave {SW[9:0]}
add wave {LEDR[0]}

force {SW[9]} 0 0, 1 40 -r 80
force {SW[8]} 0 0, 1 20 -r 40
force {SW[7]} 0 0, 1 10 -r 20


force {SW[6]} 1
force {SW[5]} 0
force {SW[4]} 1
force {SW[3]} 0
force {SW[2]} 1
force {SW[1]} 1
force {SW[0]} 1

run 80ns





