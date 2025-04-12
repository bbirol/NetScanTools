import os
import socket
import time
import speedtest

# Renk Tanımları
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"

# Giriş ekranı
def print_welcome_message():
    print(RED) 
    print(" _   _      _   ____                  ")
    print("| \\ | | ___| |_/ ___|  ___ __ _ _ __  ") 
    print("|  \\| |/ _ \\ __\\___ \\ / __/ _` | '_ \\ ")  
    print("| |\\  |  __/ |_ ___) | (_| (_| | | | |")  
    print("|_| \\_|\\___|\\__|____/ \\___\\__,_|_| |_|")  
    print(RESET)  

# Log dosyasına yaz
def log_to_file(message):
    with open("logs.txt", "a") as log_file:
        log_file.write(message + "\n")

# Hostname alma
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
    return f"{YELLOW}Hostname bulunamadı{RESET}"

# MAC adresi alma
def get_mac(ip):
    try:
        output = os.popen("arp -a " + ip).read()
        for line in output.split('\n'):
            if ip in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
        return f"{YELLOW}MAC adresi bulunamadı{RESET}"
    except:
        return f"{RED}MAC sorgusu desteklenemiyor{RESET}"

# Ağ cihazlarını tarama
def get_devices_on_network(target_ip):
    ip_parts = target_ip.split('.')
    base_ip = '.'.join(ip_parts[:3]) + '.'
    devices = []

    print(f"\n🔍 {CYAN}{base_ip}1 - {base_ip}254{RESET} aralığında ağ taraması başlatılıyor...\n")
    start_time = time.time()

    for i in range(1, 255):
        ip = base_ip + str(i)
        response = os.system(f"ping -n 1 -w 1 {ip} > nul")  # Windows için
        if response == 0:
            hostname = get_hostname(ip)
            mac = get_mac(ip)
            devices.append((ip, hostname, mac))
            print(f"{GREEN}✅ {ip:15} | {hostname:25} | {mac}{RESET}")
    
    duration = time.time() - start_time
    print(f"\n{GREEN}✅ Tarama tamamlandı. Toplam bulunan cihaz: {len(devices)}{RESET}")
    print(f"{CYAN}⏱️ Tarama süresi: {round(duration, 2)} saniye{RESET}\n")
    
    log_message = f"Ağ Tarama Sonuçları: {len(devices)} cihaz bulundu, Tarama süresi: {round(duration, 2)} saniye"
    log_to_file(log_message)

    return devices

# Hız testi
def run_speed_test():
    print("\n🌐 İnternet hız testi başlatılıyor...\n")
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping

    print(f"📥 İndirme Hızı: {download_speed:.2f} Mbps")
    print(f"📤 Yükleme Hızı: {upload_speed:.2f} Mbps")
    print(f"📶 Gecikme (Ping): {ping:.2f} ms\n")

    log_message = f"İnternet Hız Testi Sonuçları: İndirme Hızı: {download_speed:.2f} Mbps, Yükleme Hızı: {upload_speed:.2f} Mbps, Ping: {ping:.2f} ms"
    log_to_file(log_message)

# Port tarama
def scan_ports(ip, start_port, end_port):
    print(f"\n🔍 {ip} üzerinde {start_port} ile {end_port} arasındaki portlar taranıyor...\n")
    
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
    
    log_message = f"Port Tarama Sonuçları: Tarama yapılan IP: {ip}, Açık portlar: {open_ports}"
    log_to_file(log_message)
    
    return open_ports

# Ana sistem
def system():
    print_welcome_message()  
    while True:
        print(f"\n{CYAN}Ağ Tarayıcı ve Hız Testi Tool{RESET}")
        print(f"{CYAN}[1] : Ağ İzleme ve Cihaz Tespiti{RESET}")
        print(f"{CYAN}[2] : İnternet Hız Testi{RESET}")
        print(f"{CYAN}[3] : Port Tarama{RESET}")
        print(f"{CYAN}[4] : Çıkış{RESET}\n")

        selecter = input("Seçiminizi yapın: ")

        if selecter == "1":
            print("\n🔍 Ağ İzleme başlatılıyor...")
            target_ip = input(f"{YELLOW}🎯 IP adresi girin (örn: 192.168.1.1): {RESET}").strip()
            get_devices_on_network(target_ip)

        elif selecter == "2":
            run_speed_test()

        elif selecter == "3":
            target_ip = input(f"{YELLOW}🎯 Tarama yapılacak IP adresini girin (örn: 192.168.1.1): {RESET}").strip()
            start_port = int(input("📍 Başlangıç portunu girin: "))
            end_port = int(input("📍 Bitiş portunu girin: "))
            open_ports = scan_ports(target_ip, start_port, end_port)
            
            if open_ports:
                print(f"\n{len(open_ports)} açık port bulundu:")
                for port in open_ports:
                    print(f"{GREEN}✅ Port {port} açık.{RESET}")
            else:
                print(f"{YELLOW}\nAçık port bulunamadı.{RESET}")

        elif selecter == "4":
            print(f"{CYAN}Çıkış yapılıyor...{RESET}")
            break  

        else:
            print(f"{RED}Geçersiz seçim! Lütfen geçerli bir seçenek girin.{RESET}")

if __name__ == "__main__":
    system()
