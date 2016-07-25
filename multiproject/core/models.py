from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from profiles.models import Customer


# class Address(TimeStampedModel):
#     """
#     Address
#     """
#     first_name = models.TextField(blank=True)
#     last_name = models.TextField(blank=True)
#     service = models.TextField(blank=True)
#     department = models.TextField(blank=True)
#     street_line1 = models.TextField(blank=True)
#     street_line2 = models.TextField(blank=True)
#     city = models.TextField()
#     zipcode = models.TextField()
#     tsa_text = models.TextField(blank=True)
#     cedex_text = models.TextField(blank=True)
#     country = models.TextField(blank=True)
#
#     @property
#     def full_text(self):
#         """
#         Generate text address from structured data
#         """
#         return  # FIXME


class Organization(TimeStampedModel):
    """
    Brand or Official organization
    """
    name = models.CharField(_("Marque"), max_length=256, unique=True)
    website = models.CharField(_("Site officiel"), blank=True, max_length=2048)
    logo = models.FilePathField(path="/some/path/where/logos/will/be", blank=True)

    def __str__(self):
        return self.name


class Field(TimeStampedModel):
    """
    Field (ex: Nom, Prénom, Numéro de téléphone, numéro d'abonné).
    Certains sont génériques, d'autres spécifiques
    Certains sont juste des champs à remplir, d'autres des choix multiples
    """

    SHORT_TEXT = 'SHORT_TEXT'
    LONG_TEXT = 'LONG_TEXT'
    INTEGER = 'INTEGER'
    DATE = 'DATE'
    TIME = 'TIME'
    DATETIME = 'DATETIME'
    SIMPLE_CHOICE = 'SIMPLE_CHOICE'
    MULTI_CHOICE = 'MULTI_CHOICE'

    FIELD_TYPE_CHOICES = (
        (SHORT_TEXT, 'Short Text'),
        (LONG_TEXT, 'Long Text'),
        (INTEGER, 'Integer'),
        (SIMPLE_CHOICE, 'Simple Choice'),
        (MULTI_CHOICE, 'Multiple Choice'),
        (DATE, 'Date'),
        (TIME, 'Time'),
        (DATETIME, 'DateTime'),
    )

    name = models.CharField(_("Nom"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128)
    description = models.CharField(_("Description (aide)"), blank=True, null=False, max_length=2048)
    default_value = models.CharField(_("Défaut"), blank=True, null=False, max_length=2048)
    # For simple/multiple choices only. Separeted by semicolons
    choices = models.TextField(_("Choix"), blank=True, null=False)
    max_size = models.PositiveIntegerField(default=2048)
    field_type = models.CharField(choices=FIELD_TYPE_CHOICES, max_length=256)

    def __str__(self):
        return '{} ({})'.format(self.name, self.get_field_type_display())

    def save(self, *args, **kwargs):
        """
        Create a default slug based on the field name
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Field, self).save(*args, **kwargs)


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

    fields = models.ManyToManyField(Field)
    html_template = models.FilePathField(path='html_templates/', recursive=True, max_length=1024)
    organization = models.ForeignKey(Organization)
    uploader = models.ForeignKey(Customer, blank=True, null=True)  # If created by a customer
    default_to_address = models.CharField(_("Adresse du destinataire"), max_length=1024)
    description = models.CharField(_("Description"), max_length=1024)
    purpose = models.CharField(choices=PURPOSE_CHOICES, max_length=256)
    url = models.CharField(_("Site officiel"), blank=True, max_length=2048)

    def __str__(self):
        return self.description


class Letter(TimeStampedModel):
    """
    Actual letter instance which uses a lettertype
    """
    letter_type = models.ForeignKey(LetterType)
    # We can get all the related values, calling self.field_set
    creator = models.ForeignKey(Customer)

    def __str__(self):
        return 'Letter #{}, sent by {}'.format(self.pk, self.creator)


class FieldValue(TimeStampedModel):
    """
    Actual filled field, using a field type
    """
    field = models.ForeignKey(Field)
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

    RECOMMANDE = 'RECOMMANDE'
    RECOMMANDE_AR = 'RECOMMANDE_AR'
    SIMPLE = 'SIMPLE'

    DISPATCH_TYPE = (
        (RECOMMANDE, 'Lettre recommandée sans AR'),
        (RECOMMANDE_AR, 'Lettre recommandée avec AR'),
        (SIMPLE, 'Lettre classique')
    )

    letter = models.ForeignKey(Letter)
    from_address = models.CharField(max_length=1024)
    to_address = models.CharField(max_length=1024)
    status = models.CharField(choices=STATUS_CHOICES, max_length=128)


class Attachment(TimeStampedModel):
    """
    Attachment
    """
    file = models.FileField()
    dispatch = models.ForeignKey(Dispatch, blank=True, null=True)
