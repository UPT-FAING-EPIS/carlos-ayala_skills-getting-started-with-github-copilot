from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)
ORIGINAL_ACTIVITIES = deepcopy(activities)


def setup_function():
    """Reset in-memory state before each test."""
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def test_signup_for_activity_rejects_duplicate_student():
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity."}


def test_signup_for_activity_adds_student_once():
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert activities[activity_name]["participants"].count(new_email) == 1


def test_remove_participant_unregisters_student():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]
