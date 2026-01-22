import random
from datetime import datetime, timedelta
import uuid

def generate_sql_injection_attack(
    start_time: datetime,
    src_ip: str,
    target_url: str,
    endpoint: str = "/api/users",
    success_index: int = None
):
    """
    Generate synthetic logs for a SQL injection attack.
    
    Args:
        start_time: Starting timestamp for the attack
        src_ip: Source IP address of the attacker
        target_url: Target URL/domain
        endpoint: API endpoint being targeted
        success_index: Index of payload that succeeds (random if None)
    
    Returns:
        List of log entries representing the attack
    """
    attack_id = str(uuid.uuid4())
    logs = []
    
    # Common SQL injection payloads
    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "admin' --",
        "' UNION SELECT NULL--",
        "' UNION SELECT username, password FROM users--",
        "1' AND SLEEP(5)--",
        "'; DROP TABLE users--",
        "' OR 'a'='a",
    ]
    
    current_time = start_time
    
    if success_index is None:
        success_index = random.randint(3, len(payloads) - 1)
    
    for i, payload in enumerate(payloads):
        # Determine if this attempt succeeds
        if i == success_index:
            status_code = 200
            action = "sql_injection_success"
            response_time = random.uniform(0.8, 2.5)
        elif i < success_index:
            status_code = random.choice([400, 403, 500])
            action = "sql_injection_blocked"
            response_time = random.uniform(0.1, 0.5)
        else:
            # After success, might continue probing
            status_code = random.choice([200, 500])
            action = "sql_injection_exploit"
            response_time = random.uniform(1.0, 3.0)
        
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "web",
            "src_ip": src_ip,
            "target_url": target_url,
            "endpoint": endpoint,
            "method": "GET",
            "payload": payload,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "action": action,
            "attack_stage": "initial_access" if i <= success_index else "exploitation",
            "attack_id": attack_id,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        logs.append(log)
        
        # Increment time between attempts
        current_time += timedelta(seconds=random.uniform(1.0, 4.0))
        
        # Stop after a few exploitation attempts
        if i > success_index and i >= success_index + 2:
            break
    
    return logs
