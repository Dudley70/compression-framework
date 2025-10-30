## POST /auth
- Body: `{username: string, password: string}`
- Returns: `{token: string}` (200) | `{error: string}` (401)
- Auth: None required
- Headers: `Content-Type: application/json`

## GET /users  
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`
- Pagination: `?page=1&limit=50`

## POST /users
- Auth: Admin role required
- Body: `{name: string, email: string, role: string}`
- Returns: Created user (201) | Error (400/403)

## PUT /users/{id}
- Auth: Self or admin
- Body: Partial user object
- Returns: Updated user (200) | Error (400/403/404)

## DELETE /users/{id}
- Auth: Admin only
- Returns: Success (204) | Error (403/404)
- Note: Soft delete, preserves audit trail

## Token Usage
- Header: `Authorization: Bearer {token}`
- Expiry: 24 hours
- Refresh: Re-authenticate when expired
- Rate limit: 100 requests/hour per token