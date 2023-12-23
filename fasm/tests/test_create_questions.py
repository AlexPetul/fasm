from fastapi import status

from tests.factories import SectionFactory


def test_create_question_manually(client, app):
    section = SectionFactory()
    response = client.post(app.url_path_for("questions:list-create", pk=section.id), json={"content": "answer"})

    assert response.status_code, status.HTTP_201_CREATED

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["content"] == "answer"
