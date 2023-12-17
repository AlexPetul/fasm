from sqladmin import (
    Admin,
    ModelView,
)

from src.sections.models import (
    Question,
    Section,
)


class SectionAdmin(ModelView, model=Section):
    column_list = [Section.id, Section.name, Section.slug]
