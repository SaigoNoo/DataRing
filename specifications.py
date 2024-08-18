class CLI:
    """
    Classe qui gère l'asynchrone et permet l'itération en differée pour pinger les DNS sans attendre la fin du prècedent.

    Autheur: Doussis Giorgios
    Date: 18-08-2023
    """

    async def run_ping_when_zero(self, dns: dict):
        """
        Permettra de lancer le ping dès que le timer (parametre duration dans le dns.json) en async

        + ---- PRE -----------------------------------------------------------
        | :param dns: Contient toutes les données contenues dans le dns.json
        + ---- POST ----------------------------------------------------------
        | :return: coroutine
        + --------------------------------------------------------------------
        """


class DataRingRequest:
    """
    Classe qui permetra de gérer les pings et de formater les données pour les autres classes
    """

    def __init__(self):
        """
        Méthode qui contiendra la liste des DNS actualisée (à chaud)

        + ---- PRE ---------------------------------------------------------------
        | Pas de PRE
        + ---- POST --------------------------------------------------------------
        | Pas de POST
        + ---- RAISE -------------------------------------------------------------
        | - Risque de crash shi le fichier dns.json est mal formaté ou innexistant
        + -------------------------------------------------------------------------
        """

    def update_config(self):
        """
        Méthode qui mettra à jour le contenu de self.dns lors de son appel

        + ---- PRE ----------------------------------------------------------------
        | - Il faut que le fichier dns.json existe et sois correctement formaté
        + ---- POST ---------------------------------------------------------------
        | - La variable self.dns sera actualisé
        + ---- RAISE --------------------------------------------------------------
        | - Risque de crash shi le fichier dns.json est mal formaté ou innexistant
        + -------------------------------------------------------------------------
        :return: None
        """

    def test_dns(self, dns: dict):
        """
        Méthode qui teste un ping sur le DNS et renvoie un dictionnaire avec des statistiques
        après avoir actualisé le self.dns

        + ---- PRE ----------------------------------------------------------------
        | :param: dns > doit être un dictionnaire contenant les paramètres du fichier dns.json
        + ---- POST ----------------------------------------------------------------
        | - Renvoie un dictionnaire après le ping de 2ms
        + --------------------------------------------------------------------------
        :return: dict de statistiques
        """


class Config:
    """
    Classe qui permet de gérer le fichier DNS.json via des méthodes (et via API indirectement)
    ! ATTENTION !
    Je parle de crash dans les RAISES mais il n'y quasiment aucune chance qu'un crash surviennent
    car les ajouts se font via l'API qui s'assurent que le format soit correct et de renvoyer un message
    et annuler une mauvaise action !
    """

    def __init__(self):
        """
        Contiendra le contenu du fichier dns.json

        + ---- PRE ---------------------------------------------------------------------
        | - Il faut que le fichier dns.json existe et sois correctement formaté
        + ---- POST --------------------------------------------------------------------
        | - Va stocker dans self.dns le dict dns.json
        + ---- RAISE -------------------------------------------------------------------
        | - Risque de crash shi le fichier dns.json est mal formaté ou innexistant
        + ------------------------------------------------------------------------------
        """

    def add_entry(self, label: str, enable: int, dns: str, priority: int, period: int):
        """
        Permet d'ajouter / réecrire un DNS mais en mémoire
        + ---- PRE -----------------------------------------------------------------------------
        | :param label: Étiquette identifiant le DNS dans le dns.json
        | :param enable: Si 1 c'est True, si 0 c'est False
        | :param dns: IP ou DNS à tester
        | :param priority: Entre 1 et 4, à lire dans le Readme.md
        | :param period: Timeout à attendre avant de lancer le ping
        + ---- POST -----------------------------------------------------------------------------
        | - Le nouveau DNS est stockée dans la mémoire alloué au script ! NON PERMANANT !
        + ---------------------------------------------------------------------------------------
        :return: None
        """

    def delete_entry(self, label: str):
        """
        Permet de supprimer un DNS mais en mémoire
        + ---- PRE ------------------------------------------------------------------------
        | :param label: Étiquette identifiant le DNS dans le dns.json
        + ---- POST -----------------------------------------------------------------------
        | Le DNS est supprimé dans la mémoire alloué au script ! NON PERMANANT !
        + ---- RAISE ----------------------------------------------------------------------
        | - Si le label n'est pas dans le dns.json, cela provoquera un crash !
        + ---------------------------------------------------------------------------------
        :return: None
        """

    def save_config(self):
        """
        Permet de mettre à jour le dictionnaire en mémoire en JSON vers le fichier dns.json
        + --- PRE -------------------------------------------------------------------------
        | - Il faut que self.dns contiennent quelque chose et formaté en format dictionnaire
        + ---- POST -----------------------------------------------------------------------
        | - Le contenu du self.dns est stocké de facon permanante dans le fichier dns.json
        + ---- RAISE ----------------------------------------------------------------------
        | - Si le self.dns est vide ou est mal formaté, le programme pourrait crash !
        + ---------------------------------------------------------------------------------
        :return: None
        """


class Notification:
    """
    Permet d'envoyer des notifications Discord (et plus pour les prochaines updates) si le DNS est configuré pour...
    """

    def __init__(self):
        """
        Contiendra les URL vers les services de notifications
        + ---- PRE ---------------------------------------------------------------------------
        | Rien
        + ---- POST --------------------------------------------------------------------------
        | Rien
        + ---- RAISE -------------------------------------------------------------------------
        | - Le self.discord doit contenir une URL valide
        + ------------------------------------------------------------------------------------
        """

    def send_notification(self, data: dict):
        """
        Cette méthode enverra une notification vers le service specifié
        + ---- PRE ----------------------------------------------------------------------------
        | - le self.discord doit contenir une URL Webhook valide
        + ---- POST ---------------------------------------------------------------------------
        | - Cela générera à l'aide de la libraire discord-webhook un objet de type embed
        |   et enverra via une requete get / post le message au service concerné
        + ---- RAISE --------------------------------------------------------------------------
        | - Si l'URL est erronée ou vide, il n'y aura pas de crash mais le message ne sera pas envoyé
        |   et une erreur 400 sera renvoyé !
        + -------------------------------------------------------------------------------------
        :param data: dictionnaire contenant toutes les stats suite au ping
        :return: str > Code réponse HTTP
        """


class Error:
    """
    Classe qui va retenir quels DNS sont erronés pour éviter de notifier par message l'erreur en boucle
    """

    def __init__(self):
        """
        Cette méthode contiendra un tableau avec les label qui rencontrent une erreur

        + ---- PRE ----------------------------------------------------------------------------
        | Rien
        + ---- POST ---------------------------------------------------------------------------
        | - Crée un self.errors list vide
        + -------------------------------------------------------------------------------------
        """

    def add(self, label: str):
        """
        Ajoute un label dans la lise self.errors

        + ---- PRE ------------------------------------------------------------------------------
        | - Il faut que le self.errors soit initialisé
        + ---- POST -----------------------------------------------------------------------------
        | - Ca encode en mémoire alloué au script le label du DNS erroné
        + ---------------------------------------------------------------------------------------
        :param label: str étant le label du DNS
        :return: None
        """

    def rem(self, label: str):
        """
        Supprime un label dans la lise self.errors

        + ---- PRE ------------------------------------------------------------------------------
        | - Il faut que le self.errors soit initialisé et contienne le label
        + ---- POST -----------------------------------------------------------------------------
        | - Ca retire de la mémoire alloué au script le label du DNS erroné
        + ---------------------------------------------------------------------------------------
        :param label: str étant le label du DNS
        :return: None
        """


class Logs:
    """
    Logs va gérer les logs dans le fichier log.json et garder un historique des pings (permettra la génération d'un
    graphique dans les prochains updates
    """

    def __init__(self):
        """
        Contiendra le contenu du fichier log.json

        + ---- PRE ---------------------------------------------------------------------
        | Rien
        + ---- POST --------------------------------------------------------------------
        | La variable self.file va être initialisée
        + ---- RAISE -------------------------------------------------------------------
        | - Crash possible si le fichier n'existe pas ou n'est pas encodé en JSON
        + ------------------------------------------------------------------------------
        """

    def add(self, data: dict):
        """
        Permettra d'ajouter un événement dans le log.json

        + ---- PRE ---------------------------------------------------------------------
        | :param data: dictionnaire qui contiendra les stats du ping
        + --- POST ---------------------------------------------------------------------
        | - Va créer une structure JSON avec la structure suivante Year > Month > Day > Hour > Minute > Seconde
        | - Va stocker les stats du ping dans la clé Seconde
        | - En fonction de si le PING a réussi, des clés stats pourront s'ajouter, ms_avg, etc...
        + ------------------------------------------------------------------------------

        :return: None
        """


async def root():
    """
    Fonction liée à FastAPI qui renvoie la requete web à la docs

    + ---- PRE ------------------
    | Rien
    + ---- POST -----------------
    | Renvoie l'URL vers la docs
    + ---------------------------
    :return: RedirectUrl
    """


async def add(tag: str, enable: int, dns: str, priority: int, period: int):
    """
    Fonction liée à FastAPI qui exploite Config().add() pour ajouter un DNS via API Request

    + ---- PRE ------------------
    | :param: tag > str identifiant le DNS
    | :param: enable > int qui définir si le script doit pinger ou non le DNS
    | :param: dns > Addresse / IP à ping
    | :param: priority > int définie dans le Readme.md
    | :param: period > int qui défini la durée differée a attendre avant de ping
    + ---- POST -----------------
    | - Ajoute le DNS à la mémoire et appelle Config().save()
    + ---------------------------
    :return: None
    """


async def delete(tag: str):
    """
    Fonction liée à FastAPI qui exploite Config().rem() pour supprimer un DNS via API Request

    + ---- PRE ------------------
    | :param: tag > str identifiant le DNS
    + ---- POST -----------------
    | - Supprime le DNS à la mémoire et appelle Config().save()
    + ---------------------------
    :return: None
    """


async def update(tag: str, enable: int, dns: str, priority: int, period: int):
    """
    Fonction liée à FastAPI qui exploite Config().add() pour mettre à jour un DNS via API Request

    + ---- PRE ------------------
    | :param: tag > str identifiant le DNS
    | :param: enable > int qui définir si le script doit pinger ou non le DNS
    | :param: dns > Addresse / IP à ping
    | :param: priority > int définie dans le Readme.md
    | :param: period > int qui défini la durée differée a attendre avant de ping
    + ---- POST -----------------
    | - Modifie le DNS à la mémoire et appelle Config().save()
    + ---------------------------
    :return: None
    """
