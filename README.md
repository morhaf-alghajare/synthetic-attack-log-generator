# Synthetic Attack Log Generator

A powerful Python tool for generating realistic synthetic cybersecurity attack logs. Designed for testing SIEM systems, training security analysts, and validating detection algorithms.

## 🚀 Features

- **Multiple Attack Models**:
  - 🔑 **Credential Stuffing**: Simulates massive login attempts across user lists.
  - 💉 **SQL Injection**: Generates various payload patterns (UNION, boolean-based) with HTTP context.
  - 🔓 **Brute Force**: Simulates password attacks against SSH, RDP, FTP, and Telnet.
  - 📡 **Port Scanning**: Sequential, random, and common port reconnaissance patterns.
- **Distributed Attack Simulation**: Support for multiple source IPs (specific list or randomized) to simulate botnets or DDoS.
- **Realistic Data**: Includes realistic timestamps, HTTP status codes, payloads, and user agents.
- **JSON Output**: structured, easy-to-parse JSON logs saved with timestamped filenames.
- **CLI Interface**: Robust command-line arguments for full control over simulation parameters.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/synthetic-attack-logs.git
   cd synthetic-attack-logs
   ```

2. No external dependencies required! (Uses standard Python libraries: `json`, `random`, `datetime`, `uuid`, `argparse`).

3. Run the tool:
   ```bash
   python main.py --help
   ```

## 💻 Usage

```bash
python main.py [options]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-t, --attack-type` | Type of attack (`credential_stuffing`, `sql_injection`, `brute_force`, `port_scan`, `ddos`, `ransomware`, `exfiltration`, `all`) | `credential_stuffing` |
| `--target` | Target host, IP, or URL | `target.example.com` |
| `--src-ip` | Source IP(s). Single IP or comma-separated list | `192.168.1.100` |
| `--random-ips` | Flag to generate random source IPs (simulates distributed attack) | `False` |
| `--ip-count` | Number of random IPs to generate if using `--random-ips` | `3` |
| `--add-noise` | Add benign (normal) traffic to mix with attacks | `False` |
| `--noise-count` | Number of benign log entries to generate | `50` |
| `--count` | Number of attempts/logs to generate | Varies by attack |
| `--service` | Specific service for brute force (`ssh`, `rdp`, `ftp`, `telnet`) | `ssh` |
| `-o, --output-dir` | Directory to save JSON logs | `logs` |
| `--list-attacks` | List all available attack types and exit | - |

## 📖 Examples

### 1. Simple Credential Stuffing
```bash
python main.py -t credential_stuffing --target auth.company.com
```

### 2. Distributed Brute Force Attack (SSH)
Simulate an attack from 10 random IP addresses:
```bash
python main.py -t brute_force --service ssh --random-ips --ip-count 10 --count 50
```

### 3. Targeted SQL Injection
Simulate an attack from specific known malicious IPs:
```bash
python main.py -t sql_injection --src-ip "10.10.10.5,192.168.0.55" --target api.prod.com
```

### 4. Network Reconnaissance (Port Scan)
Scan a specific target IP:
```bash
python main.py -t port_scan --target 192.168.1.50 --count 100
```

### 5. Full Simulation Run
Generate logs for ALL attack types to create a diverse dataset:
```bash
python main.py -t all --random-ips --ip-count 5
```

### 6. Realistic Noise Generation
Add benign traffic (normal user activity) to mix with attack logs:
```bash
python main.py -t port_scan --add-noise --noise-count 200
```

### 7. New Attack Models (DDoS, Ransomware, Exfiltration)
```bash
# DDoS Attack (SYN Flood)
python main.py -t ddos --count 1000

# Ransomware Simulation
python main.py -t ransomware --count 50

# Data Exfiltration
python main.py -t exfiltration --count 100
```

## 📄 Output Format

Logs are saved as JSON files in the `logs/` directory (e.g., `logs/attack_sql_injection_20260122_190725.json`).

**Example JSON Entry:**
```json
{
  "timestamp": "2026-01-22T19:07:25.123456Z",
  "log_type": "web",
  "src_ip": "10.0.0.1",
  "target_url": "api.prod.com",
  "endpoint": "/api/users",
  "method": "GET",
  "payload": "' OR '1'='1",
  "status_code": 200,
  "action": "sql_injection_success",
  "attack_stage": "exploitation",
  "attack_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```
