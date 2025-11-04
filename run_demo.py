
import json
import collector, timeline
from ai_engine import generate_exec_brief, generate_tech_handoff
from notifier import post_message

def run_demo():
    parsed = collector.normalize_alert({
        "event": "Power fluctuation and cooling spike",
        "severity": "critical",
        "rack": "R12",
        "datacenter": "us-east-dc1",
        "cooling_temp_c": 89,
        "cluster": "east-app-cluster",
        "vm_recovery_progress": "5/12 VMs online",
        "hypervisor": "hv-east-03",
        "customer_impact": "partial service degradation"
    })
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
        "status": "AWAITING_INCIDENT_COMMANDER_APPROVAL",
        "exec_brief": "",
        "tech_notes": ""
    }
    timeline.upsert(incident)
    print("\n[orchestrator] Collector stored base incident:")
    print(json.dumps(incident, indent=2))

    parsed_for_ai = {
        "time_utc": parsed["time_utc"],
        "rack": parsed["rack"],
        "datacenter": parsed["datacenter"],
        "cluster": parsed["details"]["cluster"],
        "impact": parsed["customer_impact"],
        "vm_recovery_progress": parsed["details"]["vm_recovery_progress"],
        "cooling_temp_c": parsed["details"]["cooling_temp_c"],
        "hypervisor": parsed["details"]["hypervisor"],
        "severity": parsed["severity"]
    }
    exec_brief = generate_exec_brief(parsed_for_ai)
    tech_notes = generate_tech_handoff(parsed_for_ai)

    incident["exec_brief"] = exec_brief
    incident["tech_notes"] = tech_notes
    timeline.upsert(incident)
    print("\n[ai-engine] Added Exec Brief + SRE Notes to incident.")

    message = (
        f"*Incident Draft* — {incident['datacenter']} {incident['rack']}\n"
        f"Status: {incident['status']}\n\n"
        f"*Executive Brief:*\n{exec_brief}\n\n"
        f"*SRE Handoff:*\n{tech_notes}"
    )
    post_message(message)

    print("\n[orchestrator] Demo complete. Open the dashboard via:")
    print("  streamlit run dashboard.py")

if __name__ == "__main__":
    run_demo()
