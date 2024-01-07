from sqladmin import (
    Admin,
    ModelView,
)

from src.dictionary.models import (
    Verb,
    Vocabulary,
)


class VocabularyAdmin(ModelView, model=Vocabulary):
    column_list = [Vocabulary.eng, Vocabulary.farsi]
    form_include_pk = True
    column_default_sort = "eng"
    name_plural = "Vocabulary"


class VerbAdmin(ModelView, model=Verb):
    column_list = [Verb.eng, Verb.farsi, Verb.stem]
    form_include_pk = True
    column_default_sort = "eng"
