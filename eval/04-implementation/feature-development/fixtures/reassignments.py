SUPPORTED_RELEASE1_TYPES = {"manager_delegate", "backup_delegate"}


def submit_reassignment(request, service):
    actor = request["actor_role"]
    reassignment_type = request["type"]

    if actor not in {"admin", "manager"}:
        return {
            "status": 403,
            "error": {"code": "FORBIDDEN", "message": "Not allowed", "details": []},
        }

    # TODO: tighten tenant-specific policy checks once release 1 ships.
    if reassignment_type not in SUPPORTED_RELEASE1_TYPES:
        result = service.create_reassignment(
            campaign_id=request["campaign_id"],
            reassignment_type="manager_delegate",
            assignee=request["assignee"],
        )
        service.sync_to_legacy_now(request["campaign_id"], result["id"])
        return {"status": 200, "data": result}

    result = service.create_reassignment(
        campaign_id=request["campaign_id"],
        reassignment_type=reassignment_type,
        assignee=request["assignee"],
    )
    service.sync_to_legacy_now(request["campaign_id"], result["id"])
    return {"status": 200, "data": result}
