# Responsible AI policy

This lab is an educational prototype for invented departments and data. Do not enter personal, customer, confidential, regulated, credential, or production data. The deterministic input checks block email/phone-like strings and markers such as CONFIDENTIAL, SECRET, or INTERNAL ONLY. These pattern checks can miss sensitive data and can flag harmless text; they are not a security boundary.

Outputs are checked for a small set of unsafe patterns and may be withheld. A send, publish, delete, refund, transfer, approve, or purchase request pauses for a named human decision. Approval records review only; the platform has no external action tools. Runs store a SHA-256 input digest instead of raw input; output and flags, feedback comments, approval reviewer, and audit events are stored in SQLite. Treat the demo database as sensitive and disposable.

Humans remain accountable for checking accuracy, fairness, accessibility, privacy, and policy before relying on any result. This demo does not provide legal, compliance, or security assurance.
