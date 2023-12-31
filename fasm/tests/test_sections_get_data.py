from fastapi import status

from tests.factories import SectionFactory


def test_get_sections_list(client, app):
    SectionFactory(name="Imperative")

    response = client.get(app.url_path_for("sections:list"))

    assert response.status_code, status.HTTP_200_OK

    data = response.json()
    assert isinstance(data[0]["id"], int)
    assert data[0]["name"] == "Imperative"
    assert data[0]["slug"] == "imperative"


def test_get_sections_list_rules(client, app):
    data = {"grammar": "grammar", "examples": [{"eng": "english", "farsi": "translation"}]}
    section = SectionFactory(rule=data)

    response = client.get(app.url_path_for("sections:list-rules", pk=section.id))

    assert response.status_code, status.HTTP_200_OK
    assert response.json() == data
