def submit_reassignment(request, service):
    actor = request["actor_role"]
    reassignment_type = request["type"]

    if actor not in {"admin", "manager"}:
        return {
            "status": 403,
            "error": {"code": "FORBIDDEN", "message": "Not allowed", "details": []},
        }

    if reassignment_type == "manager_delegate":
        result = service.create_reassignment(
            campaign_id=request["campaign_id"],
            reassignment_type="manager_delegate",
            assignee=request["assignee"],
        )
        service.sync_to_legacy_now(request["campaign_id"], result["id"])
        return {"status": 200, "data": result}

    if reassignment_type == "backup_delegate":
        result = service.create_reassignment(
            campaign_id=request["campaign_id"],
            reassignment_type="backup_delegate",
            assignee=request["assignee"],
        )
        service.sync_to_legacy_now(request["campaign_id"], result["id"])
        return {"status": 200, "data": result}

    return {
        "status": 400,
        "error": {
            "code": "UNSUPPORTED_REASSIGNMENT_TYPE",
            "message": "Unsupported reassignment type for release 1",
            "details": [],
        },
    }
