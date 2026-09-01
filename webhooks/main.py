import hashlib
import hmac
import time

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

SECRET = "YOUR_WEBHOOK_SECRET"  # Replace with your actual webhook secret

app = FastAPI()


# --8<-- [start:check-signature]
def check_signature(
    payload: bytes,
    t: int,
    signature: str,
    secret: bytes,
    max_age_seconds: int = 300,
    max_skew_seconds: int = 60,
) -> bool:
    """
    Recompute the signature of the payload using the secret and the timestamp, and compare it
    with the signature provided in the header. Returns False if the timestamp falls outside the
    accepted window, so that a captured request cannot be replayed indefinitely.
    """

    # The signature stays valid for as long as the payload does, so the
    # timestamp is what bounds replay. Check it before anything else.
    now = time.time()
    if not (now - max_age_seconds < t < now + max_skew_seconds):
        return False

    mac = hmac.new(secret, digestmod=hashlib.sha256)
    mac.update(str(t).encode())
    mac.update(b".")
    mac.update(payload)
    recomputed_signature = mac.hexdigest()

    # Constant-time comparison. A plain `==` short-circuits on the first
    # differing character and leaks how many leading characters matched.
    return hmac.compare_digest(recomputed_signature, signature)


# --8<-- [end:check-signature]


@app.post("/webhookhandler")
async def webhook_handler(request: Request):
    """
    Handle incoming webhook requests.
    """

    # Gets the signature from the request header.
    signature = request.headers.get("nextmv-signature")
    if not signature:
        return Response(
            status_code=401,
            headers={"content-type": "text/plain"},
            content=bytes("Unauthorized: Missing Signature", "utf-8"),
        )

    # Extract the timestamp and the signature string from the header. The
    # timestamp itself is validated inside `check_signature`. Only the errors a
    # malformed header can actually cause are caught here: ValueError from the
    # two-part unpacking and from `int`, IndexError from a missing "=".
    try:
        t, sig = signature.split(",")
        signature_time = int(t.split("=")[1])
        signature_string = sig.split("=")[1]
    except (ValueError, IndexError):
        return Response(
            status_code=401,
            headers={"content-type": "text/plain"},
            content=bytes("Unauthorized: Invalid Signature Format", "utf-8"),
        )

    # Make sure secret is set.
    if not SECRET:
        return Response(
            status_code=500,
            headers={"content-type": "text/plain"},
            content=bytes("Internal Server Error", "utf-8"),
        )

    # Check signature.
    body = await request.body()
    if not check_signature(body, signature_time, signature_string, SECRET.encode()):
        return Response(
            status_code=401,
            headers={"content-type": "text/plain"},
            content=bytes("Unauthorized: Invalid signature", "utf-8"),
        )

    # Do something useful with the webhook payload here. For example, you can
    # parse the JSON payload and take action based on its contents.
    body_json = body.decode("utf-8")
    print(body_json)

    # Optionally give a response to the webhook sender, which is the Nextmv
    # Cloud API.
    return JSONResponse(
        status_code=200,
        content={
            "message": "Webhook received!",
            "body": body_json,
        },
    )
