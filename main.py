from json import load, dumps
from pythonping import ping
from fastapi import FastAPI
from asyncio import create_task, sleep
from rich.console import Console
from rich.panel import Panel
from uvicorn import run as runuvi
from requests import get


class CLI:
    async def counter_when_zero(self, label: str, dns: dict):
        await sleep(int(dns["period"]))
        return DataRingRequest().test_dns(label=label, dns=dns)


class DataRingRequest:
    def __init__(self):
        self.dns = None
        self.update_config()

    def update_config(self):
        with open('ressources/dns.json', 'r') as dns:
            self.dns = load(dns)

    def test_dns(self, label: str, dns: dict):
        if dns["enable"]:
            return self.dns_response(label=label, dns=dns["dns"])

    def dns_response(self, label: str, dns: str):
        try:
            response = ping(target=dns, verbose=False, timeout=2)
            if not response.success():
                return [label, dns, response.success(), "DNS_EXIST_BUT_NO_MS"]
            else:
                return [label, dns, response.success(), response.rtt_avg_ms]
        except:
            return [label, dns, False]


class Config:
    def __init__(self):
        with open(file="ressources/dns.json", mode="r", encoding="utf-8") as dns:
            self.dns = load(dns)

    def tag_exist(self, label: str):
        return label in self.dns

    def add_entry(self, label: str, enable: int, dns: str, priority: int, period: int):
        self.dns[label] = {
            "enable": int(enable) == 1,
            "dns": dns,
            "priority": int(priority),
            "period": int(period)
        }

    def delete_entry(self, label: str):
        del self.dns[label]

    def save_config(self):
        with open(file="ressources/dns.json", mode="w") as dns:
            dns.write(dumps(obj=self.dns, indent=2))


class Notification:
    def __init__(self):
        self.discord = "https://discord.com/api/webhooks/1150119172097986691/6iSgNysP6bFfjiS7QjE9UuthUjlqthg0XLFZ0YqHPf7t2kApjbCJZ0sr64tsIuDo9KhU"

    def check_discord_exist(self):
        r = get(url=self.discord).json()
        return "application_id" in r and "avatar" in r and "channel_id" in r and "guild_id" in r

    def send_discord_notif(self, data: dict):
        pass


# Declarations
dataring = DataRingRequest()
app = FastAPI(
    description="API integrée à DataRing"
)
cli = CLI()


# Déclarations des requêtes
@app.get("/add")
async def add(tag: str, enable: int, dns: str, priority: int, period: int):
    if 0 < priority < 5:
        c = Config()
        c.add_entry(label=tag, enable=enable, dns=dns, priority=priority, period=period)
        c.save_config()
        return 'Added'
    else:
        return "Priority should be between 1 and 4"


@app.get("/delete")
async def delete(tag: str):
    c = Config()
    if c.tag_exist(label=tag):
        c.delete_entry(label=tag)
        c.save_config()
        return "Deleted"
    else:
        return f"Label {tag} doesn't exist!"


@app.get("/update")
async def update(tag: str, enable: int, dns: str, priority: int, period: int):
    if 0 < priority < 5:
        c = Config()
        if c.tag_exist(label=tag):
            c.add_entry(label=tag, enable=enable, dns=dns, priority=priority, period=period)
            c.save_config()
            return 'Updated'
        else:
            return f"Label {tag} doesn't exist!"
    else:
        return "Priority should be between 1 and 4"


async def check_dns():
    def format_preview(result: list):
        label = result[0]
        dns = result[1]
        dns_exist = result[2]
        reachable = result[2]
        for element in result:
            if str(element).startswith("DNS_EXIST_BUT"):
                dns_exist = True
        ms = result[3] if result[2] else None
        priority = Config().dns[label]["priority"]
        period = Config().dns[label]["period"]
        notified = "Notification sended" if priority == 1 or priority == 4 and not reachable else "Nothhing to do..."
        Console(
            record=True
        ).print(
            Panel.fit(
                f"- DNS: {dns}\n- DNS EXIST: {dns_exist}\n- DNS REACHABLE: {reachable}\n- MS: {ms}\n- Priority: {priority}\n- Period: {period}\n\n{notified}",
                title=label,
                width=60
            )
        )

    while True:
        tasks = []
        for dns in dataring.dns:
            task = create_task(cli.counter_when_zero(label=dns, dns=dataring.dns[dns]))
            task.add_done_callback(lambda t: format_preview(result=t.result()))
            tasks.append(task)

        await sleep(0)
        await sleep(max(int(d["period"]) for d in dataring.dns.values()))

        dataring.update_config()


# Lancement de la tâche de fond au démarrage de l'application
@app.on_event("startup")
async def startup_event():
    create_task(check_dns())


# Démarrer l'application avec uvicorn
if __name__ == "__main__":
    # Tester les services Notif
    n = Notification()
    if not n.check_discord_exist():
        raise ConnectionError("Discord Webhook isn't correctly configured !")
    runuvi(app, host="127.0.0.1", port=8000)
