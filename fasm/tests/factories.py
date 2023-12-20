import factory

from fasm.src.sections.models import Section


class SectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Section
        sqlalchemy_session_factory = lambda: common.Session()
