# FastAPI_Authentication_TodoApp

A todo app that shows login with an access token and a refresh token, built with FastAPI, React and json-server.

- Access token (short-lived) is sent with every request, and the refresh token (httpOnly cookie) quietly renews it.
- Sign up, logout that ends the session, a maximum session length and rate limiting on login and register.
- Protected routes, with separate `/client` and `/admin` API routes for the two roles.

## Run it

Three terminals, start the database first.

```
cd db
npm install
cp db.seed.json db.json
npm start
```

```
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 3000
```

```
cd client
npm install
npm run dev
```

Open http://localhost:5173

## Settings

Create `server/.env` and `client/.env` (they are not committed).

`server/.env`: `JWT_ALGORITHM`, `ACCESS_TOKEN_SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_SECRET_KEY`, `REFRESH_TOKEN_EXPIRE_DAYS`, `SESSION_MAX_DAYS`, `CORS_ORIGINS`, `DB_URL`, `COOKIE_SECURE`, `AUTH_RATE_LIMIT`, `REFRESH_GRACE_SECONDS`

`client/.env`: `VITE_API_URL`, `VITE_CLIENT_PORT`

Use long random values for the two secret keys, for example `python -c "import secrets; print(secrets.token_hex(32))"`.

## Demo users

| Username | Password | Role |
|---|---|---|
| alice | alice123 | admin |
| bob | bob123 | client |
