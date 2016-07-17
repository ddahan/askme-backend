from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from profiles.models import Customer  # Should not be redlined, works well.


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


class Position(TimeStampedModel):
    """
    Position
    """
    value = models.CharField(_("Position"), max_length=1024, unique=True)  # How to represent it?


class FieldType(TimeStampedModel):
    """
    Field (ex: Nom, Prénom, Numéro de téléphone, numéro d'abonné).
    Certains sont génériques, d'autres spécifiques
    """

    # TODO : does not handle boolean fields

    CHARFIELD = 'CHARFIELD'
    TEXTAREA = 'TEXTAREA'

    WIDGET_CHOICES = (
        (CHARFIELD, 'Charfield'),
        (TEXTAREA, 'TextArea')
    )

    name = models.CharField(_("Nom"), max_length=256)
    description = models.CharField(_("Description (aide)"), max_length=2048)
    default_value = models.CharField(_("Valeur par défaut"), max_length=2048)
    max_length = models.PositiveIntegerField(default=2048)
    widget = models.CharField(choices=WIDGET_CHOICES, max_length=256)  # Use generic fk instead?


class DuetFieldPos(TimeStampedModel):
    """
    Duet : couples de pk de fields et de positions associées
    """

    field = models.ForeignKey(FieldType)
    positions = models.ManyToManyField(Position)


class LetterType(TimeStampedModel):
    """
    Letter Type. Ex: Résiliation abonnement téléphonique SFR
    """

    # Template Formats
    FORMAT_A4 = 'A4'

    PAGE_FORMAT_CHOICES = (
        (FORMAT_A4, 'Format A4'),
    )

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
    purpose = models.CharField(choices=PURPOSE_CHOICES, max_length=256)  # could be a FK to a model?
    organization = models.ForeignKey(Organization)
    url = models.CharField(_("Site officiel"), blank=True, max_length=2048)
    sheet_format = models.CharField(choices=PAGE_FORMAT_CHOICES, max_length=256)
    # TODO: text inside with information to be filled : {field-name}
    uploader = models.ForeignKey(Customer, blank=True, null=True)  # If this letter type has been created by a customer
    default_to_address = models.ForeignKey(Address, help_text=_("Adresse du destinataire"))


class FieldInfo(TimeStampedModel):
    """
    FieldInfo, related to a letter type.
    """
    letter_type = models.ForeignKey(LetterType)
    # Field data
    field_pos = models.ForeignKey(DuetFieldPos)
    index = models.PositiveSmallIntegerField(_("Ordre d'affichage dans le formulaire"))
    # Field Font infos
    size = models.PositiveSmallIntegerField(_("Taille de la police"), default=12)
    font = models.CharField(_("Police d'écriture"), max_length=256)


class Letter(TimeStampedModel):
    """
    Actual letter which uses a lettertype
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
