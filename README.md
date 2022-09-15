# Log Analytics Custom Log Uploader

## Description
This project is designed to integrate a windows based application into Azure Log Analytics and Sentinel.

## How it Works
The `Upload-Script.ps1` is called (directly or using Scheduler), which uses the Python script `process_logs.py` to read and convert the text, and the output is piped to `Upload-AzMonitorLog.ps1` to ingest the logs into a Custom Table for Log Analytics / Sentinel.

## Settings
### Upload-Script.ps1:
Set the Sentinel Connector Options
```
# Sentinel Settings
$LogTypeName = 'TableName'
$WorkspaceId = 'xxxx'
$WorkspaceKey = 'xxxx'
# Optional
#$Proxy = 'http://xxxx:8080'
```
Also, set the path to the Ingestion script
```
function Upload-Logs {
	D:\Upload-AzMonitorLog.ps1 -WorkspaceId $WorkspaceId -WorkspaceKey $WorkspaceKey -LogTypeName $LogTypeName -AddComputerName -Proxy $Proxy
}
```
### settings.py

The settings are explained directly in the file [here](settings.py)


### Upload-AzMonitorLog.ps1

This script has been modified to allow for a `-Proxy` argument, but otherwise remains identical to the original [here][1].


[1]:https://www.powershellgallery.com/packages/Upload-AzMonitorLog/1.2/Content/Upload-AzMonitorLog.ps1