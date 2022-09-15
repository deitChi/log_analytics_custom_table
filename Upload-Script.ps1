# Start Timer
$StartTime = get-date 

# Sentinel Settings
$LogTypeName = 'TableName'
$WorkspaceId = 'xxxx'
$WorkspaceKey = 'xxxx'
$Proxy = 'http://xxxx:8080'

function Upload-Logs {
	D:\Upload-AzMonitorLog.ps1 -WorkspaceId $WorkspaceId -WorkspaceKey $WorkspaceKey -LogTypeName $LogTypeName -AddComputerName -Proxy $Proxy
}

# Timestamp Filter, which logs Job Completion
filter timestamp {"$(Get-Date -Format G): $_"}

# Run Script, pipe output into Sentinel (separate script)
python .\process_logs.py
#python .\process_logs.py | Out-Null
#python .\process_logs.py | Upload-Logs | timestamp | Tee D:\csv_generator.log -Append

# Get End Timer
$RunTime = New-TimeSpan -Start $StartTime -End (get-date) 
# Timer Output
"Execution time was {0} hours, {1} minutes, {2} seconds and {3} milliseconds." -f $RunTime.Hours,  $RunTime.Minutes,  $RunTime.Seconds,  $RunTime.Milliseconds