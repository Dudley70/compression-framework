## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Auth: None required

## GET /users
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`

## PUT /users/:id
- Auth: Bearer + admin role
- Body: User update object
- Returns: Updated user (200) | 403/404