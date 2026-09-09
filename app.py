import os

import requests
from flask import Flask, request, redirect, abort

app = Flask(__name__)

SNIPEIT_API_URL = os.environ["SNIPEIT_API_URL"].rstrip("/")
SNIPEIT_PUBLIC_URL = os.getenv(
    "SNIPEIT_PUBLIC_URL",
    SNIPEIT_API_URL
).rstrip("/")

SNIPEIT_TOKEN = os.environ["SNIPEIT_TOKEN"]

VERIFY_TLS = os.getenv("VERIFY_TLS", "true").lower() in (
    "1", "true", "yes", "on"
)

session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {SNIPEIT_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "LibreDesk-SnipeIT-Resolver/1.0",
})


@app.get("/")
def lookup():
    email = (request.args.get("email") or "").strip().lower()

    # Basic sanity check
    if not email or "@" not in email or len(email) > 254:
        abort(400, description="Missing or invalid email address")

    try:
        response = session.get(
            f"{SNIPEIT_API_URL}/api/v1/users",
            params={
                "email": email,
                "limit": 2,
            },
            timeout=10,
            verify=VERIFY_TLS,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        app.logger.error("Snipe-IT request failed: %s", exc)
        abort(502, description="Could not contact Snipe-IT")

    users = data.get("rows", [])
    users = [
        user for user in users
        if str(user.get("email", "")).strip().lower() == email
    ]

    if len(users) == 0:
        abort(404, description=f"No Snipe-IT user found for {email}")

    if len(users) > 1:
        abort(409, description=f"Multiple Snipe-IT users found for {email}")

    user_id = users[0].get("id")

    if not user_id:
        abort(502, description="Snipe-IT response contained no user ID")
      
    target = f"{SNIPEIT_PUBLIC_URL}/users/{int(user_id)}#assets"

    return redirect(target, code=302)


@app.get("/healthz")
def health():
    return {"status": "ok"}
