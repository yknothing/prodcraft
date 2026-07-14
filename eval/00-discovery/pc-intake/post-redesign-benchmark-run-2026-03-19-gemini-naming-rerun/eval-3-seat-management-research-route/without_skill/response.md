To determine whether the real friction in the seat management flow stems from permissions, procurement, or guest users, we need to validate these hypotheses without relying on assumptions.

**Assumptions Made:** 
- "Seat management" refers to assigning, purchasing, or modifying user licenses within a B2B SaaS platform.
- You have basic product analytics, access to support tickets, and the ability to reach out to admin users.

Here is a structured approach to uncover the root cause:

### 1. Quantitative Data Analysis (Product Analytics)
Look at how admins actually behave in the platform to find the friction points:
*   **Procurement:** Look for abandoned checkout flows. Do admins click "Add Seat," see a billing prompt, and then cancel? This indicates procurement friction (e.g., needing finance approval to spend more).
*   **Guest Users:** Look at user churn and reassignment. Are admins frequently rotating a single seat among multiple external email domains (e.g., `@client.com`)? This is a classic workaround when a platform lacks a dedicated, cheaper "Guest" role.
*   **Permissions:** Track role changes. Do admins frequently upgrade/downgrade user roles or visit the permissions page immediately after adding a user, only to get stuck?

### 2. Qualitative Analysis (Support Tickets & Sales Calls)
Categorize your existing feedback over the last 90 days. Search your support desk for keywords related to the three areas:
*   **Permissions:** Search *"custom role," "access denied," "view-only," "admin rights."*
*   **Procurement:** Search *"invoice," "prorate," "credit card," "annual contract," "finance."*
*   **Guest Users:** Search *"client access," "contractor," "external," "freelancer," "share without paying."*

Whichever category has the highest volume and highest negative sentiment is likely your primary culprit.

### 3. Targeted User Research (Contextual Inquiry)
Don't just ask admins what they hate—watch them work. Conduct 5-7 interviews with admins who have recently added or removed users.
*   **Prompt:** *"Walk me through the last time you had to add a new person to the team."*
*   **Watch for:** Do they complain about the cost (Procurement)? Do they struggle to figure out what the user can see (Permissions)? Or do they complain that the person only needs to see one specific project (Guest Users)?

### Next Steps Recommendation
Start with the **Support Ticket Analysis**. It is the fastest way to get the "voice of the customer" without scheduling interviews or waiting for data queries. If you find overwhelming complaints about paying $X just so a client can view a document, your root cause is **Guest Users**. If the complaints are about navigating corporate credit cards, it's **Procurement**.
