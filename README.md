# 🔎 MBH SUBFINDER

A simple, interactive subdomain discovery tool written entirely in Python.

MBH SUBFINDER searches public Certificate Transparency records through [crt.sh](https://crt.sh/) to discover subdomains associated with a domain.

##  Features

- ASCII banner and interactive terminal interface
- Passive subdomain discovery
- Automatic duplicate removal and alphabetical sorting
- Results saved to a `.txt` file
- No external Python dependencies

##  Getting Started

**Requirements:** Python 3 and an internet connection.

Download `subfinder.py` and run:

```bash
python subfinder.py
```

On Windows, you can also use:

```powershell
py -3 subfinder.py
```

Enter a domain when prompted:

```text
example.com
```

Results are displayed in the terminal and saved alongside the script:

```text
example.com_subdomains.txt
```

##  How It Works

1. Takes a domain as input.
2. Queries crt.sh for matching certificate records.
3. Extracts subdomains and removes duplicates and wildcard entries.
4. Displays and saves the results.

Certificate records may include historical names. Results are not checked for availability, and discovery is not exhaustive.

##  Roadmap

This is the first version of MBH SUBFINDER. The project will grow with more features and tools for penetration testing.

##  Project Status

**Version:** 1.0  
**Language:** Python  
**Data source:** [crt.sh](https://crt.sh/)
