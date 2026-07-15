# Context Notes

Security design identifies what must be protected, who might abuse the system, and which controls must exist at each boundary. It sits upstream of security audit: the goal here is to design the defenses, not just inspect the code later.

In Prodcraft, security design is most valuable when the system adds new trust boundaries, handles sensitive data, or depends on brownfield coexistence where old and new controls may differ.
