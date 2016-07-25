from _datetime import datetime
from django.db import transaction

from core.models import *
from profiles.models import *

@transaction.atomic
def init_data():
    """
    Script to fake fixtures for first test
    """

    # CUSTOMER PART

    user = User.objects.create_user(
        first_name="David",
        last_name="Dahan",
        address="13 rue de Montyon, 75009 PARIS",
        phone_number="06 62 10 25 08",
        email="beaucroco@gmail.com",
    )

    customer = Customer(
        user=user
    )

    # LETTER TYPE PART

    organization = Organization(
        name="Numéricable",
        website="http://numericable.fr",
    )

    sheet_format = Format(
        name="Format A4",
        slug="A4"
    )

    field1 = Field(name="Date d'envoi", default_value=datetime.today(), field_type=Field.DATE)
    field2 = Field(name="Numéro client", default_value="123456789", field_type=Field.SHORT_TEXT)
    field3 = Field(name="Services à résilier", field_type=Field.SIMPLE_CHOICE,
                   choices="le service TV;le service Internet;l'ensemble des services")
    field4 = Field(name="Date de résiliation", field_type=Field.DATE)

    letter_type = LetterType(
        fields=(field1, field2, field3, field4,),
        description="Résiliation abonnement Numéricable",
        purpose=LetterType.RESILIATION,
        organization=organization,
        url="http://offres.numericable.fr/",
        uploader=None,
        default_to_address="NUMERICABLE\nService Clients\nTSA 61000\n92894 Nanterre cedex 9",
        sheet_format=sheet_format
    )

    # LETTER CONTENT

    letter = Letter(
        letter_type=letter_type,
        creator=customer
    )

    # WARN: how to translate data type to str? (here is an exemple : date to string)
    field_value1 = FieldValue(field=field1, letter=letter, value="20 septembre 2015")
    field_value2 = FieldValue(field=field2, letter=letter, value="91793889")
    field_value3 = FieldValue(field=field3, letter=letter, value="l'ensemble des services")
    field_value4 = FieldValue(field=field4, letter=letter, value="14 octobre 2015")
