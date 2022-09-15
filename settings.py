from datetime import datetime

# Log Path                  Set this to the folder that contains the logs we wish to ingest
Path = 'C:\\Path\\to\\Logs\\'

# Use State                 Whether or not to use the Statefile
Use_StateFile = True

# Dump State Every n Processed Files
Dump_StateFile_Interval = 10

# State Path                Set this to the folder that will contain the statefiles (one per day) for the logs which have been processed.
SPath = 'C:\\Path\\to\\State\\'

# Size Cutoff (in bytes)    Any files above this size, will be added to the statefile, and not processed on the next run.
#                           A file smaller than this value, will be processed, but not added to state.
Min_Full_Log_Size = 20480000

# Collect Logs From         Set the date that the Files are collected from. This can be a string, but the format should match the logs.
Match_Date = datetime.today().strftime("%Y%m") + '14'
#Date = datetime.today().strftime("%Y%m%d")

# Full Log Match String
Match_Logs = '*' + Match_Date + "*.log"

# Use Regex Filter          Select if the Filtering should support Regex (much slower, see notes)
Use_Regex = False

# Filter the following Logs - separate additional queries with comma
# Regex Example
# FilterQueries = [
#     "\] AgentLogin",
#     "^[13]55 Error"
# ]
# Non Regex Example (Faster)
FilterQueries = [
    "] AgentLogin",
    "155 Error",
    "355 Error"
]