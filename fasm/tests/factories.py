import factory
from factory.fuzzy import FuzzyText

from conftest import session
from src.auth.models import User
from src.dictionary.models import Verb
from src.sections.models import (
    Question,
    Section,
)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"


class SectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Section
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText(prefix="Section_")


class QuestionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Question
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"


class VerbFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Verb
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    eng = FuzzyText(prefix="Eng_")
    farsi = FuzzyText(prefix="Translation_")
    stem = FuzzyText(prefix="Stem_")
