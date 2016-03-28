from django.db import models

# User app #########################################################################################


class User():
    pass


class Asker():
    user = models.ForeignKey(User)


class Replyer():
    user = models.ForeignKey(User)


# Core app #########################################################################################


class Survey():
    title = models.Charfield()
    description = models.Charfield()
    creator = models.ForeignKey(Asker)
    deadline = models.Datetime()
    price = models.DecimalField()


class Question():
    title = models.Charfield()
    help_text = models.Charfield()
    survey = models.ForeignKey(Survey)
    required = models.BooleanField()
    accepted = models.BooleanField() # peut être refusée si le contenu est incohérent
    prev = models.ForeignKey(Question)
    next = models.ForeignKey(Question)
    kind = models.Choicetype('TEXT', 'MULTIPLE_CHOICE', 'CHECKBOXES', 'SCALE', 'RANGE',
                             'DATETIME')


# Options
class Option():
    class Meta:
        abstract = True

    question = models.ForeignKey(Question)
    prev = models.ForeignKey(Option)
    next = models.ForeignKey(Option)


class TextOption(Option):  # Text questions
    pass  # TODO: sûrement pas nécessaire


class ChoiceOption(Option):  # multiple choice and checkboxes questions
    choice = models.Charfield()


class ScaleOption(Option):  # scale questions
    lower_bound = models.IntegerField(min_value=0)
    upper_bound = models.IntegerField(max_value=10)
    lower_bound_label = models.Charfield(blank=True)
    upper_bound_label = models.Charfield(blank=True)


class RangeOption(Option):  # Range question
    lower_bound = models.FloatField()
    upper_bound = models.FloatField()


class DateTimeOption(Option):
    datetime = models.Datetime()


# Answers

class Answer():
    class Meta:
        abstract = True

    question = models.ForeignKey(Question)
    replyer = models.ForeignKey(Replyer)


class TextAnswer(Answer):
    text = models.Charfield()


class ChoiceAnswer(Answer):
    choice = models.ForeignKey(ChoiceOption)


class ScaleAnswer(Answer):
    choice = models.PositiveField()


class RangeAnswer(Answer):
    lower_choice = models.FloatField()
    upper_choice = models.FloatField()


class DateTimeAnswer(Answer):
    choice = models.Datetime()

####################################################################################################


class ConditionalDisplayRule():
    """ Permet d'afficher une question seulement si la condition est remplie """
    question = models.ForeignKey(Question)

    trigger_on_choice_option = models.ForeignKey(ChoiceOption, blank=True)
    # etc.. TODO: ajouter des trigger sur différents

    activated_question = models.ForeignKey(Option)


####################################################################################################
# Règle quelque part : en fonction du type de question, le type d'option accepté, et leur nombre min/max
ALLOWED_OPTIONS_PER_QUESTIONS = (('TEXT', 'TextOption', 1, 1),
                                 ('MULTIPLE_CHOICE', 'ChoiceOption', 2, 10),
                                 ('CHECKBOXES', 'ChoiceOption', 1, 15),
                                 ('SCALE', 'ScaleOption', 1, 1),
                                 ('RANGE', 'RangeOption', 1, 1),
                                 ('DATE', 'DateTimeOption', 1, 1)
                                )

# TODO: Question : plus performant d'ordonner par liste chainée ou par champ order ?