# pwcheck 🔐

A tiny command-line tool that tells you how strong a password is.
No dependencies. Nothing is saved or sent anywhere.

## Features

- Strength score from 0 to 100 with a progress bar
- Entropy estimate (in bits)
- Detects common passwords, sequences (`abcd`, `1234`, `qwer`) and repeats (`aaa`)
- Gives clear tips to improve the password
- Hidden input, so nobody can read it over your shoulder

## Requirements

- Python 3.8 or newer

## Usage

```bash
python pwcheck.py
```

Type your password (it stays hidden), press Enter, and read the result.

Example output:

```
  Strength : [##############################] 100/100
  Verdict  : Very strong
  Entropy  : ~105 bits
  Nothing to improve. Nice one!
```

## Run the tests

```bash
python -m unittest
```

## How it works

1. Count which kinds of characters are used (lowercase, uppercase, digits, symbols).
2. Estimate entropy: `length x log2(pool size)`.
3. Remove points for weak patterns (sequences, repeats, few unique characters).
4. Give an instant `0` to well-known passwords.

## Roadmap

- [ ] Check against a bigger common-password list
- [ ] Generate a strong random password
- [ ] Colored output

## License

MIT
