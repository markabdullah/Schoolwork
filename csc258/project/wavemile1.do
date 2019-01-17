# Set the working dir, where all compiled Verilog goes.
vlib work

# Compile all Verilog modules in seventoonemux.v to working dir;
# could also have multiple Verilog files.
# The timescale argument defines default time unit
# (used when no unit is specified), while the second number
# defines precision (all times are rounded to this value)
vlog -timescale 1ns/1ns NotNot.v

# Load simulation using mux as the top level simulation module.
vsim -L altera_mf_ver datapath

# Log all signals and add some signals to waveform window.
log {/*}
# add wave {/*} would add all items in top level simulation module.
add wave {/*}



force {clock} 0 0, 1 5 -repeat 10

force {reset} 0 0, 1 20

force {key_answer[3]} 1 0
force {key_answer[2]} 0 0
force {key_answer[1]} 0 0
force {key_answer[0]} 0 0

force {counter[5]} 1 0
force {counter[4]} 1 0
force {counter[3]} 1 0
force {counter[2]} 1 0
force {counter[1]} 1 0
force {counter[0]} 1 0

force {key_in[3]} 0 0, 1 40, 0 60
force {key_in[2]} 0 0
force {key_in[1]} 0 0
force {key_in[0]} 0 0

force {counter_case[1]} 0 0
force {counter_case[0]} 0 0

force {x_in[9]} 0 0
force {x_in[8]} 0 0
force {x_in[7]} 0 0
force {x_in[6]} 0 0
force {x_in[5]} 0 0
force {x_in[4]} 0 0
force {x_in[3]} 0 0
force {x_in[2]} 0 0
force {x_in[1]} 0 0
force {x_in[0]} 0 0

force {y_in[8]} 0 0
force {y_in[7]} 0 0
force {y_in[6]} 0 0
force {y_in[5]} 0 0
force {y_in[4]} 0 0
force {y_in[3]} 0 0
force {y_in[2]} 0 0
force {y_in[1]} 0 0
force {y_in[0]} 0 0

force {colour_in[2]} 1 0
force {colour_in[1]} 0 0
force {colour_in[0]} 0 0

force {draw} 1 50


run 500ns
