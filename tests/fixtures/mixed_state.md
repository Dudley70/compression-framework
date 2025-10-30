# API Documentation

## Authentication (COMPRESSED)
- Endpoint: `/auth`
- Method: POST
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Token expires in 24h
- Refresh with `/refresh` endpoint

## New Feature - Rate Limiting (VERBOSE)

We've recently added rate limiting to the API to ensure fair usage across
all clients. Rate limiting helps prevent abuse and ensures that the API
remains responsive for everyone who uses it.

The rate limiting system works by tracking the number of requests made by
each authenticated user within a specific time window. If you exceed the
limit, you'll receive a 429 status code and will need to wait before making
additional requests.

Here's how to work with rate limits: first, check the response headers for
rate limit information. The `X-RateLimit-Limit` header shows your total
limit, `X-RateLimit-Remaining` shows how many requests you have left, and
`X-RateLimit-Reset` shows when the limit will reset.

When you hit the rate limit, we recommend implementing exponential backoff
in your client code. This means waiting longer between retry attempts to
avoid overwhelming the server.

## User Management (COMPRESSED)
- GET `/users` - List users (admin)
- POST `/users` - Create user
- PUT `/users/:id` - Update user
- DELETE `/users/:id` - Remove user
- Roles: admin, user, readonly