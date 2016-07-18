from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from profiles.models import Customer


class Address(TimeStampedModel):
    """
    Address
    """
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    service = models.TextField(blank=True)
    department = models.TextField(blank=True)
    street_line1 = models.TextField(blank=True)
    street_line2 = models.TextField(blank=True)
    city = models.TextField()
    zipcode = models.TextField()
    tsa_text = models.TextField(blank=True)
    cedex_text = models.TextField(blank=True)
    country = models.TextField(blank=True)

    @property
    def full_text(self):
        """
        Generate text address from structured data
        """
        return  # FIXME


class Organization(TimeStampedModel):
    """
    Brand or Official organization
    """
    name = models.CharField(_("Marque"), max_length=256, unique=True)
    website = models.CharField(_("Site officiel"), blank=True, max_length=2048)
    logo = models.FilePathField(path="/some/path/where/logos/will/be", blank=True)


class Format(TimeStampedModel):
    """
    Format (could be a choicefield instead of a pk?)
    """
    name = models.CharField(_("Nom"), max_length=256)  # ex: "Format A4"
    slug = models.CharField(_("Slug"), max_length=256)  # ex : "FORMAT_A4"


class Zone(TimeStampedModel):
    """
    Determine how to geographically place a bunch of data
    """
    related_format = models.ForeignKey(Format)
    margins = models.FloatField()
    # min height, max height


class FieldType(TimeStampedModel):
    """
    Field (ex: Nom, Prénom, Numéro de téléphone, numéro d'abonné).
    Certains sont génériques, d'autres spécifiques
    Certains sont juste des champs à remplir, d'autres des choix multiples
    """

    # WARN : does not handle boolean fields / multichoice fields

    CHARFIELD = 'CHARFIELD'
    TEXTAREA = 'TEXTAREA'

    WIDGET_CHOICES = (
        (CHARFIELD, 'Charfield'),
        (TEXTAREA, 'TextArea')
    )

    name = models.CharField(_("Nom"), max_length=256)
    description = models.CharField(_("Description (aide)"), max_length=2048)
    default_value = models.CharField(_("Valeur par défaut"), max_length=2048)
    max_size = models.PositiveIntegerField(default=2048)
    widget = models.CharField(choices=WIDGET_CHOICES, max_length=256)  # Use generic fk instead?


class LetterType(TimeStampedModel):
    """
    Letter Type. Ex: Résiliation abonnement téléphonique SFR
    Content is N ZoneTextDuet
    """

    # Letter Purposes
    RESILIATION = 'RESILIATION'
    INFORMATION = 'INFORMATION'
    OTHER = 'OTHER'

    PURPOSE_CHOICES = (
        (RESILIATION, 'Résiliation'),
        (INFORMATION, 'Information'),
        (OTHER, 'Autre'),
    )

    description = models.CharField(_("Description"), max_length=1024)
    purpose = models.CharField(choices=PURPOSE_CHOICES, max_length=256)
    organization = models.ForeignKey(Organization)
    url = models.CharField(_("Site officiel"), blank=True, max_length=2048)
    uploader = models.ForeignKey(Customer, blank=True, null=True)  # If created by a customer
    default_to_address = models.ForeignKey(Address, help_text=_("Adresse du destinataire"))
    sheet_format = models.ForeignKey(Format)


class ZoneTextDuet(TimeStampedModel):
    """
    ZoneTextDuet
    """
    zone = models.ForeignKey(Zone)
    text_to_fill = models.TextField()  # ex: "Je soussigné {first_name} {last_name}"
    letter_type = models.ForeignKey(LetterType)


class FieldInfo(TimeStampedModel):
    """
    FieldInfo, related to a letter type.
    """
    zone_text_duet = models.ForeignKey(ZoneTextDuet)
    # index = models.PositiveSmallIntegerField(_("Ordre d'affichage dans le formulaire")) -> no need
    # Field Font infos
    size = models.PositiveSmallIntegerField(_("Taille de la police"), default=12)
    font = models.CharField(_("Police d'écriture"), max_length=256)


class Letter(TimeStampedModel):
    """
    Actual letter instance which uses a lettertype
    """
    letter_type = models.ForeignKey(LetterType)
    # We can get all the related values, calling self.field_set
    creator = models.ForeignKey(Customer)


class Field(TimeStampedModel):
    """
    Actual field filled, using a field type
    """
    field_type = models.ForeignKey(FieldType)
    letter = models.ForeignKey(Letter)
    value = models.CharField(_("Valeur"), max_length=1024)


class Dispatch(TimeStampedModel):
    """
    A sending of a letter
    """

    CREATED = 'CREATED'
    GENERATION_STARTED = 'GENERATION_STARTED'
    GENERATION_FINISHED = 'GENERATION_FINISHED'

    STATUS_CHOICES = (
        (CREATED, 'Demande créée'),
        (GENERATION_STARTED, 'Génération PDF démarée'),
        (GENERATION_FINISHED, 'Génération PDF terminée')
        # More status here when we will use an API to actually send the mail
    )

    letter = models.ForeignKey(Letter)
    from_address = models.ForeignKey(Address, related_name="from_dispatch", blank=True, null=True)  # Will be use with actual sending
    to_address = models.ForeignKey(Address, related_name="to_dispatch", blank=True, null=True)  # Will be used with actual sending
    status = models.CharField(choices=STATUS_CHOICES, max_length=128)


class Attachment(TimeStampedModel):
    """
    Attachment
    """
    file = models.FileField()
    dispatch = models.ForeignKey(Dispatch, blank=True, null=True)
