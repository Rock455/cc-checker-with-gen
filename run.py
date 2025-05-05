from bin_checker import bin_checker, check_cards, parse_card
import os
import re
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    title = "Auto Generate + Checker CC Extrap"
    author = "Not Thushar"
    language = "Python"
    width = 52  
    border = f"{Fore.CYAN}{Style.BRIGHT}{'═' * width}{Style.RESET_ALL}"
    empty_line = f"{Fore.CYAN}║{' ' * (width - 2)}║{Style.RESET_ALL}"

    def center_text(text, width, color=Fore.WHITE):
        text_length = len(text.replace(Style.BRIGHT, '').replace(color, '')) 
        padding = (width - 2 - text_length) // 2
        extra_space = ' ' if (width - 2 - text_length) % 2 != 0 else ''
        return f"{Fore.CYAN}║{' ' * padding}{color}{Style.BRIGHT}{text}{' ' * padding}{extra_space}{Fore.CYAN}║{Style.RESET_ALL}"

    print(f"\n{border}")
    print(empty_line)
    print(center_text(title, width, Fore.GREEN))
    print(empty_line)
    print(center_text(f"Created By: {author}", width, Fore.YELLOW))
    print(center_text(f"Language: {language}", width, Fore.YELLOW))
    print(empty_line)
    print(f"{border}\n")
    

    print("\n[1] Generate and Check Cards from BIN")
    print("[2] Check Specific Cards")
    mode = input("Select mode (1 or 2): ").strip()
    while mode not in ["1", "2"]:
        print("Invalid choice! Enter 1 or 2.")
        mode = input("Select mode (1 or 2): ").strip()
    
    if mode == "1":
        print("\n[1] Enter Single BIN")
        print("[2] Load BINs from File")
        bin_option = input("Select BIN input method (1 or 2): ").strip()
        while bin_option not in ["1", "2"]:
            print("Invalid choice! Enter 1 or 2.")
            bin_option = input("Select BIN input method (1 or 2): ").strip()
        
        if bin_option == "1":
            bins = [get_single_bin()]
        else:
            bins = get_bins_from_file()
        
        amount = input("[+] Amount per BIN: ").strip()
        while not amount.isdigit() or int(amount) <= 0:
            print("Invalid amount! Enter a positive number.")
            amount = input("[+] Amount per BIN: ").strip()
        
        for bin_input in bins:
            print(f"\nProcessing BIN: {bin_input}")
            bin_checker(bin_input, card_count=int(amount))
    
    else:
        print("\n[1] Enter Single Card")
        print("[2] Load Cards from File")
        card_option = input("Select card input method (1 or 2): ").strip()
        while card_option not in ["1", "2"]:
            print("Invalid choice! Enter 1 or 2.")
            card_option = input("Select card input method (1 or 2): ").strip()
        
        if card_option == "1":
            cards = [get_single_card()]
        else:
            cards = get_cards_from_file()
        
        check_cards(cards)

def get_single_bin():
    bin_input = input("[+] BIN: ").strip()
    bin_cleaned = re.sub(r'[a-zA-Z]', '', bin_input)
    if not bin_cleaned or not all(c.isdigit() or c in '|x' for c in bin_cleaned):
        print("Invalid BIN! Enter digits, 'x', or '|' only.")
        return get_single_bin()
    return bin_input

def get_bins_from_file():
    filename = input("[+] BIN file path: ").strip()
    while not os.path.isfile(filename):
        print("File not found! Enter a valid file path.")
        filename = input("[+] BIN file path: ").strip()
    
    bins = []
    with open(filename, "r") as f:
        for line in f:
            bin_input = line.strip()
            if bin_input:
                bin_cleaned = re.sub(r'[a-zA-Z]', '', bin_input)
                if bin_cleaned and all(c.isdigit() or c in '|x' for c in bin_cleaned):
                    bins.append(bin_input)
                else:
                    print(f"Skipping invalid BIN: {bin_input}")
    if not bins:
        print("No valid BINs found in file. Exiting.")
        exit(1)
    return bins

def get_single_card():
    card_input = input("[+] Card: ").strip()
    card = parse_card(card_input)
    if not card:
        print("Invalid card! Format: CC|MM|YYYY|CVV (16-digit CC, 1-12 MM, 2025-2030 YYYY, 3-digit CVV).")
        return get_single_card()
    return card

def get_cards_from_file():
    filename = input("[+] Card file path: ").strip()
    while not os.path.isfile(filename):
        print("File not found! Enter a valid file path.")
        filename = input("[+] Card file path: ").strip()
    
    cards = []
    with open(filename, "r") as f:
        for line in f:
            card_input = line.strip()
            if card_input:
                card = parse_card(card_input)
                if card:
                    cards.append(card)
                else:
                    print(f"Skipping invalid card: {card_input}")
    if not cards:
        print("No valid cards found in file. Exiting.")
        exit(1)
    return cards

if __name__ == "__main__":
    main()