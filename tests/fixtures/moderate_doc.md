# API Authentication Guide

## Overview

This endpoint handles user authentication for the API. When a user wants to access protected resources, they must first authenticate using their credentials.

## POST /auth

Authenticates user credentials and returns access token.

**Request Details**:
- Endpoint: `/auth`
- Method: POST
- Body: `{username: string, password: string}`

**Response Format**:
- Success (200): `{token: string}`
- Failure (401): `{error: string}`

The authentication process validates the provided credentials against the user database. If successful, the system generates a JWT token that can be used for subsequent API requests.

**Example Usage**:
```json
POST /auth
{
  "username": "john",
  "password": "secret123"
}
```

The returned token should be included in the Authorization header for authenticated requests. Tokens expire after 24 hours and must be refreshed.