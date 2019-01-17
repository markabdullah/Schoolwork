vlib work
vlog -timescale 1ns/1ns ram32x4.v
vsim -L altera_mf_ver ram32x4
log {/*}
add wave {clock} 
add wave {address[4:0]} 
add wave {data[3:0]} 
add wave {wren}
add wave {q[3:0]}

force {clock} 0 0, 1 10 -r 20

force {data[3]} 1 0
force {data[2]} 1 0, 0 15
force {data[1]} 0 0, 1 15
force {data[0]} 0 0

force {address[4]} 1 0, 0 15, 1 35, 0 55
force {address[3]} 0 0, 1 15, 0 35, 1 55
force {address[2]} 1 0, 0 15, 1 35, 0 55
force {address[1]} 0 0, 1 15, 0 35, 1 55
force {address[0]} 1 0, 0 15, 1 35, 0 55

force {wren} 0 0, 1 5, 0 15, 1 25, 0 35


run 100ns





