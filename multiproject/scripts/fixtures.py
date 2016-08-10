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
        email="david.dahan3@gmail.com",
    )

    customer = Customer.objects.create(
        user=user
    )

    # FIELDS (can be use in 1 -> N letter types)

    field1 = Field.objects.create(name="Date d'envoi", default_value=datetime.today(), field_type=Field.DATE)
    field2 = Field.objects.create(name="Numéro client", default_value="123456789", field_type=Field.SHORT_TEXT)
    field3 = Field.objects.create(name="Services à résilier", field_type=Field.SIMPLE_CHOICE,
        choices="le service TV;le service Internet;l'ensemble des services")
    field4 = Field.objects.create(name="Date de résiliation", field_type=Field.DATE)
    field5 = Field.objects.create(name="Ville", field_type=Field.SHORT_TEXT)

    field6 = Field.objects.create(name="N° de contrat", default_value="123456789", field_type=Field.SHORT_TEXT)
    field7 = Field.objects.create(name="Logement concerné par la résiliation", field_type=Field.SHORT_TEXT)
    field8 = Field.objects.create(name="Motif de résiliation", field_type=Field.SIMPLE_CHOICE,
        choices="changement de domicile;")

    # LETTER TYPE 1

    organization_1 = Organization.objects.create(
        name="Numéricable",
        website="http://numericable.fr",
    )

    letter_type_1 = LetterType.objects.create(
        html_template="resiliation_numericable.html",
        description="Résiliation abonnement Numéricable",
        purpose=LetterType.RESILIATION,
        organization=organization_1,
        url="http://offres.numericable.fr/",
        uploader=None,
        default_to_address="NUMERICABLE\nService Clients\nTSA 61000\n92894 Nanterre cedex 9",
    )
    letter_type_1.fields.add(field1, field2, field3, field4, field5)

    # LETTER TYPE 2

    organization_2 = Organization.objects.create(
        name="Amaguiz",
        website="https://www.amaguiz.com"
    )

    letter_type_2 = LetterType.objects.create(
        html_template="resiliation_amaguiz.html",
        description="Résiliation abonnement Amaguiz",
        purpose=LetterType.RESILIATION,
        organization=organization_2,
        url="https://www.amaguiz.com/resilier-assurance",
        uploader=None,
        default_to_address="Amaguiz.com\nService Client\nTSA 47717\n35577 Cesson Sevigne CEDEX",
    )
    letter_type_2.fields.add()



    # LETTER CONTENT

    letter = Letter.objects.create(
        letter_type=letter_type_1,
        creator=customer
    )

    # WARN: how to translate data type to str? (here is an exemple : date to string)
    FieldValue.objects.create(field=field1, letter=letter, value="20 septembre 2015")
    FieldValue.objects.create(field=field2, letter=letter, value="91793889")
    FieldValue.objects.create(field=field3, letter=letter, value="l'ensemble des services")
    FieldValue.objects.create(field=field4, letter=letter, value="14 octobre 2015")