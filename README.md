# tullingedk/member

Member management portal for Tullinge gymnasium datorklubb.

## Deployment Instructions

Copy the `.enx.example` to `.env` and modify the values where required.

Use `docker-compose` to run the application using `gunicorn` on port `5000`.

```bash
docker-compose -f prod.yml up -d
```

Use nginx or other proxy in front of gunicorn.

## Contributors ✨

Copyright (C) 2020 - 2021, Tullinge gymnasium datorklubb, <info@tgdk.se>

Initially written by [Vilhelm Prytz](https://github.com/vilhelmprytz).
