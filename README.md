# tullingedk/member

Member management portal for Tullinge gymnasium datorklubb.

## Environment Variables

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_HOSTED_DOMAIN`
- `OAUTHLIB_INSECURE_TRANSPORT` - Set to `1` if running application behind proxy such as Nginx.
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_DATABASE`

## Deployment

Fill in `.env` file or set required environment variables in other suitable way.

Use `docker-compose` to run the application using `gunicorn` on port `5000`.

```bash
docker-compose -f prod.yml up -d
```

Use nginx or other proxy in front of gunicorn.
