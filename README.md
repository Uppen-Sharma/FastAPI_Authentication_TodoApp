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

The `.env` files are not committed. Copy the examples and fill them in:

```
cp server/.env.example server/.env
cp client/.env.example client/.env
```

Fill in `ACCESS_TOKEN_SECRET_KEY` and `REFRESH_TOKEN_SECRET_KEY` in `server/.env` with two different long random values, for example `python -c "import secrets; print(secrets.token_hex(32))"`.

## Demo users

| Username | Password | Role |
|---|---|---|
| alice | alice123 | admin |
| bob | bob123 | client |
