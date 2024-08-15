from json import load
from pythonping import ping
from fastapi import FastAPI
from time import sleep
from asyncio import run, sleep


class Printer:
    async def counter_when_zero(self, configuration: dict, class_instance):
        print(type(class_instance))
        await sleep(int(configuration["period"]))
        return


class DataRingRequest:
    def __init__(self):
        def read_config():
            with open('ressources/dns.json', 'r') as dns:
                return load(dns)

        self.dns = read_config()

    def test_dns(self):
        for dns in self.dns:
            if self.dns[dns]["enable"]:
                return self.dns_response(self.dns[dns]["dns"])

    def dns_response(self, dns_value: str):
        try:
            return [ping(target=dns_value, verbose=False, timeout=2).success(), 1]
        except:
            return [False, 0]


# Déclarations
dataring = DataRingRequest()
app = FastAPI(
    description="API integrée à DataRing"
)


# Déclarations des request
@app.get("/add")
async def add(tag: str, enable: int, dns: str, priority: int, period: int):
    return "Ajouté"


@app.get("/delete")
async def delete(tag: str):
    return "Supprimé"


@app.get("/update")
async def update(tag: str, enable: int, dns: str, priority: int, period: int):
    return "Mis à jour"


while True:
    print(dataring.test_dns())
