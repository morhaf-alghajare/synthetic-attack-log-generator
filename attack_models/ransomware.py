import random
from datetime import datetime, timedelta
import uuid

def generate_ransomware_attack(
    start_time: datetime,
    src_ip: str, # Attacker C2 or lateral movement source
    target_host: str,
    file_count: int = 50
):
    """
    Generate synthetic system logs for a Ransomware attack.
    
    Args:
        start_time: Starting timestamp
        src_ip: Source IP (C2/Attacker)
        target_host: Hostname being encrypted
        file_count: Number of files 'encrypted'
    
    Returns:
        List of log entries
    """
    attack_id = str(uuid.uuid4())
    logs = []
    current_time = start_time
    
    # 1. Initial Access / Execution (simulated CMD execution)
    commands = [
        ("vssadmin.exe delete shadows /all /quiet", "Stopping backup services"),
        ("wbadmin.exe DELETE SYSTEMSTATEBACKUP", "Deleting system state backups"),
        ("bcdedit.exe /set {default} recoveryenabled No", "Disabling recovery")
    ]
    
    for cmd, desc in commands:
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "process_audit",
            "host": target_host,
            "user": "SYSTEM",
            "process_name": "cmd.exe",
            "command_line": cmd,
            "event_id": 4688,
            "action": "Process Created",
            "parent_process": "powershell.exe",
            "attack_stage": "inhibit_system_recovery",
            "attack_id": attack_id
        }
        logs.append(log)
        current_time += timedelta(seconds=random.randint(1, 5))

    # 2. File Encryption Phase
    target_dirs = ["C:\\Users\\Admin\\Documents\\", "C:\\Users\\Admin\\Pictures\\", "D:\\Data\\Finance\\"]
    extensions = ["docx", "pdf", "xlsx", "jpg", "sql"]
    
    for _ in range(file_count):
        directory = random.choice(target_dirs)
        filename = f"report_{random.randint(1000, 9999)}.{random.choice(extensions)}"
        enc_filename = filename + ".locked"
        
        # File Modification Log
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "file_audit",
            "host": target_host,
            "user": "Admin",
            "file_path": directory + enc_filename,
            "original_file": directory + filename,
            "event_id": 4663,
            "action": "FileWrite",
            "process": "unknown_encryptor.exe",
            "details": "An attempt was made to access an object.",
            "attack_id": attack_id
        }
        logs.append(log)
        current_time += timedelta(milliseconds=random.randint(10, 200)) # FAST encryption
        
    # 3. Ransom Note Creation
    log = {
        "timestamp": current_time.isoformat() + "Z",
        "log_type": "file_audit",
        "host": target_host,
        "user": "Admin",
        "file_path": "C:\\Users\\Admin\\Desktop\\READ_ME_NOW.txt",
        "event_id": 11, # Sysmon FileCreate
        "action": "FileCreate",
        "process": "unknown_encryptor.exe",
        "content_preview": "YOUR FILES HAVE BEEN ENCRYPTED...",
        "attack_id": attack_id
    }
    logs.append(log)
    
    return logs
