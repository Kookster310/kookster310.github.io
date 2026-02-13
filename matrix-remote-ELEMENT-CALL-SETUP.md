# Element Call (Matrix RTC) setup for matrix.310networks.com

The **MISSING_MATRIX_RTC_FOCUS** error means Element doesn’t know where your Matrix RTC (Element Call) backend is. You need:

1. **lk-jwt-service** – issues LiveKit JWTs to Matrix users
2. **Synapse** – enable MSCs for Element Call
3. **Well-known** – advertise the RTC focus at `https://matrix.310networks.com/.well-known/matrix/client`
4. **Reverse proxy** – one host that serves both JWT and LiveKit SFU (e.g. `matrixrtc.310networks.com`)

---

## 1. Add lk-jwt-service to Docker Compose

On the Pi, edit `matrix-remote/docker-compose.yaml` and add this service (and add `depends_on` for synapse if the JWT service should start after it). Use the same `LIVEKIT_KEY` / `LIVEKIT_SECRET` as in `livekit/livekit.yaml` (key name `matrix`, value the hex string).

**Add this service** (after `livekit`, before `element-call`):

```yaml
  lk-jwt-service:
    image: ghcr.io/element-hq/lk-jwt-service:latest
    container_name: matrix-lk-jwt
    restart: unless-stopped
    environment:
      - LIVEKIT_URL=wss://matrixrtc.310networks.com/livekit/sfu
      - LIVEKIT_KEY=matrix
      - LIVEKIT_SECRET=b4bbc5cb502c5c64726ea0ceed960f87ac97b8c60c165344fc9cc4807c067d6c
      - LIVEKIT_FULL_ACCESS_HOMESERVERS=matrix.310networks.com
    ports:
      - "8070:8080"
    networks:
      - matrix
    depends_on:
      - livekit
```

Create a subdomain **matrixrtc.310networks.com** pointing to the Pi (or to the machine that runs the reverse proxy). The reverse proxy for that host must route:

- **`/livekit/jwt/`** → `http://localhost:8070/` (or the Pi’s IP if proxy is elsewhere), so that:
  - `https://matrixrtc.310networks.com/livekit/jwt/sfu/get`
  - `https://matrixrtc.310networks.com/livekit/jwt/get_token`
  - `https://matrixrtc.310networks.com/livekit/jwt/healthz`
  work.
- **`/livekit/sfu`** (WebSocket) → `http://localhost:7880/` (LiveKit), so that:
  - `wss://matrixrtc.310networks.com/livekit/sfu` connects to LiveKit.

Example **Caddy** (on the Pi, same host as Docker):

```caddy
matrixrtc.310networks.com {
    handle /livekit/jwt/* {
        reverse_proxy 127.0.0.1:8070
    }
    handle /livekit/sfu* {
        reverse_proxy 127.0.0.1:7880
    }
}
```

Example **Nginx**:

```nginx
server {
    listen 443 ssl;
    server_name matrixrtc.310networks.com;
    # ssl_* and other directives as needed

    location /livekit/jwt/ {
        proxy_pass http://127.0.0.1:8070/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /livekit/sfu {
        proxy_pass http://127.0.0.1:7880;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 2. Synapse: enable Element Call MSCs

On the Pi, edit `synapse/data/homeserver.yaml` and add this block (e.g. after `turn_allow_guests`):

```yaml
# Element Call (Matrix RTC) – required for MISSING_MATRIX_RTC_FOCUS
experimental_features:
  msc3266_enabled: true   # Room summary API
  msc4222_enabled: true   # Sync v2 state_after
  msc4140_enabled: true   # Delayed events for call signalling
  max_event_delay_duration: 24h
  msc_message:
    per_second: 0.5
    burst_count: 30
  src_delayed_event_mgmt:
    per_second: 1
    burst_count: 20
```

Then restart Synapse:

```bash
cd /path/on/pi/matrix-remote
docker compose restart synapse
```

---

## 3. Well-known (RTC focus discovery)

Element discovers the RTC focus from **`https://matrix.310networks.com/.well-known/matrix/client`**. That URL must be served by the same host that serves your Matrix client API (often the same reverse proxy as Synapse).

**Content** of `/.well-known/matrix/client` must include your existing `m.homeserver` and **`org.matrix.msc4143.rtc_foci`**:

```json
{
  "m.homeserver": {
    "base_url": "https://matrix.310networks.com"
  },
  "org.matrix.msc4143.rtc_foci": [
    {
      "type": "livekit",
      "livekit_service_url": "https://matrixrtc.310networks.com/livekit/jwt"
    }
  ]
}
```

- Serve it as **`Content-Type: application/json`**.
- Allow CORS if needed, e.g. `Access-Control-Allow-Origin: *` (or your Element origin).

Where to put it depends on your proxy:

- **Caddy**: you can put a file under the site root and serve it, or use `respond` for that path.
- **Nginx**: `alias` or `try_files` to a JSON file.
- **Synapse**: Synapse does **not** serve `/.well-known/matrix/client` itself; the proxy in front of `matrix.310networks.com` must serve it.

After you add/update this and restart Synapse, reload Element (or wait for cache) and try a call again.

---

## 4. Optional: LiveKit room creation

If you use `LIVEKIT_FULL_ACCESS_HOMESERVERS`, the JWT service will create LiveKit rooms for your users. You can disable automatic room creation in LiveKit so only the JWT service creates rooms:

In `livekit/livekit.yaml` set:

```yaml
room:
  auto_create: false
  empty_timeout: 300
  max_participants: 20
```

Then restart LiveKit: `docker compose restart livekit`.

---

## Checklist

- [ ] `lk-jwt-service` in `docker-compose.yaml`, env vars correct (especially `LIVEKIT_URL`, `LIVEKIT_KEY`, `LIVEKIT_SECRET`, `LIVEKIT_FULL_ACCESS_HOMESERVERS`)
- [ ] DNS: `matrixrtc.310networks.com` → Pi (or proxy host)
- [ ] Reverse proxy for `matrixrtc.310networks.com`: `/livekit/jwt/` → 8070, `/livekit/sfu` → 7880
- [ ] Synapse: `experimental_features` (MSCs) added and Synapse restarted
- [ ] `https://matrix.310networks.com/.well-known/matrix/client` returns the JSON above (with `org.matrix.msc4143.rtc_foci`)
- [ ] `docker compose up -d` (or at least start `lk-jwt-service` and `livekit`)

Then try a 1:1 or room call again in Element.
