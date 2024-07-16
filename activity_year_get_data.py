#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 19:28:36 2024

@author: tomaspacheco
"""


import glob
import tqdm
import json
import pandas as pd

dir_main = '/Users/tomaspacheco/Desktop/atpscraping_16jul/'
dir_input = dir_main + 'input/'
dir_output = dir_main + 'output/activity_years/'


def get_first_year(html_source):
    try:
        # Extract JSON data from HTML source
        parsed_json = json.loads(html_source.split("<pre>")[1].split('</pre>')[0])
        
        # Extract 'Won' data
        won = parsed_json.get('Won', 'No data')
        
        # Extract the first year of activity
        year = min(parsed_json.get('ActivityYearsList', []), default='No data')
        
    except (IndexError, AttributeError):
        # Handle cases where HTML structure is unexpected or JSON is malformed
        won = 'No data'
        year = 'No data'
    
    return {'year': year, 'won': won}


# Import all txts
dir_input = '/Users/tomaspacheco/Documents/GitHub/11julyatp/activity_years/'
files = glob.glob(dir_input + "*.txt")


# Get characteristics and save them in a dictionary
first_year = {}
for player in tqdm.tqdm(files):
    # Get player id
    p_id = player.split('source_')[1].split('.txt')[0]
    # Open source code
    html_source = open(player, 'r').read()
    # Extract characteristics
    first_year[p_id] = get_first_year(html_source)
    
data_activity = pd.DataFrame.from_dict(first_year, orient='index').reset_index()
data_activity.columns = ['id_player', 'first_activity_year', 'Won']   
        
    
data_activity.to_csv(dir_output+'data_activity.csv', index=False)

    
    

