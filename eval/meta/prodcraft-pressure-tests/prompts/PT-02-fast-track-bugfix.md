# PT-02 Fast-Track Bugfix Prompt

Fix a small but real bug in an existing service.

The failure is already isolated to one file: a parser crashes when an optional header is missing.
This is not a production incident right now, and there is no architecture redesign expected.

I want the smallest safe path that still keeps testing discipline.
