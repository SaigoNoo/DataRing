# A l'attention des utilisateurs GitHub
Sachez que ce projet n'est nullement professionnel, mais simplement un travail d'études où je dois jouer le role de développeur avec le client.

# Rédaction du cahier des charges
Par *[Doussis Giorgios](https://github.com/SaigoNoo)*

## Présentation Client
Le clients sont des responsables IT de l'EPHEC (École pratique des hautes études commerciales). Ils sont spécialisés en Administration des systèmes et réseaux.<br>
Ce sont des personnes surchargés par leur travail en ce moment, d'où la raison de cette déléguation de commande.<br>
Il est donc clair que les clients ci-présents sont compétants dans le domaine et sauront donc exploiter l'utilitaire accompagnée d'une solide documentation.

## Description du Projet
Le projet consiste à créer une platefore de monitoring pour pinger (interroger) des noms de domaines comme google.be, ephec.be, etc...<br>
Il est demandé de réaliser l'utilitaire en **Python** est en **ligne de commande (CLI)**, probablement pour pouvoir facilement implémenter des futures fonctions.<br>
La configuration doit être simple et modifiable avec un fichier, à chaud (fichier JSON contenant les domaines)<br>

## Exemple de fichier JSON attendu
```json
{
  "EPHEC": {
    "enable": true,
    "dns": "www.ephec.be",
    "priority": 0,
    "period": 15
  },
  "PLEX - Bad DNS": {
    "enable": true,
    "dns": "plxe.dosis.eb",
    "priority": 1
  },
  "PLEX - Good DNS": {
    "enable": true,
    "dns": "plex.doussis.be",
    "priority": 2
  }
}
```

## Objectif
Avoir un suivi en temps réel de l'état des services, d'un simple coup d'oeil avec une intervale personnalisable en secondes.<br>
L'objectif est de pouvoir permettre aux responsables de l'IT d'interagir<br>
en conséquence lors d'une éventuelle panne système et de pouvoir éventuellement prévenir leurs utilisateurs sur l'indisponibilité d'un de leurs services.<br>

## Besoins fonctionnels

### Visuel

Rendre l'outil un minimum lisible et agréable a lire. Il serait désagréable de consulter plus de 100 domaines si tout est mal structuré et en blanc.<br>
Pouvoir éventuellement stocker les données à chaque interval pour avoir une statistique des disponibilités par intervales d'analyse.

### Des fréquences d'actualisation correctes

Scanner les noms de domaines a une fréquence adaptée de sorte à avoir le temps de lire les informations à l'écran et pouvoir trier les données par:
- fqdn (dns)
- par status (connectés / déconnectés)
- par niveau de priorité (0 => Plus haute priorité à chiffre positif infini)
<br>

> ⚠️ Ce qu'on entend par priorité représente quelle nom de domaine sera scané en priorité, et quelles actions seront définies en fonctionne d'un comportement quelconque, comme une notification etc... ⚠️


### Gestion des noms de domaines cibles | Manuel

La méthode, peut-être la plus barbare, elle consiste à éditer un fichier JSON et d'y insérer un sous-dictionnaire sans passer par le logiciel en lui-même.
Il s'agirait de passer par un éditeur de texte (GUI ou non), et de l'éditer à chaud, le programme, actualise sa liste de noms de domaines a chaque itération de lecture.

### Gestion des noms de domaines cibles | Programme

La méthode la plus simple pour ajouter un DNS cible serait d'employer l'argument ``--àdd`` avec le second script.
Il suffirait d'executer ``setup.py --add`` indépendamment du script ``main.py`` pour y procèder.

__Exemple basique de code pour lire le fichier et y écrire:__
```py
from json import load, dump


def read_json(file):
  with open(file=file, mode='r', enconding='utf8') as dns_list:
    return load(dns_list)

def write(file, name: str, enable: bool, dns: str, priority: int=1):
content = read_json(file=file)[name] = {
    "enable": enable,
    "dns": dns,
    "priority": priority
}
    with open(file=file, mode='w', encoding='utf8') as dns_list:
        file.write(dumps(content, indent=2))

datas_json = read_json(file='dns.json')
write(file='dns.json', name='GOOGLE BE', enable=True, dns='google.be')
```
> ⚠️ Par ce moyen (comme pour l'autre en manuel), la modification pourra être faite à chaud. ⚠️

### Gestion des inputs

Il n'y a aucun input attendu dans le programme, a part les appels avec arguments. Ce logiciel de base, ne se contente que de traiter des instructions, et toutes entrée (signal, clavier, souris) executant du code ASCII ne devra en rien interferer avec le script. Les seules commandes attendues sont les suivantes:
```bash
python3 main.py
```
```bash
python3 setup.py --add --name="GOOGLE BE --dns="google.be" --enable=True --priority=1
```
```bash
python3 setup.py --del --name="GOOGLE BE"
```
```bash
python3 setup.py --edit --name="GOOGLE BE" --enable=False
```

### Rapports, historiques...
Le logiciel devra être capable de mémoriser chaque itération d'analyse, c'est à dire, l'heure du scan et le résultat du domaine scané. 
Un format proposé serait de la structure suivante:
```json
"scans: {
  "GOOGLE BE": {
    "2024": {
      "mars": {
        "13": {
          "12:41": {
            "reachable": true,
            "latence": 15
          }
          "12:46": {
            "reachable": true,
            "latence": 12
          }
        }
      }
    }
  }
}
```
> ⚠️ Eviter de stocker les scans toutes les 1 minutes, mais toutes les 5 minutes, sinon le fichier JSON pourra vite devenir très lourd.  ⚠️

On pourra ainsi, créer des méthodes ou fonctiones capables de traiter rapidement les données a partir d'une date, un mois, et filtrer sur ceux qui étaient disponible ou non...
A partir de ces données, et grace a la structure JSON (dictionnaire), on pourra générer des graphiques sur base des données obtenues.

### Utilitaire administratifs et de prévention des soucis techniques

Ce script incorporera une large gamme de systèmes de notification tels que:
- Notification e-mail (SMTP)
- Notification discord (via bot ou par webhook)
- Notification Telegram
- Optionnel: Notification vers logiciel client (notification OS)

### Description des priorités:
| Numéro de priorité | Description |
|--------------------|-------------|
| 1 | Niveau absolu, si aucune réponse n'est renvoyé au script, envoyer une notification aux administrateurs |
|---|--------------------------------------------------------------------------------------------------------|

## Contraintes Techniques / Légales

Certains services externes peuvent réagir si un nombre de pings sont trop récurents sur un temps donné, et peut donc corrompre les données récoltées.<br>
<br>
Il faut donc configurer les pings en fonctions des règles du service. <br>
<br>
C'est pour cela que l'on propose le paramètre ``period`` dans le fichier json,<br>
afin de définir tout les combiens de temps il faudra lancer un scan pour un domain donnée !<br>
<br>
``🛑 INFO: Si period n'est pas défini dans le JSON, il prendra alors une valeur par défaut définie dans le code principale``<br>

## Méthodologie et Planning
Le projet devra être développé dans un délai inférieur à 30 jours, avec des jalons clés à respecter pour chaque phase de développement.<br>
Les réunions avec le client ne sont pas nécessaires mais un suivi est préferé par le client tout les 6 jours.<br>

## Fonctionnalités Minimum (MVP)
- [x] Le ping doit fonctionner pour au moins un DNS.
- [x] ROUGE si deconnecté, JAUNE si inconnu.
- [x] Trier par défaut par ordre alphabétique

## Budget
~~Le budget sera défini dans un devis séparé en fonction des coûts de développement et de test~~
Le travail étant achevé, ce dernier est estimé à 150 € pour une licence entreprise.

## Timeline
| Semaine       | Informations |
| ------------- | ------------- |
| S1  | Création du cahier des charges|
| S2  | Initialisation + finalisation du MVP#01  |
| S3  | Création du projet final + couleurs |
| S4  | Fin du projet + Test unitaires  |
