import json
import os
import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path
from attack_models.credential_stuffing import generate_credential_stuffing_attack
from attack_models.sql_injection import generate_sql_injection_attack
from attack_models.brute_force import generate_brute_force_attack
from attack_models.port_scan import generate_port_scan_attack
from attack_models.noise import generate_benign_traffic
from attack_models.ddos import generate_ddos_attack
from attack_models.ransomware import generate_ransomware_attack
from attack_models.exfiltration import generate_exfiltration_attack


def generate_random_ip():
    """Generate a random IP address."""
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def parse_source_ips(src_ip_arg, random_ips, ip_count):
    """
    Parse source IP configuration.
    
    Args:
        src_ip_arg: Source IP argument (single IP or comma-separated list)
        random_ips: Whether to generate random IPs
        ip_count: Number of random IPs to generate
    
    Returns:
        List of source IP addresses
    """
    if random_ips:
        return [generate_random_ip() for _ in range(ip_count)]
    elif ',' in src_ip_arg:
        return [ip.strip() for ip in src_ip_arg.split(',')]
    else:
        return [src_ip_arg]


def save_logs_to_file(logs: list[dict], output_dir: str = "logs", attack_type: str = "unknown", is_noisy: bool = False) -> str:
    """
    Save generated logs to a JSON file in the specified directory.
    
    Args:
        logs: List of log entries to save
        output_dir: Directory to save logs to (default: "logs")
        attack_type: Type of attack for filename
        is_noisy: Whether logs contain noise
    
    Returns:
        Path to the saved file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "_noisy" if is_noisy else ""
    filename = f"attack_{attack_type}{suffix}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save logs to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    return filepath
    
def generate_credential_stuffing(args, src_ips):
    """Generate credential stuffing attack logs."""
    usernames = ["admin", "user1", "test", "root", "administrator", "guest", "user", "demo"]
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_credential_stuffing_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            usernames=usernames[:args.count] if args.count else usernames,
            host=args.target
        )
        all_logs.extend(logs)
    
    return all_logs, "credential_stuffing"


def generate_sql_injection_logs(args, src_ips):
    """Generate SQL injection attack logs."""
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_sql_injection_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_url=args.target,
            endpoint="/api/users"
        )
        all_logs.extend(logs)
    
    return all_logs, "sql_injection"


def generate_brute_force_logs(args, src_ips):
    """Generate brute force attack logs."""
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_brute_force_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_host=args.target,
            service=args.service if hasattr(args, 'service') else "ssh",
            username="root",
            attempt_count=args.count if args.count else 20
        )
        all_logs.extend(logs)
    
    return all_logs, "brute_force"


def generate_port_scan_logs(args, src_ips):
    """Generate port scanning attack logs."""
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_port_scan_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_ip=args.target,
            scan_type="common",
            port_count=args.count if args.count else 50
        )
        all_logs.extend(logs)
    
    return all_logs, "port_scan"


def generate_ddos_logs(args, src_ips):
    """Generate DDoS attack logs."""
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_ddos_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_ip=args.target,
            duration_seconds=60,
            intensity="high"
        )
        all_logs.extend(logs)
    
    return all_logs, "ddos"


def generate_ransomware_logs(args, src_ips):
    """Generate Ransomware attack logs."""
    all_logs = []
    
    # Ransomware is usually single-host, but we'll iterate IPs as "compromised hosts"
    for src_ip in src_ips:
        logs = generate_ransomware_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_host=args.target,
            file_count=args.count if args.count else 20
        )
        all_logs.extend(logs)
    
    return all_logs, "ransomware"


def generate_exfiltration_logs(args, src_ips):
    """Generate Data Exfiltration logs."""
    all_logs = []
    
    for src_ip in src_ips:
        logs = generate_exfiltration_attack(
            start_time=datetime.now(),
            src_ip=src_ip,
            target_ip="45.10.10.10", # Simulated external C2
            total_size_mb=args.count if args.count else 50
        )
        all_logs.extend(logs)
    
    return all_logs, "exfiltration"


def list_attacks():
    """List all available attack types."""
    attacks = {
        "credential_stuffing": "Credential stuffing attack with multiple username attempts",
        "sql_injection": "SQL injection attack with various payloads",
        "brute_force": "Brute force password attack (SSH/RDP/FTP)",
        "port_scan": "Network port scanning reconnaissance",
        "ddos": "Distributed Denial of Service (SYN Flood)",
        "ransomware": "Ransomware file encryption and system inhibition",
        "exfiltration": "Unauthorized data transfer to external IPs",
        "all": "Generate all attack types"
    }
    
    print("\n📋 Available Attack Types:\n")
    for attack, description in attacks.items():
        print(f"  • {attack:20s} - {description}")
    print()

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🔒 Synthetic Attack Log Generator - Generate realistic attack logs for testing and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single source IP (default)
  python main.py -t credential_stuffing
  
  # Multiple source IPs (comma-separated)
  python main.py -t sql_injection --src-ip "10.0.0.5,10.0.0.6,10.0.0.7"
  
  # Random source IPs for distributed attack simulation
  python main.py -t brute_force --random-ips --ip-count 5
  
  # Add noise (benign traffic) to make logs realistic
  python main.py -t port_scan --add-noise --noise-count 200
  
  # Custom parameters
  python main.py -t port_scan --target 192.168.1.100 --count 30
  
  # Generate all attack types
  python main.py -t all --random-ips --ip-count 3 --add-noise
  
  # List available attacks
  python main.py --list-attacks
        """
    )
    
    # ... (existing args) ...
    
    parser.add_argument(
        '-t', '--attack-type',
        choices=['credential_stuffing', 'sql_injection', 'brute_force', 'port_scan', 'ddos', 'ransomware', 'exfiltration', 'all'],
        default='credential_stuffing',
        help='Type of attack to simulate (default: credential_stuffing)'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='logs',
        help='Output directory for log files (default: logs)'
    )
    
    parser.add_argument(
        '--src-ip',
        default='192.168.1.100',
        help='Source IP address(es) - single IP or comma-separated list (default: 192.168.1.100)'
    )
    
    parser.add_argument(
        '--random-ips',
        action='store_true',
        help='Generate random source IPs for distributed attack simulation'
    )
    
    parser.add_argument(
        '--ip-count',
        type=int,
        default=3,
        help='Number of random IPs to generate when --random-ips is used (default: 3)'
    )
    
    parser.add_argument(
        '--add-noise',
        action='store_true',
        help='Add benign (normal) traffic noise to the log output'
    )
    
    parser.add_argument(
        '--noise-count',
        type=int,
        default=50,
        help='Number of benign log entries to generate (default: 50)'
    )
    
    parser.add_argument(
        '--target',
        default='target.example.com',
        help='Target host/IP/URL (default: target.example.com)'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        help='Number of attempts/iterations (varies by attack type)'
    )
    
    parser.add_argument(
        '--service',
        choices=['ssh', 'rdp', 'ftp', 'telnet'],
        default='ssh',
        help='Service to attack for brute force (default: ssh)'
    )
    
    parser.add_argument(
        '--list-attacks',
        action='store_true',
        help='List all available attack types and exit'
    )
    
    return parser.parse_args()


def main():
    """Generate synthetic attack logs for testing and analysis."""
    args = parse_arguments()
    
    # Handle list attacks command
    if args.list_attacks:
        list_attacks()
        return
    
    # Attack type to generator mapping
    attack_generators = {
        'credential_stuffing': generate_credential_stuffing,
        'sql_injection': generate_sql_injection_logs,
        'brute_force': generate_brute_force_logs,
        'port_scan': generate_port_scan_logs,
        'ddos': generate_ddos_logs,
        'ransomware': generate_ransomware_logs,
        'exfiltration': generate_exfiltration_logs
    }
    
    # Determine which attacks to run
    if args.attack_type == 'all':
        attack_types = ['credential_stuffing', 'sql_injection', 'brute_force', 'port_scan', 'ddos', 'ransomware', 'exfiltration']
    else:
        attack_types = [args.attack_type]
    
    # Parse source IPs
    src_ips = parse_source_ips(args.src_ip, args.random_ips, args.ip_count)
    
    print(f"\n🔒 Synthetic Attack Log Generator")
    print(f"{'=' * 60}")
    print(f"Source IPs: {', '.join(src_ips) if len(src_ips) <= 5 else f'{len(src_ips)} random IPs'}")
    if args.add_noise:
        print(f"Noise: Enabled ({args.noise_count} benign entries)")
    print(f"{'=' * 60}\n")
    
    total_logs = 0
    total_noise = 0
    
    # Generate logs for each attack type
    for attack_type in attack_types:
        print(f"Generating {attack_type.replace('_', ' ').title()} attack logs...")
        
        generator = attack_generators[attack_type]
        logs, attack_name = generator(args, src_ips)
        
        if logs:
            # Generate noise if requested
            if args.add_noise:
                # Find time range of attack
                timestamps = [log.get("timestamp") for log in logs if log.get("timestamp")]
                if timestamps:
                    # Convert string timestamps to datetime objects
                    # Format is ISO (might have "Z" or not based on previous code)
                    # The utils use isoformat() + "Z"
                    times = []
                    for ts in timestamps:
                        if ts.endswith('Z'):
                            ts = ts[:-1]
                        try:
                            # Try simple iso format first
                            times.append(datetime.fromisoformat(ts))
                        except ValueError:
                            pass
                    
                    if times:
                        start_time = min(times)
                        end_time = max(times)
                        # Add some buffer to windows
                        start_time -= timedelta(seconds=60)
                        end_time += timedelta(seconds=60)
                        
                        noise_logs = generate_benign_traffic(
                            start_time=start_time,
                            end_time=end_time,
                            hosts=[args.target],
                            count=args.noise_count
                        )
                        
                        logs.extend(noise_logs)
                        logs.sort(key=lambda x: x.get("timestamp", ""))
                        total_noise += len(noise_logs)
                        print(f"  ✓ Added {len(noise_logs)} benign noise entries")

            # Save to file
            filepath = save_logs_to_file(logs, args.output_dir, attack_name, args.add_noise)
            total_logs += len(logs)
            
            print(f"  ✓ Generated {len(logs)} total entries")
            print(f"  ✓ Saved to: {filepath}\n")
        else:
            print(f"  ✗ No logs generated\n")
    
    # Summary
    print(f"{'=' * 60}")
    print(f"📊 Summary: Generated {total_logs} log entries ({total_noise} noise)")
    print(f"📁 Output directory: {args.output_dir}\n")


if __name__ == "__main__":
    main()
