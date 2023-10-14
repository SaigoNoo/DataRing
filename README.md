# Cahier des charges pour la création de DataRing
## Présentation du client :
Le client du projet est *Madame X*, développeur principalement dans le domaine du web (cloud, backend, fronted, ...).
Le client semble très a l'aise avec le domaine de développement étant donnée sa longue experience dans le domaine (plus de **10 ans**).
Sa faculté d'élocution, et les termes technique laisse penser que ce client sait de quoi l'on parle et sait exactement ce dont elle aura besoin. 

## Présentation du projet :
Le projet consiste à réaliser un logiciel de monitoring qui permettra de suivre le fonctionnement des plusieurs services (web, bases de données, etc...) depuis un, et un seul endroit.
A l'aide de méthodes, qui seront décrites au point **Demandes fonctionnelles**, on pourra choisir quelle méthode sera appliqué pour tester la disponibilité d'un service. Plusieurs noms
de projets sont pensés, mais DataRing (**Data** ~~*Monito*~~**ring**).

## Objectif du client :
Comme expliqué ci-dessus, le client souhaite monitorer differents services comme un serveur web, une base de donnée, ou tout services répondant via une requete internet.
Bien qu'il s'agisse d'une fonctionnalités, le client demande à ce que ce projet soit réalisé en Python car il s'agit d'un des seuls environnements dont
sa machine dispose et probablement pour mettre a jour le logiciel par elle-même si une nouvelle technologie venait a devoir
être implémantée dans l'utilitaire.

## Cible / Utilisateur :
La destination finale de ce projet est le client lui-même (client à particulier), et donc ce n'est pas **directement à destination d'une entreprise**.
*Madame X* semble possèder les ressources nécessaires au déploiement de cet utilitaire.

## Demandes fonctionnelles :
- [ ] Logiciel crée en Python
- [ ] Utilisation en CLI (commande line interface)
- [ ] Éventuellement implémenter un système de notification en cas de panne
- [ ] Un descriptif de panne

## Contraintes :
- [ ] Une éventuelle interface GUI (desktop ou web), dans le cas où un grand nombre de services a monitorer doivent être listés.
- [ ] Certains services pourraient ne pas avoir de méthodes pour répondre à un test. Mais dans ce cas, un ping devrait suffire.
- [ ] Savoir si cet utilitaire sera utilisé en tant que service serveur (tournera en permanence en arrière-plan) ou juste comme logiciel qu'on appelera depuis n'importe quelle machine cliente.

## Enveloppe budgétaire :
```text
A discuter, le client n'en a pas parlé
```
## Planification :
| **Semaine** | **Date** | **Description** |
|-------------|----------|-----------------|
|             |          |                 |
