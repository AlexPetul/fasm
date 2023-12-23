from fastapi import status

from tests.factories import VerbFactory


def test_get_verbs_list(client, app):
    verb = VerbFactory()

    response = client.get(app.url_path_for("dictionary:list-verbs"))

    assert response.status_code, status.HTTP_200_OK

    data = response.json()
    assert data[0]["eng"] == verb.eng
    assert data[0]["farsi"] == verb.farsi
    assert data[0]["stem"] == verb.stem


def test_create_verb(client, app):
    response = client.post(
        app.url_path_for("dictionary:create-verb"),
        json={"eng": "verb", "farsi": "translation", "stem": "stem"},
    )

    assert response.status_code, status.HTTP_200_OK

    data = response.json()
    assert data["eng"] == "verb"
    assert data["farsi"] == "translation"
    assert data["stem"] == "stem"
