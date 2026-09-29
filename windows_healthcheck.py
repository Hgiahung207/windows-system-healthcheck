'''
* PSEUDOCODE:
import win32api
import win32net
import win32service
import win32process
import win32file
import time

def run_healthcheck():
    report = [] to store the health check report
    time.strftime("%Y/%m/%d %H:%M:%S") for current date
    report.append("-" to add a header to the report)
    report.append("{times}") to add the report generation time to the report

    #MODULE 1: Get Computer Name
    Use win32api.GetComputerName() to get the computer name and add it to the report

    #MODULE 2: Get OS Info
    Use win32net.NetServerGetInfo to retrieve the server information and add the platform ID and version to the report

    #MODULE 3: Check the status of important services
    Make a list of essential services to check.That includes 'wuauserv', 'WinDefend' and 'EventLog'
    Open the service control manager using win32service.OpenSCManager
        Try to open the service and check its status
            - if status code is 4, log as RUNNING
            - Otherwise record as STOPPED and add to a warning list
            - If the service is not found, mark it as Not Found and add to warning list 
            - If any services are in the warning list, append a warning line listing them
    
    #MODULE 4: Check for important process
    Use win32process.EnumProcesses() to get a list of running processes
    For each process, check if it’s the important one (explorer.exe, svchost.exe, winlogon.exe):
    - If found set flag = True
    After loop:
        - Report total number of running processes and add to report
        - Add a line indicating if the important process is running or not
    
    #MODULE 5: 
    Check disk space on C: drive
    Use win32file.GetDiskFreeSpaceEx to get free and total space
    Calculate free space in GB and percentage free

    if percentage free is less than 15%, add a warning line to the report

    notify user that the health check is complete and save the report to a text file
    
    if __name__ == "__main__":
    run_healthcheck()
'''

import win32api
import win32net
import win32service
import win32process
import win32file
import time

def run_healthcheck():
    report = []
    times = time.strftime("%Y/%m/%d %H:%M:%S")
    report.append("---------------- WINDOWS SYSTEM HEALTH REPORT -----------------\n")

    report.append(f"Report Generated on: {times}")
 
    report.append(f"\n---------------------- BASIC SYSTEM INFO ----------------------\n")
    #MODULE 1: Get Computer Name
    report.append(f"Computer Name: {win32api.GetComputerName()}")
 
    #MODULE 2: Get Operating System Information
    server_information = win32net.NetServerGetInfo(None, 101)
    report.append(f"Operation System Platform: {server_information['platform_id']}, Version: {server_information['version_major']}.{server_information['version_minor']}\n")
    report.append("---------- CHECKING THE STATUS OF IMPORTANT SERVICES ----------\n")
    #MODULE 3: Check the status of important services
    service_need_to_check = ["wuauserv", "WinDefend","EventLog","Spooler"]
    stopped_services = []
    scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
    for service_name in service_need_to_check:
        try:
            svc = win32service.OpenService(scm, service_name, win32service.SERVICE_QUERY_STATUS)
            status = win32service.QueryServiceStatus(svc)
            state = "RUNNING" if status[1] == 4 else "STOPPED"
            report.append(f"{service_name} Service Status: {state}")
 
            if state == "STOPPED":
                stopped_services.append(service_name)
        except:
            report.append(f"{service_name} Service: Not Found")
            stopped_services.append(service_name)
 
    if stopped_services:
        stopped_str = ", ".join(stopped_services)
        report.append(f"\n* WARNING: THE FOLLOWING SERVICES ARE STOPPED -> {stopped_str}")
    
    report.append("\n----------------- CHECKING IMPORTANT PROCESSES ----------------\n")
    # MODULE 4: Check for important process
    important_process = ["explorer.exe", "svchost.exe", "winlogon.exe"]
    pid_list = win32process.EnumProcesses()
    found_status = {name: False for name in important_process}

    for pid in pid_list:
        if pid == 0:
            continue
        try:
            handle = win32api.OpenProcess(0x0400 | 0x0010, False, pid)
            exe_name = win32process.GetModuleFileNameEx(handle, 0).lower()
            for name in important_process:
                if name in exe_name:
                    found_status[name] = True
            win32api.CloseHandle(handle)
        except:
            continue

    report.append(f"Total running processes: {len(pid_list)}")
    for name in important_process:
        status = "YES" if found_status[name] else "NO"
        report.append(f"{name} running: {status}")
 
    report.append("\n----------------- CHECKING C: DRIVE FREE SPACE ----------------")
    # MODULE 5:
    free, total, _ = win32file.GetDiskFreeSpaceEx("C:\\")
    free_gb = free / (1024**3)
    percent_free = (free / total) * 100
 
    report.append(f"\nC: Drive Free Space: {free_gb:.2f} GB ({percent_free:.1f}% free)")
 
    if percent_free < 15:
        report.append(f"\n* WARNING: DRIVE C IS RUNNING LOW ON SPACE, IS ONLY {percent_free:.1f}% FREE")
    report.append("\n------------------------- END OF REPORT ------------------------")
    print("Health Check Now Complete, to view the report, please check the system_report.txt file in the current directory.") #Notice in the cmd that the report is saved to a text file
 
    # Note: The report is saved to a text file 
    final_text = "\n".join(report)
    with open("system_report.txt", "w") as f:
        f.write(final_text)
 
    win32api.MessageBox(0, "Health Check Now Complete!", "Success", 0) #Notice in message box that the health check is complete
 
if __name__ == "__main__":
    run_healthcheck()
 