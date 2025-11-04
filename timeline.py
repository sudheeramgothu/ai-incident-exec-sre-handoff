
import json
from pathlib import Path
from typing import Dict, Any, List

STORE_PATH = Path(__file__).parent / "incident_store.json"

def _init_store() -> None:
    if not STORE_PATH.exists():
        STORE_PATH.write_text("[]")

def load_all() -> List[Dict[str, Any]]:
    _init_store()
    return json.loads(STORE_PATH.read_text())

def save_all(items: List[Dict[str, Any]]) -> None:
    STORE_PATH.write_text(json.dumps(items, indent=2))

def upsert(incident: Dict[str, Any]) -> None:
    items = load_all()
    found = False
    for i, it in enumerate(items):
        if it.get("incident_id") == incident.get("incident_id"):
            items[i] = incident
            found = True
            break
    if not found:
        items.append(incident)
    save_all(items)

def get(incident_id: str):
    for it in load_all():
        if it.get("incident_id") == incident_id:
            return it
    return None

def set_status(incident_id: str, new_status: str):
    items = load_all()
    for i, it in enumerate(items):
        if it.get("incident_id") == incident_id:
            it["status"] = new_status
            items[i] = it
            save_all(items)
            return it
    return None
