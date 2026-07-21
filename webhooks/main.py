import hashlib
import hmac
import time

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

SECRET = "YOUR_WEBHOOK_SECRET"  # Replace with your actual webhook secret

app = FastAPI()


def check_signature(payload: bytes, t: int, signature: str, secret: str):
    """
    Recompute the signature of the payload using the secret and the timestamp. Compare the
    recomputed signature with the signature provided in the header.
    """
    mac = hmac.new(secret, digestmod=hashlib.sha256)
    mac.update(str(t).encode())
    mac.update(b".")
    mac.update(payload)
    recomputed_signature = mac.hexdigest()
    return recomputed_signature == signature


@app.post("/webhookhandler")
async def webhook_handler(request: Request):
    """
    Handle incoming webhook requests.
    """

    # Gets the signature from the request header.
    signature = request.headers.get("nextmv-signature")

    # Extract timestamp and signature from header. Check the timestamp and
    # extract the signature string.
    signature_time, signature_string = 0, ""
    try:
        t, sig = signature.split(",")
        now = time.time()
        signature_time = int(t.split("=")[1])
        signature_string = sig.split("=")[1]

        # Check if the timestamp is not older than 5 minutes and not in the
        # future. This means to avoid replay attacks.
        if not (now - 300 < signature_time < now + 60):
            print(f"Invalid Time Value: {now - 300} < {signature_time} < {now + 60}")
            return Response(
                status_code=401,
                headers={"content-type": "text/plain"},
                content=bytes("Unauthorized: Invalid Time Value", "utf-8"),
            )
    except Exception:
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
