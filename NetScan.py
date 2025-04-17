import os
import socket
import time
import speedtest

# Color Definitions
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"

# Welcome Message
def print_welcome_message():
    print(RED) 
    print(" _   _      _   ____                  ")
    print("| \\ | | ___| |_/ ___|  ___ __ _ _ __  ") 
    print("|  \\| |/ _ \\ __\\___ \\ / __/ _` | '_ \\ ")  
    print("| |\\  |  __/ |_ ___) | (_| (_| | | | |")  
    print("|_| \\_|\\___|\\__|____/ \\___\\__,_|_| |_|")  
    print(RESET)  

# Write to log file
def log_to_file(message):
    with open("logs.txt", "a") as log_file:
        log_file.write(message + "\n")

# Get Hostname
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        pass
    try:
        output = os.popen(f'nbtstat -A {ip}').read()
        for line in output.splitlines():
            if "<00>" in line and "UNIQUE" in line:
                return line.strip().split()[0]
    except:
        pass
    return f"{YELLOW}Hostname not found{RESET}"

# Get MAC Address
def get_mac(ip):
    try:
        output = os.popen("arp -a " + ip).read()
        for line in output.split('\n'):
            if ip in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
        return f"{YELLOW}MAC address not found{RESET}"
    except:
        return f"{RED}MAC query not supported{RESET}"

# Scan devices on the network
def get_devices_on_network(target_ip):
    ip_parts = target_ip.split('.')
    base_ip = '.'.join(ip_parts[:3]) + '.'
    devices = []

    print(f"\n🔍 {CYAN}{base_ip}1 - {base_ip}254{RESET} range network scan is starting...\n")
    start_time = time.time()

    for i in range(1, 255):
        ip = base_ip + str(i)
        response = os.system(f"ping -n 1 -w 1 {ip} > nul")  # For Windows
        if response == 0:
            hostname = get_hostname(ip)
            mac = get_mac(ip)
            devices.append((ip, hostname, mac))
            print(f"{GREEN}✅ {ip:15} | {hostname:25} | {mac}{RESET}")
    
    duration = time.time() - start_time
    print(f"\n{GREEN}✅ Scan completed. Total devices found: {len(devices)}{RESET}")
    print(f"{CYAN}⏱️ Scan time: {round(duration, 2)} seconds{RESET}\n")
    
    log_message = f"Network Scan Results: {len(devices)} devices found, Scan time: {round(duration, 2)} seconds"
    log_to_file(log_message)

    return devices

# Speed test
def run_speed_test():
    print("\n🌐 Starting internet speed test...\n")
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping

    print(f"📥 Download Speed: {download_speed:.2f} Mbps")
    print(f"📤 Upload Speed: {upload_speed:.2f} Mbps")
    print(f"📶 Latency (Ping): {ping:.2f} ms\n")

    log_message = f"Internet Speed Test Results: Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps, Ping: {ping:.2f} ms"
    log_to_file(log_message)

# Port scan
def scan_ports(ip, start_port, end_port):
    print(f"\n🔍 Scanning ports from {start_port} to {end_port} on {ip}...\n")
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  
            result = sock.connect_ex((ip, port))  
            if result == 0:
                open_ports.append(port)  
            sock.close()  
        except socket.error:
            continue  
    
    log_message = f"Port Scan Results: Scanned IP: {ip}, Open ports: {open_ports}"
    log_to_file(log_message)
    
    return open_ports

# Main System
def system():
    print_welcome_message()  
    while True:
        print(f"\n{CYAN}Network Scanner and Speed Test Tool{RESET}")
        print(f"{CYAN}[1] : Network Monitoring and Device Detection{RESET}")
        print(f"{CYAN}[2] : Internet Speed Test{RESET}")
        print(f"{CYAN}[3] : Port Scan{RESET}")
        print(f"{CYAN}[4] : Exit{RESET}\n")

        selecter = input("Make your selection: ")

        if selecter == "1":
            print("\n🔍 Network Monitoring is starting...")
            target_ip = input(f"{YELLOW}🎯 Enter IP address (e.g., 192.168.1.1): {RESET}").strip()
            get_devices_on_network(target_ip)

        elif selecter == "2":
            run_speed_test()

        elif selecter == "3":
            target_ip = input(f"{YELLOW}🎯 Enter the IP address to scan (e.g., 192.168.1.1): {RESET}").strip()
            start_port = int(input("📍 Enter the starting port: "))
            end_port = int(input("📍 Enter the ending port: "))
            open_ports = scan_ports(target_ip, start_port, end_port)
            
            if open_ports:
                print(f"\n{len(open_ports)} open ports found:")
                for port in open_ports:
                    print(f"{GREEN}✅ Port {port} is open.{RESET}")
            else:
                print(f"{YELLOW}\nNo open ports found.{RESET}")

        elif selecter == "4":
            print(f"{CYAN}Exiting...{RESET}")
            break  

        else:
            print(f"{RED}Invalid selection! Please enter a valid option.{RESET}")

if __name__ == "__main__":
    system()
