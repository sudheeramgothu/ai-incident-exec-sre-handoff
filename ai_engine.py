
from datetime import datetime

def generate_exec_brief(parsed: dict) -> str:
    ts = parsed.get("time_utc", datetime.utcnow().isoformat() + "Z")
    rack = parsed.get("rack", "unknown")
    dc = parsed.get("datacenter", "unknown DC")
    cluster = parsed.get("cluster", "an application cluster")
    impact = parsed.get("impact", "partial degradation")
    progress = parsed.get("vm_recovery_progress", "recovery in progress")
    return (
        f"At {ts}, the {dc} facility experienced instability on rack {rack}, "
        f"resulting in {impact} on {cluster}. Power/cooling were stabilized and "
        f"{progress}. A follow-up update will be provided after full service validation."
    )

def generate_tech_handoff(parsed: dict) -> str:
    lines = []
    rack = parsed.get("rack", "R?")
    dc = parsed.get("datacenter", "dc-?")
    temp = parsed.get("cooling_temp_c", "?")
    hv = parsed.get("hypervisor", "hv-?")
    progress = parsed.get("vm_recovery_progress", "?/?? VMs online")
    cluster = parsed.get("cluster", "app-cluster")
    impact = parsed.get("impact", "degraded")
    sev = parsed.get("severity", "major")
    lines.append(f"- Rack {rack} in {dc} reported power dip / cooling spike (max {temp}°C)")
    lines.append(f"- Hypervisor {hv}: VM recovery {progress}")
    lines.append(f"- {cluster} impact: {impact}")
    lines.append(f"- Next 30m focus: continue VM bring-up on {hv}, validate service SLOs")
    lines.append(f"- Escalation severity: {sev}")
    return "\n".join(lines)
