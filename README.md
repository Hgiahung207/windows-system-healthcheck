* Windows System Health Check Tool

Automated Python script designed for System Administrators to monitor essential Windows metrics and generate health status reports.
* Features 
  - Computer Name: Identifies host machine for multi-device auditing.
  - OS Information: Displays OS platform and version.
  - Service Monitoring: Audits critical background services (`wuauserv`, `WinDefend`, `EventLog`, `Spooler`).
  - Process Check: Scans active processes for essential system components (`explorer.exe`, `svchost.exe`, `winlogon.exe`).
  - Disk Space Check: Calculates C: drive free space and flags warnings if available space is below 15%.
  - Output: Logs report to `system_report.txt` and notifies via GUI Message Box.

* Requirements
  - OS: Windows
  - Python 3.x
  - `pywin32` library
