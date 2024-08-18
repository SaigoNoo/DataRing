from json import load, dumps
from pythonping import ping
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from asyncio import create_task, sleep, gather
from rich.console import Console
from rich.panel import Panel
from uvicorn import run as runuvi
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime


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
        self.update_config()
        if dns["enable"]:
            try:
                response = ping(target=dns["dns"], verbose=False, timeout=2)
                return {
                    "label": label,
                    "dns": dns["dns"],
                    "dns_exist": response.success() and response.stats_packets_sent == 4,
                    "dns_reachable": response.success(),
                    "ms": response.rtt_avg_ms,
                    "priority": dns["priority"],
                    "period": dns["period"]
                }
            except:
                return {
                    "label": label,
                    "dns": dns["dns"],
                    "dns_reachable": False,
                    "priority": dns["priority"],
                    "period": dns["period"]
                }


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

    def send_discord_notif(self, label: str, data: dict):
        webhook = DiscordWebhook(url=self.discord, username="DataRing | Notifier")
        embed = DiscordEmbed(
            title=f"Alerte de connexion pour {label}",
            color=16711680,
            description="Une erreur de connexion à été reportée"
        )
        embed.set_author(name="DataRing")
        embed.set_footer(text="Ceci est un message géneré par DataRing")
        embed.add_embed_field(name="DBS or IP", value=data["dns"])
        if "dns_reachable" in data:
            embed.add_embed_field(name="DNS Reachable", value=data["dns_reachable"])
        if "dns_exist" in data:
            embed.add_embed_field(name="DNS Exist", value=data["dns_exist"])
        if "ms" in data:
            embed.add_embed_field(name="Timeout", value=str(data["ms"]))
        embed.add_embed_field(name="Priority", value=str(data["priority"]))
        embed.add_embed_field(name="Period", value=str(data["period"]))
        webhook.add_embed(embed=embed)
        send = webhook.execute()
        return send.status_code


class Errors:
    def __init__(self):
        self.errors = []

    def add(self, label: str):
        self.errors.append(label)

    def rem(self, label: str):
        index = self.errors.index(label)
        del self.errors[index]


class Logs:
    def __init__(self):
        self.file = "ressources/log.json"

    def add(self, label: str, result: dict):
        def key_exist_in(key: str, dict: dict):
            return key in dict

        with open(file="ressources/log.json", mode="r", encoding="utf-8") as log:
            data = load(log)
        now = datetime.now()
        year = str(now.strftime("%Y"))
        month = str(now.strftime("%m"))
        day = str(now.strftime("%d"))
        hour = str(now.strftime("%H"))
        minute = str(now.strftime("%M"))
        seconds = str(now.strftime("%S"))
        if not key_exist_in(key=year, dict=data):
            data[year] = {}
        if not key_exist_in(key=month, dict=data[year]):
            data[year][month] = {}
        if not key_exist_in(key=day, dict=data[year][month]):
            data[year][month][day] = {}
        if not key_exist_in(key=hour, dict=data[year][month][day]):
            data[year][month][day][hour] = {}
        if not key_exist_in(key=minute, dict=data[year][month][day][hour]):
            data[year][month][day][hour][minute] = {}
        if not key_exist_in(key=seconds, dict=data[year][month][day][hour][minute]):
            data[year][month][day][hour][minute][seconds] = {}
        data[year][month][day][hour][minute][seconds] = {
            "label": label,
            "dns": result["dns"],
            "priority": result["priority"],
            "period": result["period"]
        }
        if "dns_reachable" in result:
            data[year][month][day][hour][minute][seconds]["dns_exist"] = result["dns_exist"]
            data[year][month][day][hour][minute][seconds]["dns_reachable"] = result["dns_reachable"]
            data[year][month][day][hour][minute][seconds]["ms"] = result["ms"]
        with open(file="ressources/log.json", mode="w", encoding="utf-8") as log:
            log.write(dumps(data, indent=2))


# Declarations
dataring = DataRingRequest()
app = FastAPI(
    description="API integrée à DataRing"
)
cli = CLI()


# Déclarations des requêtes
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


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
        return 'Deleted'
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
    def format_preview(result: dict):
        # Si Priorité 1 et que DNS ne réponds pas et n'est pas indexé comme ERREUR -> Ajouter + Envoyer
        if result["priority"] == 1 and not result["dns_reachable"] and not result["label"] in e.errors:
            e.add(label=result["label"])
            n.send_discord_notif(label=result["label"], data=result)
            notified = "Notification sent !"

        elif result["priority"] == 4 and not result["label"] in e.errors:
            e.add(label=result["label"])
            n.send_discord_notif(label=result["label"], data=result)
            notified = "Notification sent !"

        # Si DNS répond et indexé comme erreur, le supprimer des erreurs et qu'il n'a pas la priorité 4
        elif result["dns_reachable"] and result["label"] in e.errors and result["priority"] != 4:
            e.rem(label=result["label"])
            notified = "Resolved !"

        # Si DNS ne répond pas et est toujours indexé comme ERREUR - > Juste message
        elif not result["dns_reachable"] and result["label"] in e.errors:
            notified = "Already not resolved"

        elif result["dns_reachable"] and result["priority"] == 2:
            l.add(label=result["label"], result=result)
            notified = "Error logged !"

        else:
            notified = "Nothing more to do..."

        text = ""
        text += f"- DNS: {result['dns']}\n"
        if "dns_exist" in result:
            text += f"- DNS EXIST: {result['dns_exist']}\n"
        text += f"- DNS REACHABLE: {result['dns_reachable']}\n"
        if "ms" in result:
            text += f"- MS: {result['ms']}\n"
        text += f"- Priority: {result['priority']}\n"
        text += f"- Period: {result['period']}\n\n"
        text += f"{notified}"
        Console(record=True).print(
            Panel.fit(
                renderable=text,
                title=result["label"],
                width=60
            )
        )

    while True:
        tasks = []
        for dns in dataring.dns:
            print(cli.counter_when_zero(label=dns, dns=dataring.dns[dns]))
            task = create_task(cli.counter_when_zero(label=dns, dns=dataring.dns[dns]))
            task.add_done_callback(lambda t: format_preview(result=t.result()))
            tasks.append(task)

        results = await gather(*tasks)

        for result in results:
            format_preview(result)

        dataring.update_config()


@app.on_event("startup")
async def startup_event():
    create_task(check_dns())


# Démarrer l'application avec uvicorn
if __name__ == "__main__":
    # Tester les services Notif
    n = Notification()
    e = Errors()
    l = Logs()
    runuvi(app, host="127.0.0.1", port=8000)
