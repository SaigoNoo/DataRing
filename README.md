# Rédaction du cahier des charges
Par *[Doussis Giorgios](https://github.com/SaigoNoo)*

## Présentation Client
Ce sont les responsables IT de l'EPHEC. Ils sont spécialisés en Administration des systèmes et réseaux.
Ce sont des personnes surchargés par leur travail en ce moment, d'où la raison de cette déléguation de commande.

## Description du Projet
Il s'agit de créer une platefore de monitoring pour pinger des noms de domaines comme google.be, ephec.be, ...
Il est demandé de réaliser l'utilitaire en **Python** est en **ligne de commande (CLI)**.
La configuration doit être simple et modifiable a chaud (fichier JSON contenant les domaines)

## Objectif
Avoir un suivi en temps réel de l'état des services, d'un simple coup d'oeil. L'objectif est de pouvoir permettre aux responsables de l'IT d'interagir
en conséquence lors d'une éventuelle panne système et de pouvoir éventuellement prévenir leurs utilisateurs sur l'indisponibilité de services.

## Besoins fonctionnels

### Visuel

Rendre l'outil un minimum lisible et agréable a lire. Il serait désagréable de consulter plus de 100 domaines si tout est mal structuré et en blanc.

### Des fréquences d'actualisation correctes

Scanner les noms de domaines a une fréquence de sorte à ne pas surcharger l'écran et a filtrer les fqdn (dns) par status (connectés / déconnectés)

## Contraintes Techniques / Légales

Certains services peuvent mal réagir si un nombre de pings sont trop récurents sur un temps donné.
Il faut donc configurer les pings en fonctions des règles du service. 

## Méthodologie et Planning
Le projet devra être développé dans un délai inférieur à 30 jours, avec des jalons clés à respecter pour chaque phase de développement.
Les réunions avec le client ne sont pas nécessaires mais un suivi est préferé par le client tout les 6 jours.

## Fonctionnalités Minimum (MVP)
- [ ] Le ping doit fonctionner pour au moins un DNS.
- [ ] ROUGE si deconnecté, JAUNE si inconnu. 

## Budget
Le budget sera défini dans un devis séparé en fonction des coûts de développement et de test

## Timeline
| Semaine       | Informations |
| ------------- | ------------- |
| S1  | Création du cahier des charges|
| S2  | Initialisation + finalisation du MVP#01  |
| S3  | Création du projet final + couleurs |
| S4  | Fin du projet + Test unitaires  |
