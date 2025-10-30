# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Headers: `Content-Type: application/json`

## GET /users
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`
- Pagination: `?page=1&limit=50`

## PUT /users/:id
- Auth: Bearer + admin role
- Body: User update object
- Returns: Updated user (200) | 403/404
- Validation: Required fields enforced

## DELETE /users/:id
- Auth: Bearer + admin
- Returns: 204 | 403/404
- Cascade: Removes related data