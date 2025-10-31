# Security Requirements

All API endpoints must validate authentication tokens before processing requests. Rate limiting is required to prevent abuse. Input validation must sanitize all user-provided data. HTTPS is mandatory for all communications. Password storage must use bcrypt with minimum 10 salt rounds.