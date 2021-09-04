from app.tests.conftest import API_PREFIX, Session, TestClient, Course, User


class TestCourse:
    def test_create_course(self, user: User, client: TestClient):
        new_course = {
            "name": "Discrete Maths",
            "description": "hello world",
            "status": "completing",
            "due": "2021-08-29",
            "syllabus": [{"item": 123}],
            "user_id": user.id,
        }
        response = client.post(API_PREFIX + "/courses/", json=new_course)
        data = response.json()
        assert response.status_code == 200
        assert all(item in data.items() for item in new_course.items())

    def test_read_courses(self, course: Course, client: TestClient):
        response = client.get(API_PREFIX + "/courses/")
        data = response.json()
        assert response.status_code == 200
        assert data[0]["name"] == course.name
        assert data[0]["user_id"] == course.user_id
        assert len(data) == 1

    def test_update_course(self, course: Course, client: TestClient):
        response = client.patch(
            API_PREFIX + f"/courses/{course.id}", json={"name": "Linear Algebra"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Linear Algebra"
        assert data["user_id"] == course.user_id

    def test_delete_course(self, course: Course, session: Session, client: TestClient):
        response = client.delete(API_PREFIX + f"/courses/{course.id}")
        assert response.status_code == 200
        course_in_db = session.get(Course, course.id)
        assert course_in_db is None

    def test_course_not_found(self, client: TestClient):
        response = client.get(API_PREFIX + "/courses/69")
        assert response.status_code == 404
