from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class BankAccount(models.Model):
    """
    Bank account
    """
    iban = models.CharField(_("IBAN"), max_length=34)
    bic = models.CharField(_("BIC"), max_length=12)

    def __str__(self):
        return self.iban


class Company(models.Model):
    """
    Société (ou auto-entreprise)
    """
    AE = 'AE'
    SA = 'SA'
    EI = 'EI'
    SARL = 'SARL'
    EURL = 'EURL'
    EIRL = 'EIRL'
    SAS = 'SAS'
    SASU = 'SASU'

    COMPANY_TYPE_CHOICES = (
        (AE, 'Auto-entrepreneur'),
        (SA, 'Société anonyme'),
        (EI, 'Entreprise individuelle'),
        (SARL, 'Société anonyme à responsabilité limitée'),
        (EURL, 'Entreprise unipersonnelle à responsabilité limitée'),
        (EIRL, 'Entreprise individuelle à responsabilité limitée'),
        (SAS, 'Société par actions simplifiée'),
        (SASU, 'Société par actions simplifiée unipersonnelle'),
    )

    name = models.CharField(_("Nom"), blank=True)  # Si auto-entrepreneur
    type = models.CharField(_("Type"), choices=COMPANY_TYPE_CHOICES)
    logo = models.CharField(_("URL du logo"))
    address = models.CharField(_("Adresse"), max_length=1024)
    siret = models.CharField(_("SIRET"), max_length=256)
    siren = models.CharField(_("SIREN"), max_length=256)
    bank_account = models.ForeignKey(BankAccount)

    def __str__(self):
        return self.name


class Freelance(models.Model):
    """
    Freelance
    """

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company, null=True, blank=True)

    def __str__(self):
        return self.user


class Client(models.Model):
    """
    Client
    """

    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.user


class Mission(models.Model):
    """
    Mission
    """

    FIXED_PRICE = 'FIXED_PRICE'  # Forfait
    TIMED_PRICE = 'TIMED_PRICE'  # Régie

    MISSION_MODE_CHOICES = (
        (FIXED_PRICE, 'Forfait'),
        (TIMED_PRICE, 'Régie'),
    )

    start = models.DateField(_("Début"))
    end = models.DateField(_("Fin"), blank=True, null=True)
    mode = models.CharField(_("Type"), choices=MISSION_MODE_CHOICES, max_length=256)
    performer = models.ForeignKey(Freelance)
    client = models.ForeignKey(Client)
    short_description = models.CharField(max_length=1024, blank=True)
    long_description = models.TextField()

    def __str__(self):
        return "{} - Du {} au {}".format(self.client.company, self.start, self.end)


class WorkUnit(models.Model):
    """
    Une façon de décomposer une mission en unités de temps
    # TODO: définir comment modéliser cette partie
    """

    def __str__(self):
        pass  # TODO


class Clause(models.Model):
    """
    Clause contractuelle (peut être utilisée pour décrire les clauses existantes)
    """
    # TODO: ajouter les category choices

    description = models.TextField(_("Description"))
    category = models.CharField(_("Catégorie"), max_length=256)


class Contract(models.Model):
    """
    Contrat de travail
    # Idée : pouvoir rendre public pour aspect communautaire
    """

    created = models.DateField(_("Date d'édition"))
    mission = models.ForeignKey(Mission, blank=True, null=True)
    clauses = models.ManyToManyField(Clause, through="ClauseInContract",
                                     through_fields=('contract', 'clause'))
    signed = models.BooleanField(_("Signé ?"))

    def __str__(self):
        return "{} - {}".format(self.mission, self.created)


class ClauseInContract(models.Model):
    """
    Table de liaison M2M entre une Clause et un Contract
    """

    contract = models.ForeignKey(Contract)
    clause = models.ForeignKey(Clause)
    index = models.PositiveSmallIntegerField(_("Ordre"))


class ClauseInInvoice(models.Model):
    """
    Table de liaison M2M entre une Clause et une Invoice
    """

    invoice = models.ForeignKey(Invoice)
    clause = models.ForeignKey(Clause)
    index = models.PositiveSmallIntegerField(_("Ordre"))


class Invoice(models.Model):
    """
    Facture
    """

    CHECK = 'CHECK'
    TRANSFER = 'TRANSFER'
    ONLINE_TIER = 'ONLINE_TIER'  # Ex: Paypal
    OTHER = 'OTHER'

    PAYMENT_MODE_CHOICES = (
        (CHECK, 'Chèque'),
        (TRANSFER, 'Virement'),
        (ONLINE_TIER, 'Tier en ligne'),
        (OTHER, 'Autre')
    )

    mission = models.ForeignKey(Mission)
    identifier = models.CharField(_("Numéro"), max_length=256, unique=True)
    issue_date = models.DateField(_("Date d'émission"), default=timezone.now)
    payment_mode = models.CharField(_("Mode de règlement"), blank=True, null=True)
    payment_date = models.DateField(_("Date de réglement"), blank=True, null=True)
    price_excluding_taxes = models.DecimalField(_("Prix HT"), max_digits=8, decimal_places=2)
    price_taxes = models.DecimalField(_("TVA"), max_digits=8, decimal_places=2)
    price_including_taxes = models.DecimalField(_("Prix TTC"), max_digits=8, decimal_places=2)
    canceled = models.BooleanField(default=False)
    additional_clauses = models.ManyToManyField(Clause, through="ClauseInInvoice",
                                                through_fields=('invoice', 'clause'))

    def __str__(self):
        return "{} - {} ({})".format(self.identifier, self.mission, self.issue_date)


class Incident(models.Model):
    """
    Incident (ex: retard de paiement)
    """
