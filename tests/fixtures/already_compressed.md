# API Quick Reference

## Authentication
**Required**: Bearer token in `Authorization` header
**Obtain**: Developer portal → Create app → Copy key

## Endpoints
### Data Operations
- `GET /api/resource` - Retrieve list
- `POST /api/resource` - Create new  
- `DELETE /api/resource/:id` - Remove

### Headers
```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

## Rate Limits
- 1000 req/hour (authenticated)
- 100 req/hour (anonymous)