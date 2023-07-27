"""
Description:        Script to read through logs, and extract lines based on the FilterQueries list.
                    Convert to CSV & Reformat DateTime column to usable Log Analytics Custom Table Format.
Author:             Roman Collyer
Version:            v1.6
Version History:    v1.0 - Initial Script
                    v1.1 - Added Statefile functionality
                    v1.2 - Added LogFile Size Tracking
                    v1.3 - Added Per-Run State for easy debugging
                    v1.4 - Added Regex Matching
                    v1.5 - Added Periodic State Dump for interrupted & cancelled runs.
                    v1.6 - Added Settings File
Notes:              Regex Query Execution time was 0 hours, 1 minutes, 26 seconds and 775 milliseconds.
                   !Regex Query Execution time was 0 hours, 0 minutes, 18 seconds and 690 milliseconds. 
"""
import os
import re
import json
import glob
from settings import *

#### STATE FILE ####
if Use_StateFile:
    if not os.path.exists(SPath):                                   # Make sure State path is created
        os.makedirs(SPath)
    SFile = SPath + datetime.today().strftime("%Y%m%d") + '.json'   # Set the State File
    completed_state_key = 'processed_files'                         # Set Completed State Key
    run_state_key = 'run' + datetime.today().strftime("_%H_%M_%S")  # Set Run State Key
    if os.path.isfile(SFile) and os.access(SFile, os.R_OK):         # Load Statefile if Exists or create Empty
        with open(SFile, 'r') as statefile:
            state = json.load(statefile)
    else:
        state = {
            completed_state_key: []
        }
    state[run_state_key] = []                                       # Append Run State Key
####################

# Join Path
SearchPath = Path + Match_Logs

def jprint(jtext):
    print(json.dumps(jtext, indent=4))

def not_processed(log_file):
    if Use_StateFile:
        if log_file not in state[completed_state_key]:
            return True
        else:
            return False
    else:
        return True
        
def write_state(state_type, data):
    if Use_StateFile:
        if state_type == 'run':
            state_key = run_state_key
        elif state_type == 'completed':
            state_key = completed_state_key
        state[state_key].append(data)

def logFilter(log_line):
    for q in FilterQueries:
        if Use_Regex:
            if re.search(q, log_line):
                return True
        else:
            if q in log_line:
                return True

def get_line_date(line):
    return f'{datetime.today().strftime("%Y-%m-%d_")}{line.replace("@","").split(" ")[0]}'
            
def output(line):
    line_date = get_line_date(line)             # '2022-09-14_08:50:03.6500'
    line_app = line.split(" ")[1]               # '[gctmi]'
    line_data = " ".join(line.split(" ")[2:])   # 'AgentLogin [134129,id656250,sNRDY] distributing EventAgentNotReady'
    return f'{line_date},{line_app},{line_data}'# Combine above
    
def check_dump_interval(idx):
    if idx % Dump_StateFile_Interval == 0:
        if idx != 0:
            state_file_dump()
    
def state_file_dump():
    if Use_StateFile:
        with open(SFile, 'w') as f:
            json.dump(state, f, indent=4)

for idx, textfile in enumerate(glob.glob(SearchPath)):
    check_dump_interval(idx)
    if not_processed(textfile):
        write_state('run', textfile)                        # Add to Current Run State           
        f = open(textfile, 'r')
        if os.path.getsize(textfile) >= Min_Full_Log_Size:
            write_state('completed', textfile)              # Add to Total Processed Files State
        for line in f:
            if logFilter(line):
                print(output(line), end='')

# Output State (Debugging)
#jprint(state)
# Dump State
state_file_dump()