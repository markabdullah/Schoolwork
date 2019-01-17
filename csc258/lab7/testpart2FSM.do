vlib work
vlog -timescale 1ns/1ns part2.v
vsim control


log {/*}
add wave {clock}
add wave {reset}
add wave {go}
add wave {ld_x}
add wave {ld_y}
add wave {plot}
add wave {current_state}


force {clock} 0 0, 1 5 -r 10
force {reset} 0 0, 1 10, 0 60, 1 70

force {go[1]} 0 0, 1 10, 0 20
force {go[0]} 0 0, 1 30, 0 40

run 200ns





