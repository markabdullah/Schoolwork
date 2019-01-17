# Set the working dir, where all compiled Verilog goes.
vlib work

# Compile all Verilog modules in seventoonemux.v to working dir;
# could also have multiple Verilog files.
# The timescale argument defines default time unit
# (used when no unit is specified), while the second number
# defines precision (all times are rounded to this value)
vlog -timescale 1ns/1ns NotNot.v

# Load simulation using mux as the top level simulation module.
vsim -L altera_mf_ver control

# Log all signals and add some signals to waveform window.
log {/*}
# add wave {/*} would add all items in top level simulation module.
add wave {/*}



force {clock} 0 0, 1 5 -repeat 10

force {reset} 0 0, 1 20

force {go[1]} 0 0
force {go[0]} 0 0, 1 50, 0 70, 1 200, 0 220


run 500ns
