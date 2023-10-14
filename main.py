from json import load
from pythonping import ping

dns_queries = None


def load_dns(querie):
    for dns in querie:
        if querie[dns]['enable']:
            output(dns, querie[dns]['dns'], dns_response(querie[dns]['dns']))


def dns_response(dns_value):
    try:
        return [ping(target=dns_value, verbose=False, timeout=2).success(), 1]
    except:
        return [False, 0]


def output(label, dns, success):
    if success[1] == 0:
        response = 'UNKNOWN DNS'
    elif success[1] == 1:
        response = 'NO ANSWER'
    print(f'{label}:\n - DNS: {dns}\n - Response: {"OK" if success[0] else f"UNREACHABLE ({response})"}\n')


with open('ressources/dns.json', 'r') as dns:
    dns_queries = load(dns)

load_dns(dns_queries)
