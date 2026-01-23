import random
from datetime import datetime, timedelta
import uuid

def generate_ddos_attack(
    start_time: datetime,
    src_ip: str,
    target_ip: str,
    duration_seconds: int = 60,
    intensity: str = "high"
):
    """
    Generate synthetic firewall logs for a DDoS attack (SYN Flood).
    
    Args:
        start_time: Starting timestamp
        src_ip: Primary source IP (or spoofed)
        target_ip: Target IP
        duration_seconds: Duration of the attack
        intensity: high (many packets), medium, low
    
    Returns:
        List of log entries
    """
    attack_id = str(uuid.uuid4())
    logs = []
    
    # Packets per second based on intensity
    pps_map = {
        "high": (100, 500),
        "medium": (50, 100),
        "low": (10, 50)
    }
    min_pps, max_pps = pps_map.get(intensity, pps_map["high"])
    
    current_time = start_time
    end_time = start_time + timedelta(seconds=duration_seconds)
    
    # Common DDoS targets
    target_ports = [80, 443, 53, 8080]
    
    while current_time < end_time:
        # Batch of packets for this second
        num_packets = random.randint(min_pps, max_pps)
        
        # We won't generate a log for EVERY packet (too much noise), 
        # but a sample of them to represent the flood.
        sample_size = min(num_packets, 10) # Log 10 representative packets per burst
        
        for _ in range(sample_size):
            # 80% chance of being DENY during a DDoS as firewalls kick in
            action = "DENY" if random.random() > 0.2 else "ALLOW"
            dst_port = random.choice(target_ports)
            
            log = {
                "timestamp": current_time.isoformat() + "Z",
                "log_type": "firewall",
                "src_ip": src_ip, # In real DDoS, this varies wildly (spoofed), but using arg for consistency
                "dst_ip": target_ip,
                "dst_port": dst_port,
                "protocol": "TCP",
                "flags": "SYN",
                "packet_len": random.randint(40, 60), # Small SYN packets
                "action": action,
                "rule_id": "rate_limit_prevention" if action == "DENY" else "default_allow",
                "attack_id": attack_id
            }
            logs.append(log)
            
            # Micro-advances in time
            current_time += timedelta(microseconds=random.randint(100, 1000))
            
        current_time += timedelta(seconds=1)
        
    return logs
