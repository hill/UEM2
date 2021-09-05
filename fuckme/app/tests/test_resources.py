from typing import Callable, List
from app.tests.conftest import (
    API_PREFIX,
    Session,
    TestClient,
    User,
    Topic,
    Resource,
    TEST_SUPERUSER_PASSWORD,
)
from app.tests import util


class TestResource:
    def test_create_resource(
        self, user: User, topic: Topic, authenticated_client: TestClient
    ):
        new_resource = {
            "name": "google",
            "url": "google.com",
            "user_id": user.id,
            "topics": [topic.id],
        }
        response = authenticated_client.post(
            API_PREFIX + "/resources/", json=new_resource
        )
        data = response.json()
        assert response.status_code == 200

        assert data["name"] == new_resource["name"]
        assert data["url"] == new_resource["url"]
        assert data["user_id"] == new_resource["user_id"]
        assert len(data["topics"]) == 1
        assert data["topics"][0]["name"] == topic.name

    def test_read_resources(
        self,
        resource: Resource,
        get_request: Callable[[str], dict],
    ):
        data = get_request("/resources/")
        assert data[0]["name"] == resource.name
        assert data[0]["url"] == resource.url
        assert data[0]["user_id"] == resource.user_id
        assert len(data) == 1

    def test_search_resources(
        self,
        many_resources: List[Resource],
        topic: Topic,
        get_request: Callable[[str], dict],
    ):
        data = get_request("/resources/?search=goog")
        assert many_resources[0].name == "Google"
        assert data[0]["name"] == many_resources[0].name
        assert data[0]["url"] == many_resources[0].url
        assert data[0]["user_id"] == many_resources[0].user_id
        assert len(data) == 1

        # check multiple matches but not all results will return
        data = get_request("/resources/?search=o")
        for item in data:
            assert "o" in item["name"]

        # TODO(TOM): search by multiple topics
        # search by topic name
        data = get_request(f"/resources/?topics={topic.name}")
        assert len(data) == 2

        # check search is case insensitive
        data = get_request(f"/resources/?topics={topic.name.upper()}")
        assert len(data) == 2

        # search by topic id
        data = get_request(f"/resources/?topics={topic.id}")
        assert len(data) == 2

        # search by topic id and search term
        data = get_request(f"/resources/?search=goog&topics={topic.id}")
        assert len(data) == 1
        assert data[0]["name"] == "Google"

    def test_update_resource(
        self, resource: Resource, authenticated_client: TestClient
    ):
        response = authenticated_client.patch(
            API_PREFIX + f"/resources/{resource.id}", json={"name": "Xoogle"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Xoogle"
        assert data["url"] == resource.url
        assert data["user_id"] == resource.user_id
        assert data["votes"] == resource.votes

    def test_delete_resource(
        self, resource: Resource, session: Session, authenticated_client: TestClient
    ):
        response = authenticated_client.delete(API_PREFIX + f"/resources/{resource.id}")
        assert response.status_code == 200
        resource_in_db = session.get(Resource, resource.id)
        assert resource_in_db is None

    def test_upvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count + 1

    def test_downvote_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=-1")
        data = response.json()
        assert response.status_code == 200
        assert data["votes"] == resource.votes
        assert data["votes"] == old_vote_count - 1

    def test_too_many_votes_resource(self, resource: Resource, client: TestClient):
        old_vote_count = resource.votes
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/vote?vote=100")
        assert response.status_code == 400
        assert resource.votes == old_vote_count

    def test_mark_as_broken(self, resource: Resource, client: TestClient):
        assert resource.broken == 0
        response = client.patch(API_PREFIX + f"/resources/{resource.id}/broken")
        assert response.status_code == 200
        assert resource.broken == 1

    def test_resource_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/resources/69")
        assert response.status_code == 404

    def test_superuser_modify_resources(
        self, resource: Resource, superuser: User, client: TestClient
    ):
        # modify a resource as a superuser
        newURL = "http://new_url.com"
        assert resource.user.id != superuser.id
        r = client.patch(
            API_PREFIX + f"/resources/{resource.id}",
            json={"url": newURL},
            headers=util.user_authentication_headers(
                client=client, email=superuser.email, password=TEST_SUPERUSER_PASSWORD
            ),
        )
        assert r.status_code == 200
        data = r.json()
        assert data["url"] == newURL

        # delete a resource as a superuser
        r = client.delete(
            API_PREFIX + f"/resources/{resource.id}",
            headers=util.user_authentication_headers(
                client=client, email=superuser.email, password=TEST_SUPERUSER_PASSWORD
            ),
        )
        assert r.status_code == 200
