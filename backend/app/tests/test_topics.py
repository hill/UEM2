from app.tests.conftest import API_PREFIX, TestClient, User, Topic


class TestTopic:
    def test_create_topic(self, user: User, client: TestClient):
        new_topic = {"name": "Algebra"}
        response = client.post(API_PREFIX + "/topics/", json=new_topic)
        data = response.json()
        assert response.status_code == 200
        # check topic is a subset of the response
        assert all(item in data.items() for item in new_topic.items())

    def test_read_topics(self, topic: Topic, client: TestClient):
        response = client.get(API_PREFIX + "/topics/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == topic.name
        assert len(data) == 1

    def test_read_topic(self, topic: Topic, client: TestClient):
        response = client.get(API_PREFIX + f"/topics/{topic.id}")
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == topic.name

    def test_read_topic_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/topics/69")
        assert response.status_code == 404
