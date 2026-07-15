# Context Notes

Incident response is the skill of managing production failures under pressure. It combines technical diagnosis with communication discipline. The goal is not to find the perfect fix immediately -- it's to stop the bleeding, then investigate properly.

In a lifecycle-aware system, incident response must preserve the release boundary that just shipped. Do not widen scope into redesign during the incident. For brownfield systems, prefer mitigations that fail closed, preserve coexistence, and protect data integrity even if the temporary user experience becomes narrower.
