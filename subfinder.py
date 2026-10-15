import json
import re
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


def normalize_domain(value):
    value = value.strip()
    parsed = urlsplit(value if "://" in value else "//" + value)
    if parsed.username or parsed.password or not parsed.hostname:
        raise ValueError("Inserisci un dominio, ad esempio example.com.")
    domain = parsed.hostname.rstrip(".").encode("idna").decode("ascii").lower()
    labels = domain.split(".")
    if (
        len(domain) > 253
        or len(labels) < 2
        or all(label.isdigit() for label in labels)
        or any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels)
    ):
        raise ValueError("Dominio non valido. Esempio: example.com")
    return domain


def find_subdomains(domain):
    query = urlencode({"q": f"%.{domain}", "output": "json"})
    request = Request(
        "https://crt.sh/?" + query,
        headers={"User-Agent": "SubdomainFinder/1.0", "Accept": "application/json"},
    )
    with urlopen(request, timeout=60) as response:
        certificates = json.load(response)
    if not isinstance(certificates, list):
        raise ValueError("Risposta inattesa da crt.sh. Riprova piu' tardi.")

    results = set()
    for certificate in certificates:
        if not isinstance(certificate, dict):
            continue
        names = certificate.get("name_value", "")
        if not isinstance(names, str):
            continue
        for name in names.splitlines():
            if "*" in name:
                continue
            try:
                hostname = normalize_domain(name)
            except ValueError:
                continue
            if hostname.endswith("." + domain):
                results.add(hostname)
    return sorted(results)


def main():
    print(r"""
    __  __ ____  _   _
   |  \/  | __ )| | | |
   | |\/| |  _ \| |_| |
   | |  | | |_) |  _  |
   |_|  |_|____/|_| |_|

  ____  _   _ ____  _____ ___ _   _ ____  _____ ____
 / ___|| | | | __ )|  ___|_ _| \ | |  _ \| ____|  _ \
 \___ \| | | |  _ \| |_   | ||  \| | | | |  _| | |_) |
  ___) | |_| | |_) |  _|  | || |\  | |_| | |___|  _ <
 |____/ \___/|____/|_|   |___|_| \_|____/|_____|_| \_\

                Subdomain Finder
    """)
    print("Ricerca nei certificati pubblici tramite crt.sh.")
    print("I risultati possono essere storici e non necessariamente attivi.\n")

    while True:
        value = input("Inserisci il dominio (es. example.com), oppure Invio per uscire: ")
        if not value.strip():
            return
        try:
            domain = normalize_domain(value)
            break
        except ValueError as error:
            print(f"{error}\n")

    print(f"\nRicerca di sottodomini per {domain}... Attendi.\n")
    try:
        results = find_subdomains(domain)
    except (URLError, OSError, ValueError) as error:
        print(f"Ricerca fallita: {error}")
        print("Verifica la connessione o riprova piu' tardi.")
        return

    for hostname in results:
        print(hostname)
    print(f"\nTrovati {len(results)} sottodomini.")
    if results:
        output = Path(__file__).resolve().parent / f"{domain}_subdomains.txt"
        try:
            output.write_text("\n".join(results) + "\n", encoding="utf-8")
            print(f"Risultati salvati in: {output}")
        except OSError as error:
            print(f"Impossibile salvare il file: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nRicerca annullata.")
    finally:
        try:
            input("\nPremi Invio per chiudere...")
        except (KeyboardInterrupt, EOFError):
            pass
