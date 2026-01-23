import random
from datetime import datetime, timedelta
import uuid

def generate_exfiltration_attack(
    start_time: datetime,
    src_ip: str, # Internal compromised host
    target_ip: str, # External attacker IP
    total_size_mb: int = 50,
    protocol: str = "https"
):
    """
    Generate synthetic proxy/flow logs for Data Exfiltration.
    
    Args:
        start_time: Starting timestamp
        src_ip: Internal source IP
        target_ip: External destination IP
        total_size_mb: Total amount of data to exfiltrate in MB
        protocol: Transmission protocol (https, dns, ftp)
    
    Returns:
        List of log entries
    """
    attack_id = str(uuid.uuid4())
    logs = []
    current_time = start_time
    
    # Convert to bytes
    remaining_bytes = total_size_mb * 1024 * 1024
    
    chunk_size_min = 100 * 1024 # 100 KB
    chunk_size_max = 5 * 1024 * 1024 # 5 MB
    
    domains = ["update-windows-service.com", "cdn-content-delivery.org", "backup-cloud-storage.net"]
    dest_domain = random.choice(domains)
    
    while remaining_bytes > 0:
        chunk = random.randint(chunk_size_min, chunk_size_max)
        if chunk > remaining_bytes:
            chunk = remaining_bytes
            
        remaining_bytes -= chunk
        
        # Duration depends on "speed" (simulating bandwidth)
        duration_sec = chunk / (1024 * 1024) # Assume 1MB/s roughly
        
        log = {
            "timestamp": current_time.isoformat() + "Z",
            "log_type": "proxy",
            "src_ip": src_ip,
            "dst_ip": target_ip,
            "dest_domain": dest_domain,
            "dst_port": 443 if protocol == "https" else 80,
            "protocol": protocol,
            "http_method": "POST",
            "bytes_out": chunk,
            "bytes_in": random.randint(200, 1000), # Small response
            "status_code": 200,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            "duration_ms": int(duration_sec * 1000),
            "action": "allowed",
            "attack_id": attack_id
        }
        logs.append(log)
        
        # Gap between chunks (jitter)
        current_time += timedelta(seconds=duration_sec + random.randint(1, 10))
        
    return logs
