import random
from datetime import datetime, timedelta
import uuid

def generate_port_scan_attack(
    start_time: datetime,
    src_ip: str,
    target_ip: str,
    scan_type: str = "sequential",
    port_count: int = 50
):
    """
    Generate synthetic logs for a port scanning attack.
    
    Args:
        start_time: Starting timestamp for the attack
        src_ip: Source IP address of the attacker
        target_ip: Target IP being scanned
        scan_type: Type of scan (sequential, random, common)
        port_count: Number of ports to scan
    
    Returns:
        List of log entries representing the attack
    """
    attack_id = str(uuid.uuid4())
    logs = []
    
    # Common ports that are frequently targeted
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139,
        143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080
    ]
    
    # Port to service mapping
    port_services = {
        21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
        80: "http", 110: "pop3", 111: "rpcbind", 135: "msrpc", 139: "netbios",
        143: "imap", 443: "https", 445: "smb", 993: "imaps", 995: "pop3s",
        1723: "pptp", 3306: "mysql", 3389: "rdp", 5900: "vnc", 8080: "http-proxy"
    }
    
    current_time = start_time
    
    # Determine which ports to scan
    if scan_type == "common":
        ports = common_ports[:port_count]
    elif scan_type == "random":
        ports = random.sample(range(1, 65536), port_count)
    else:  # sequential
        start_port = random.randint(1, 1000)
        ports = list(range(start_port, start_port + port_count))
    
    # Randomly determine which ports are open
    open_ports = random.sample(ports, k=random.randint(2, min(5, len(ports))))
    
    for port in ports:
        # Determine port state
        if port in open_ports:
            state = "open"
            action = "port_open_detected"
        else:
            state = random.choice(["closed", "filtered"])
            action = f"port_{state}"
        
        # Get service name if known
        service = port_services.get(port, "unknown")
        
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "network",
            "src_ip": src_ip,
            "target_ip": target_ip,
            "port": port,
            "protocol": "tcp",
            "state": state,
            "service": service,
            "action": action,
            "scan_type": scan_type,
            "attack_stage": "reconnaissance",
            "attack_id": attack_id
        }
        
        logs.append(log)
        
        # Port scans are typically very fast
        current_time += timedelta(milliseconds=random.uniform(10, 100))
    
    return logs
