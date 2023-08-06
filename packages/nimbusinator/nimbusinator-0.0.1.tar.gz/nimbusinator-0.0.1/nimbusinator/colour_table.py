# RM Nimbus colour tables.  

# The Nimbus provided 16 colours in low-resolution mode.  In high
# resolution mode only 4 colours were available, although you can
# assign any of the 16 colours to the 4 slots in the palette.

# The full colour table here is also used in low-res mode.  The key
# is the Nimbus colour number and the value is the BGR composition.
colour_table = {
    #     B    G    R
    0:  [  0,   0,   0],    # black
    1:  [170,   0,   0],    # dark blue
    2:  [  0,   0, 170],    # dark red
    3:  [170,   0, 170],    # purple
    4:  [  0, 170,   0],    # dark green
    5:  [170, 170,   0],    # dark cyan
    6:  [  0,  84, 170],    # brown
    7:  [170, 170, 170],    # light grey
    8:  [ 84,  84,  84],    # dark grey
    9:  [255,  84,  84],    # light blue
    10: [ 84,  84, 255],    # light red
    11: [255,  84, 255],    # light purple
    12: [ 84, 255,  84],    # light green
    13: [255, 255,  84],    # light cyan
    14: [ 84, 255, 255],    # yellow
    15: [255, 255, 255]     # white
}

# Low-res default colours
low_res_default_colours = {
    0:  0,    # black
    1:  1,    # dark blue
    2:  2,    # dark red
    3:  3,    # purple
    4:  4,    # dark green
    5:  5,    # dark cyan
    6:  6,    # brown
    7:  7,    # light grey
    8:  8,    # dark grey
    9:  9,    # light blue
    10: 10,    # light red
    11: 11,    # light purple
    12: 12,    # light green
    13: 13,    # light cyan
    14: 14,    # yellow
    15: 15    # white
}

# High-res default colours
high_res_default_colours = {
    0: 1,                   # dark blue
    1: 4,                   # dark green
    2: 10,                  # light red
    3: 15                   # white
}
