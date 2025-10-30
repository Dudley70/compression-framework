---
compression:
  last_full_compression: 2025-10-30 10:00 AEDT
  baseline_tokens: 200
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
---

# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Headers: `Content-Type: application/json`
- Token expires in 24h

## GET /users  
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`
- Pagination: `?page=1&limit=50`

## NEW SECTION - Webhooks

We've just added webhook functionality to our API, which allows you to receive
real-time notifications when certain events occur in your account. This is
particularly useful for keeping external systems in sync with changes that
happen in our platform.

Webhooks work by sending HTTP POST requests to URLs that you specify when
certain events are triggered. For example, you might want to be notified
when a new user is created, when a payment is processed, or when an order
status changes.

To set up webhooks, you'll need to create an endpoint in your application
that can receive and process these notifications. Your endpoint should
return a 2xx HTTP status code to acknowledge receipt of the webhook.

Here's what you need to know about webhook security: all webhook requests
include a signature header that you can use to verify that the request
actually came from our servers. This prevents malicious actors from sending
fake webhook notifications to your application.