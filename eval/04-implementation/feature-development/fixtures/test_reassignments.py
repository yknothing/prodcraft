def test_manager_delegate_is_created(client, reassignment_service):
    response = client.post(
        "/v1/campaigns/camp-123/reassignments",
        json={
            "type": "manager_delegate",
            "assignee": "user-22",
            "actor_role": "manager",
            "campaign_id": "camp-123",
        },
    )

    assert response.status_code == 200
    assert response.json["data"]["reassignment_type"] == "manager_delegate"


def test_forbidden_actor_is_rejected(client, reassignment_service):
    response = client.post(
        "/v1/campaigns/camp-123/reassignments",
        json={
            "type": "manager_delegate",
            "assignee": "user-22",
            "actor_role": "auditor",
            "campaign_id": "camp-123",
        },
    )

    assert response.status_code == 403
