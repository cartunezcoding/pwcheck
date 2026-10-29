"""pwcheck - a tiny password strength checker.

Run it:  python pwcheck.py
Your password is typed hidden and never saved or sent anywhere.
"""

import argparse
import getpass
import math
import string

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball",
    "abc123", "football", "monkey", "letmein", "shadow", "master",
    "666666", "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "superman", "1qaz2wsx", "password1",
    "azerty", "iloveyou", "admin", "welcome", "login", "roblox",
}

KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "azertyuiop", "qsdfghjklm", "1234567890"]

LEVELS = [
    (20, "Very weak"),
    (40, "Weak"),
    (60, "Okay"),
    (80, "Strong"),
    (101, "Very strong"),
]


def pool_size(password):
    """How many different characters could each position be? (bigger = better)"""
    size = 0
    if any(c in string.ascii_lowercase for c in password):
        size += 26
    if any(c in string.ascii_uppercase for c in password):
        size += 26
    if any(c in string.digits for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += 32
    if any(c not in string.printable for c in password):
        size += 64
    return size


def entropy_bits(password):
    """Rough entropy estimate in bits."""
    size = pool_size(password)
    if size == 0:
        return 0.0
    return len(password) * math.log2(size)


def has_sequence(password, length=4):
    """Detects things like 'abcd', '4321' or 'qwer'."""
    lowered = password.lower()
    sources = [string.ascii_lowercase, string.digits] + KEYBOARD_ROWS
    for source in sources:
        for text in (source, source[::-1]):
            for i in range(len(text) - length + 1):
                if text[i:i + length] in lowered:
                    return True
    return False


def has_repeats(password, length=3):
    """Detects things like 'aaa' or '1111'."""
    return any(
        len(set(password[i:i + length])) == 1
        for i in range(len(password) - length + 1)
    )


def check(password):
    """Return (score 0-100, label, list of tips)."""
    tips = []

    if not password:
        return 0, LEVELS[0][1], ["Type something first!"]

    if password.lower() in COMMON_PASSWORDS:
        return 0, LEVELS[0][1], ["This is one of the most used passwords ever. Change it."]

    bits = entropy_bits(password)
    score = min(100, int(bits / 80 * 100))

    if len(password) < 12:
        tips.append("Use at least 12 characters.")
    if not any(c in string.ascii_uppercase for c in password):
        tips.append("Add an UPPERCASE letter.")
    if not any(c in string.ascii_lowercase for c in password):
        tips.append("Add a lowercase letter.")
    if not any(c in string.digits for c in password):
        tips.append("Add a number.")
    if not any(c in string.punctuation for c in password):
        tips.append("Add a symbol like ! or #.")

    if has_sequence(password):
        score -= 20
        tips.append("Avoid sequences like 'abcd', '1234' or 'qwer'.")
    if has_repeats(password):
        score -= 15
        tips.append("Avoid repeating the same character (like 'aaa').")
    if len(set(password)) <= len(password) // 2:
        score -= 10
        tips.append("Use more different characters.")

    score = max(0, min(100, score))
    label = next(name for limit, name in LEVELS if score < limit)
    return score, label, tips


def bar(score, width=30):
    filled = round(score / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def show(password):
    score, label, tips = check(password)
    print()
    print(f"  Strength : {bar(score)} {score}/100")
    print(f"  Verdict  : {label}")
    print(f"  Entropy  : ~{entropy_bits(password):.0f} bits")
    if tips:
        print("  Tips:")
        for tip in tips:
            print(f"    - {tip}")
    else:
        print("  Nothing to improve. Nice one!")
    print()


def main():
    parser = argparse.ArgumentParser(description="Check how strong a password is.")
    parser.add_argument(
        "password",
        nargs="?",
        help="password to test (leave empty to type it hidden - safer)",
    )
    args = parser.parse_args()

    password = args.password
    if password is None:
        password = getpass.getpass("Password to test (hidden): ")
    show(password)


if __name__ == "__main__":
    main()
