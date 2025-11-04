
import os, json
from typing import Optional
import requests

def _load_webhook_from_config() -> Optional[str]:
    try:
        import json, pathlib
        cfg_path = pathlib.Path(__file__).parent / "config.json"
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text())
            return cfg.get("slack_webhook")
    except Exception:
        pass
    return None

def post_message(message: str) -> None:
    webhook = os.getenv("SLACK_WEBHOOK") or _load_webhook_from_config()
    if not webhook:
        print("\n[notifier] (console)\n" + message + "\n")
        return
    try:
        resp = requests.post(webhook, json={"text": message}, timeout=5)
        if resp.status_code >= 300:
            print(f"[notifier] Slack POST failed: {resp.status_code} — {resp.text}")
        else:
            print("[notifier] Posted to Slack.")
    except Exception as e:
        print(f"[notifier] Slack POST exception: {e}\nFalling back to console:\n{message}")
