# Invite Modal UI Summary

The product adds a user-facing invite modal for team administrators.

Surface and states:

- trigger button: `Invite teammate`
- modal title: `Invite teammate`
- email input with inline validation
- role select with options `Admin` and `Member`
- helper text explaining who can be invited
- primary action button: `Send invite`
- secondary action button: `Cancel`
- close icon button in the modal header
- loading state while invite creation is in flight
- success state after invite is sent
- error state when invite creation fails

Expected interaction notes:

- the modal opens from the team-members page
- submit is disabled until the form is valid
- the email field can show validation errors for malformed addresses
- a general error banner appears when the backend rejects the request
- the modal closes on success and focus should return to the trigger button
