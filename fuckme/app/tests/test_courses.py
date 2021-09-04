from app.tests.conftest import API_PREFIX, Session, TestClient, Course, User, Assignment


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


class TestAssignment:
    def test_create_assignment(self, course: Course, client: TestClient):
        new_assignment = {
            "name": "Huge Exam",
            "description": "Big scary exam",
            "status": "incomplete",
            "due": "2021-12-12",
            "weight": 50,
        }
        response = client.post(
            API_PREFIX + f"/courses/{course.id}/assignments", json=new_assignment
        )
        assert response.status_code == 200
        data = response.json()
        assert all(item in data.items() for item in new_assignment.items())

    def test_read_assignments(
        self, course: Course, assignment: Assignment, client: TestClient
    ):
        response = client.get(API_PREFIX + f"/courses/{course.id}/assignments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == assignment.name
        assert data[0]["course_id"] == assignment.course.id

    def test_read_single_assignment(
        self, course: Course, assignment: Assignment, client: TestClient
    ):
        response = client.get(
            API_PREFIX + f"/courses/{course.id}/assignments/{assignment.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == assignment.name

    def test_read_single_assignment_not_found(self, course: Course, client: TestClient):
        response = client.get(API_PREFIX + f"/courses/{course.id}/assignments/69")
        assert response.status_code == 404
