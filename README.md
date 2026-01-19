# go.juliankim.dev

A personal URL shortener built with Django and PostgreSQL.

## Features
- Collision-safe short code generation
- Admin dashboard for link management
- Click tracking
- Soft-disable links (`is_active`)
- API-protected link creation
- Deployed with Fly.io + Cloudflare

## Tech Stack
- Django
- PostgreSQL
- Docker
- Fly.io
- Cloudflare DNS

## API
`POST /api/links/`

```json
{
  "url": "https://example.com"
}
