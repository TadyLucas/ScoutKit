import dns.resolver
import concurrent.futures
from urllib.parse import urlparse

def load_wordlist(path):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def resolve_subdomain(subdomain):
    try:
        dns.resolver.resolve(subdomain, "A")
        return subdomain
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
        return None
def extract_domain(url):
    parsed = urlparse(url)
    return parsed.hostname

def enumerate(url, threads=30):
    domain = extract_domain(url)
    print(f"[+]ScoutKit Bruteforcing subdomains for {domain}")
    words = load_wordlist("modules/wordlists/subdomains-top1million-5000.txt")
    targets = [f"{word}.{domain}" for word in words]
    found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(resolve_subdomain, targets)

    for sub in results:
        if sub:
            print(f"[FOUND] {sub}")
            found.append(sub)

    return found
