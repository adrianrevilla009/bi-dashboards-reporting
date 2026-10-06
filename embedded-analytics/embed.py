"""Embedded analytics core: the host app signs a short-lived token carrying the tenant,
and the analytics endpoint derives its row filter from the verified token, never from the request."""
import base64, hashlib, hmac, json, sqlite3, time

SECRET = b"lab-only-embed-secret"  # lab value; in real use it comes from a secret store


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def sign_token(tenant: str, ttl: int = 300, now: float | None = None) -> str:
    body = _b64(json.dumps({"tenant": tenant, "exp": int((now or time.time()) + ttl)}).encode())
    return f"{body}.{_b64(hmac.new(SECRET, body.encode(), hashlib.sha256).digest())}"


def verify_token(token: str, now: float | None = None) -> str:
    body, _, sig = token.partition(".")
    good = _b64(hmac.new(SECRET, body.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, good):
        raise PermissionError("bad signature")
    claims = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    if claims["exp"] < (now or time.time()):
        raise PermissionError("token expired")
    return claims["tenant"]


def revenue_by_customer(db: sqlite3.Connection, token: str) -> list[tuple]:
    """The dashboard query; the tenant predicate is always applied server-side."""
    tenant = verify_token(token)
    return db.execute(
        "SELECT c.name, SUM(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id "
        "WHERE o.status = 'PAID' AND c.tenant = ? GROUP BY c.name ORDER BY c.name", (tenant,)
    ).fetchall()
