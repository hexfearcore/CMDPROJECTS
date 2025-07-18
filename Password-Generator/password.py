#!/usr/bin/env python3
"""
Rainbow Password Generator - Pure terminal password generator
Created by HEXFEARCORE
"""

import random
import string
import hashlib
import time
import os
import sys
from typing import List, Dict, Optional
import secrets

class RainbowColors:
    DEEP_PURPLE = '\033[38;5;129m'
    PURPLE = '\033[38;5;165m'
    PINK = '\033[38;5;207m'
    RED = '\033[38;5;196m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[38;5;226m'
    GREEN = '\033[38;5;46m'
    CYAN = '\033[38;5;51m'
    BLUE = '\033[38;5;27m'
    INDIGO = '\033[38;5;57m'
    VIOLET = '\033[38;5;129m'

    RAINBOW_GRADIENT = [DEEP_PURPLE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, VIOLET]
    FIRE_GRADIENT = ['\033[38;5;196m', '\033[38;5;202m', '\033[38;5;208m', '\033[38;5;214m', '\033[38;5;220m']

    BOLD = '\033[1m'
    RESET = '\033[0m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rainbow_text(text: str, gradient: Optional[List[str]] = None) -> str:
    if gradient is None:
        gradient = RainbowColors.RAINBOW_GRADIENT
    colored_text = ""
    for i, char in enumerate(text):
        color = gradient[i % len(gradient)]
        colored_text += f"{color}{char}"
    return colored_text + RainbowColors.RESET

def print_banner():
    clear_screen()
    print(rainbow_text("\n" + "RAINBOW PASSWORD GENERATOR".center(80)))
    print(rainbow_text("by HEXFEARCORE".center(80), RainbowColors.FIRE_GRADIENT))

def create_border():
    width = 80
    line_char = '─'
    return ''.join(f"{RainbowColors.RAINBOW_GRADIENT[i % len(RainbowColors.RAINBOW_GRADIENT)]}{line_char}" for i in range(width)) + RainbowColors.RESET

def safe_input(prompt: str, default: str = "") -> str:
    try:
        return input(prompt).strip() or default
    except:
        return default

def safe_int_input(prompt: str, default: int = 8, min_val: int = 1, max_val: int = 128) -> int:
    while True:
        try:
            val = int(safe_input(prompt, str(default)))
            if min_val <= val <= max_val:
                return val
        except:
            pass
        print(f"{RainbowColors.RED}Enter a valid number between {min_val} and {max_val}{RainbowColors.RESET}")

def generate_password(length=16, specials=True, digits=True, upper=True, lower=True) -> str:
    chars = ""
    if lower: chars += string.ascii_lowercase
    if upper: chars += string.ascii_uppercase
    if digits: chars += string.digits
    if specials: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    chars = chars or string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def analyze_strength(pw: str) -> Dict:
    score = 0
    details = []
    length = len(pw)
    if length >= 16:
        score += 25
        details.append("✓ Good length")
    elif length >= 12:
        score += 15
        details.append("✓ Okay length")
    else:
        score += 5
        details.append("✗ Too short")

    has_lower = any(c.islower() for c in pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pw)

    variety = sum([has_lower, has_upper, has_digit, has_special])
    score += variety * 15
    details.append(f"✓ Character variety: {variety} types")
    return {'score': min(score, 100), 'details': details}

def display_meter(score: int):
    bar = ""
    for i in range(50):
        color = RainbowColors.RAINBOW_GRADIENT[i % len(RainbowColors.RAINBOW_GRADIENT)]
        bar += f"{color}{'#' if i < score//2 else '.'}"
    print(f"[{bar}{RainbowColors.RESET}] {score}%")

def show_passwords(passwords: List[str]):
    print(create_border())
    for i, pw in enumerate(passwords, 1):
        print(f"\n{RainbowColors.BOLD}Password #{i}:{RainbowColors.RESET}")
        print(rainbow_text(pw.center(60)))
        strength = analyze_strength(pw)
        display_meter(strength['score'])
        for d in strength['details']:
            print(f"  - {d}")
    print(create_border())

def menu():
    while True:
        print(create_border())
        print(rainbow_text("1. Generate Password"))
        print(rainbow_text("2. Generate Multiple Passwords"))
        print(rainbow_text("3. Custom Settings"))
        print(rainbow_text("4. Test Password Strength"))
        print(rainbow_text("5. Exit"))
        print(create_border())

        choice = safe_input("Select an option (1-5): ")

        if choice == '1':
            pw = generate_password()
            show_passwords([pw])
        elif choice == '2':
            count = safe_int_input("How many passwords? (1-10): ", 3, 1, 10)
            pws = [generate_password() for _ in range(count)]
            show_passwords(pws)
        elif choice == '3':
            l = safe_int_input("Length (8-128): ", 16, 8, 128)
            s = safe_input("Include special characters? (y/n): ", 'y') == 'y'
            d = safe_input("Include digits? (y/n): ", 'y') == 'y'
            u = safe_input("Include uppercase? (y/n): ", 'y') == 'y'
            lo = safe_input("Include lowercase? (y/n): ", 'y') == 'y'
            pw = generate_password(l, s, d, u, lo)
            show_passwords([pw])
        elif choice == '4':
            pw = safe_input("Enter password to test: ")
            if pw:
                s = analyze_strength(pw)
                display_meter(s['score'])
                for d in s['details']:
                    print("  -", d)
        elif choice == '5':
            print(rainbow_text("Goodbye!"))
            break
        else:
            print(rainbow_text("Invalid option. Try again.", [RainbowColors.RED]))
        input("\nPress Enter to continue...")
        clear_screen()

def main():
    print_banner()
    time.sleep(1)
    menu()

if __name__ == "__main__":
    main()
