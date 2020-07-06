#!/usr/bin/env python

#imports
from visualize import *

#get file
file = '/Users/rjara/developer/python/covid/data/positivos_covid.csv'
df = load_data(input_file=file)

#get user input selection
selection = get_selection()

#visualize
final_df = get_final_df(selection, df)

plot(final_df)
