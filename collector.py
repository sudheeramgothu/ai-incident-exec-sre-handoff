
import argparse, uuid, datetime, json
from typing import Dict, Any
import timeline

def normalize_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "incident_id": str(uuid.uuid4()),
        "time_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "rack": alert.get("rack", "R12"),
        "datacenter": alert.get("datacenter", "us-east-dc1"),
        "event": alert.get("event", "Power fluctuation and cooling spike"),
        "details": {
            "cooling_temp_c": alert.get("cooling_temp_c", 89),
            "cluster": alert.get("cluster", "east-app-cluster"),
            "vm_recovery_progress": alert.get("vm_recovery_progress", "5/12 VMs online"),
            "hypervisor": alert.get("hypervisor", "hv-east-03"),
        },
        "severity": alert.get("severity", "critical"),
        "customer_impact": alert.get("customer_impact", "partial service degradation"),
        "status": "AWAITING_INCIDENT_COMMANDER_APPROVAL"
    }

def main():
    parser = argparse.ArgumentParser(description="Simulate alert ingestion")
    parser.add_argument("--event", default="Power fluctuation and cooling spike")
    parser.add_argument("--severity", default="critical")
    parser.add_argument("--rack", default="R12")
    parser.add_argument("--datacenter", default="us-east-dc1")
    parser.add_argument("--cooling_temp_c", type=int, default=89)
    parser.add_argument("--cluster", default="east-app-cluster")
    parser.add_argument("--vm_recovery_progress", default="5/12 VMs online")
    parser.add_argument("--hypervisor", default="hv-east-03")
    parser.add_argument("--customer_impact", default="partial service degradation")
    args = parser.parse_args()

    alert = vars(args)
    parsed = normalize_alert(alert)
    print("[collector] Parsed incident data:\n", json.dumps({
        "incident_id": parsed["incident_id"],
        "summary": f"Rack {parsed['rack']} in {parsed['datacenter']} saw: {parsed['event']}",
        "impact": parsed["customer_impact"],
        "cluster": parsed["details"]["cluster"],
        "severity": parsed["severity"],
        "hypervisor": parsed["details"]["hypervisor"],
        "vm_recovery_progress": parsed["details"]["vm_recovery_progress"],
        "cooling_temp_c": parsed["details"]["cooling_temp_c"],
        "time_utc": parsed["time_utc"]
    }, indent=2))

    # persist initial record
    incident = {
        "incident_id": parsed["incident_id"],
        "time_utc": parsed["time_utc"],
        "rack": parsed["rack"],
        "datacenter": parsed["datacenter"],
        "cluster": parsed["details"]["cluster"],
        "hypervisor": parsed["details"]["hypervisor"],
        "vm_recovery_progress": parsed["details"]["vm_recovery_progress"],
        "cooling_temp_c": parsed["details"]["cooling_temp_c"],
        "impact": parsed["customer_impact"],
        "severity": parsed["severity"],
        "status": parsed["status"],
        "exec_brief": "",
        "tech_notes": ""
    }
    timeline.upsert(incident)
    print("[collector] Incident stored with status AWAITING_INCIDENT_COMMANDER_APPROVAL.")

if __name__ == "__main__":
    main()
