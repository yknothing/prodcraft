# Team Invite Email Backlog Alert

## Detection

- Queue age for invite email dispatch has exceeded the user-visible delay threshold for 18 minutes.
- Provider timeout rate is elevated.
- Invite creation still succeeds, but users are reporting delayed email delivery.
- Invite acceptance is currently healthy for invites that were already delivered.

## Early Evidence

- A recent provider-side timeout spike coincides with the queue backlog.
- No rollback signal exists yet, and there is no legacy fallback path.
- Customer support needs a clear guidance message if delays continue.
