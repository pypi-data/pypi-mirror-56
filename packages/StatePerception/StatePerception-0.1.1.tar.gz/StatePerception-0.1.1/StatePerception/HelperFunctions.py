"""
@author: Torben Gräber
"""

import os
import pickle as pk

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_color_setup(colour_start,colour_end,num_colours):
    # colour Setup
    colours = []
    for i in range(num_colours):
        ratio = i/(num_colours-1)
        colour = ratio*colour_end + (1-ratio)*colour_start
        colours.append(colour)
    return colours

def get_color_setup_3_colours(colour_start,colour_mid,colour_end,num_colours):
    # colour Setup
    colours = []
    for i in range(num_colours):
        ratio = i/(num_colours-1)
        if ratio<0.5:
            ratio_ = ratio*2
            colour = (1-ratio_)*colour_start + ratio_*colour_mid
        else:
            ratio_ = ratio*2-1
            colour = (1-ratio_)*colour_mid + ratio_*colour_end
        colours.append(colour)
    return colours

def save_pickle_file(savename,data):
    with open(savename,'wb') as f:
        pk.dump(data,f)
        
def load_pickle_file(savename):
    with open(savename,'rb') as f:
        loadlist = pk.load(f)
    return loadlist