import random
from datetime import datetime, timedelta
import uuid

def generate_credential_stuffing_attack(
    start_time: datetime,
    src_ip: str,
    usernames: list[str],
    host: str,
    success_index: int = None
):
    """
    Generate synthetic logs for a credential stuffing attack.
    
    Args:
        start_time: Starting timestamp for the attack
        src_ip: Source IP address of the attacker
        usernames: List of usernames to attempt
        host: Target host/service
        success_index: Index of username that succeeds (random if None)
    
    Returns:
        List of log entries representing the attack
    """
    attack_id = str(uuid.uuid4())
    logs = []
    
    current_time = start_time
    
    if success_index is None:
        success_index = random.randint(0, len(usernames) - 1)
    
    for i, username in enumerate(usernames):
        action = "login_success" if i == success_index else "login_failed"

        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "auth",
            "src_ip": src_ip,
            "username": username,
            "host": host,
            "action": action,
            "attack_stage": "initial_access",
            "attack_id": attack_id
        }

        logs.append(log)

        current_time += timedelta(seconds=random.randint(2, 6))

        if action == "login_success":
            break

    return logs
