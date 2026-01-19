## Development - URL Shortener
This project is designed to be run via Docker Compose.

Environment variables are documented in `.env.example`.

Core functionality:
- `/api/links/` — token-protected link creation
- `/<code>` — redirect with analytics
- `/admin/` — internal management UI
