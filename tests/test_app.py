from urllib.parse import quote


def test_get_activities_returns_activity_list(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@example.com"
    url = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate_rejected(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "remove_me@example.com"
    url = f"/activities/{quote(activity)}/signup"

    signup_response = client.post(url, params={"email": email})
    assert signup_response.status_code == 200

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    # Arrange
    activity = "Drama Club"
    email = "nobody@example.com"
    url = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
