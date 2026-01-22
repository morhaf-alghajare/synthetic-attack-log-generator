import random
from datetime import datetime, timedelta
import uuid

def generate_benign_traffic(
    start_time: datetime,
    end_time: datetime = None,
    src_ips: list[str] = None,
    hosts: list[str] = None,
    count: int = 50
):
    """
    Generate benign (normal) traffic logs to mix with attack logs.
    
    Args:
        start_time: Start of the time window
        end_time: End of the time window (defaults to start_time + 1h if None)
        src_ips: List of source IPs to use (if None, generates random trusted IPs)
        hosts: List of target hosts
        count: Number of log entries to generate
    
    Returns:
        List of log entries
    """
    if end_time is None:
        end_time = start_time + timedelta(hours=1)
        
    if src_ips is None:
        # Generate some "trusted" internal/ISP IPs
        src_ips = [f"192.168.1.{i}" for i in range(50, 200)]
        
    if hosts is None:
        hosts = ["web.example.com", "auth.example.com", "api.example.com"]
        
    logs = []
    
    # Common user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
    ]
    
    # Common endpoints
    endpoints = ["/", "/home", "/about", "/contact", "/products", "/login", "/dashboard", "/profile", "/assets/style.css", "/assets/logo.png", "/js/app.js"]
    
    # Common usernames for benign auth
    usernames = ["jdoe", "asmith", "brucew", "clarkk", "diana", "barry", "hal", "arthur"]
    
    time_window = (end_time - start_time).total_seconds()
    
    for _ in range(count):
        # random time within window
        log_time = start_time + timedelta(seconds=random.uniform(0, time_window))
        src_ip = random.choice(src_ips)
        host = random.choice(hosts)
        
        # Decide type of traffic: 80% web, 20% auth
        traffic_type = "web" if random.random() < 0.8 else "auth"
        
        log = {
            "timestamp": log_time.isoformat() + "Z",
            "src_ip": src_ip,
            "host": host,
            "attack_stage": "benign", # Marking as benign for clarity
            "id": str(uuid.uuid4())
        }
        
        if traffic_type == "web":
            endpoint = random.choice(endpoints)
            method = "GET" if endpoint != "/login" else random.choice(["GET", "POST"])
            status_code = random.choice([200, 200, 200, 301, 302, 404])
            
            log.update({
                "log_type": "web",
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "user_agent": random.choice(user_agents),
                "response_time_ms": round(random.uniform(20, 500), 2)
            })
            
            # Action based on status
            if status_code < 400:
                log["action"] = "page_view"
            else:
                log["action"] = "error"
                
        else: # auth
            username = random.choice(usernames)
            # 90% success for benign users
            success = random.random() < 0.9
            
            log.update({
                "log_type": "auth",
                "username": username,
                "action": "login_success" if success else "login_failed",
                "result": "accepted" if success else "rejected"
            })
            
        logs.append(log)
        
    # Sort by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    return logs
