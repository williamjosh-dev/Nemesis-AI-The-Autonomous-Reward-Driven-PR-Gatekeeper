from fastapi import APIRouter, Header, HTTPException, Request, status
import hmac
import hashlib
from config.settings import settings

router = APIRouter()

def verify_github_signature(request_body: bytes, signature_header: str | None) -> bool:
    """Verifies the HMAC hex digest signature from GitHub webhooks."""
    if not settings.GITHUB_WEBHOOK_SECRET:
        return True  # Bypass if secret is not set during local testing (e.g., using ngrok)
    
    if not signature_header:
        return False
    
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False
    
    mac = hmac.new(settings.GITHUB_WEBHOOK_SECRET.encode(), msg=request_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@router.post("/webhook")
async def github_webhook(request: Request, x_github_event: str = Header(None), x_hub_signature_256: str = Header(None)):
    body_bytes = await request.body()
    
    # Verify signature
    if not verify_github_signature(body_bytes, x_hub_signature_256):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")
    
    payload = await request.json()
    
    # We only care about pull requests for now (opened or synchronize/updated)
    if x_github_event == "pull_request":
        action = payload.get("action")
        pr_number = payload.get("pull_request", {}).get("number")
        repo_name = payload.get("repository", {}).get("full_name")
        diff_url = payload.get("pull_request", {}).get("diff_url")
        
        if action in ["opened", "synchronize"]:
            print(f"-> Caught PR #{pr_number} on {repo_name} (Action: {action})")
            print(f"-> Diff URL: {diff_url}")
            
            # TODO: Pass this to your Jury engine layer next!
            
            return {"status": "success", "message": f"Processed PR #{pr_number} event."}
            
    return {"status": "ignored", "event": x_github_event}