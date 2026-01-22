import random
from datetime import datetime, timedelta
import uuid

def generate_brute_force_attack(
    start_time: datetime,
    src_ip: str,
    target_host: str,
    service: str = "ssh",
    username: str = "root",
    attempt_count: int = 20,
    success_index: int = None
):
    """
    Generate synthetic logs for a brute force attack.
    
    Args:
        start_time: Starting timestamp for the attack
        src_ip: Source IP address of the attacker
        target_host: Target host/IP
        service: Service being attacked (ssh, rdp, ftp)
        username: Username being targeted
        attempt_count: Number of password attempts
        success_index: Index of attempt that succeeds (random if None)
    
    Returns:
        List of log entries representing the attack
    """
    attack_id = str(uuid.uuid4())
    logs = []
    
    # Common passwords used in brute force attacks
    common_passwords = [
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "dragon",
        "123123", "baseball", "iloveyou", "trustno1", "1234567890",
        "sunshine", "master", "welcome", "shadow", "ashley",
        "football", "jesus", "michael", "ninja", "mustang"
    ]
    
    # Service-specific ports
    service_ports = {
        "ssh": 22,
        "rdp": 3389,
        "ftp": 21,
        "telnet": 23
    }
    
    port = service_ports.get(service.lower(), 22)
    current_time = start_time
    
    if success_index is None:
        # Randomly decide if attack succeeds
        # Ensure we don't error if attempt_count is small
        max_index = min(attempt_count - 1, len(common_passwords) - 1)
        start_index = min(10, max_index)
        success_index = random.randint(start_index, max_index)
    
    for i in range(attempt_count):
        password = common_passwords[i % len(common_passwords)]
        
        # Determine if this attempt succeeds
        if i == success_index:
            action = "login_success"
            result = "accepted"
        else:
            action = "login_failed"
            result = "rejected"
        
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "auth",
            "src_ip": src_ip,
            "target_host": target_host,
            "port": port,
            "service": service,
            "username": username,
            "password_hash": f"md5:{hash(password) % 100000:05d}",  # Simulated hash
            "action": action,
            "result": result,
            "attack_stage": "initial_access",
            "attack_id": attack_id
        }
        
        logs.append(log)
        
        # Increment time between attempts (brute force is typically faster)
        current_time += timedelta(seconds=random.uniform(0.5, 2.0))
        
        # Stop after successful login
        if action == "login_success":
            break
    
    return logs
