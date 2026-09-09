## How it works

LibreDesks Context Link opens a URL like:

```text
https://snipe-lookup.example.com/?email={{email}}
```

LibreDesk replaces `{{email}}` with the current user's email address.

The lookup service then:

1. Searches Snipe-IT for the exact email address.
2. Gets the matching Snipe-IT user ID.
3. Redirects the browser to that users asset endpoint

## Setup and Run

Adjust the .env file for your environment by adding your api token and snipe-it URL and API URL. 

api/v1/ is automatically appended to the URL.

```bash
docker compose up -d --build
```

## Configure LibreDesk

Create a LibreDesk Context Link.


```text
https://<YOUR_CONTAINER_IP:PORT>/?email={{email}}
```

When an agent clicks the link, LibreDesk inserts the contact's email address automatically.
