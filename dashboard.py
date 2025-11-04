import streamlit as st
import json
from pathlib import Path
import timeline

st.set_page_config(page_title="AI-Assisted Incident Briefing", layout="wide")

# Compatibility shim for rerun across Streamlit versions
if hasattr(st, "rerun"):
    _rerun = st.rerun
else:
    _rerun = st.experimental_rerun

st.title("AI-Assisted Incident Briefing Dashboard")
st.caption("AI drafts. Humans decide. — Governance-first demo")

incidents = timeline.load_all()  # returns [] if none

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Incidents")
    if not incidents:
        st.info("No incidents yet. Run `python run_demo.py` in a terminal.")
    else:
        for inc in incidents:
            # Use a plain container for broad Streamlit compatibility
            with st.container():
                st.markdown(f"**Incident ID:** `{inc['incident_id']}`")
                st.write(f"**Status:** {inc['status']}")
                st.write(f"**Severity:** {inc['severity']}")
                st.write(f"**Location:** {inc['datacenter']} / {inc['rack']}")
                st.write(f"**Cluster:** {inc['cluster']}")
                st.write(f"**Hypervisor:** {inc['hypervisor']}")
                st.write(f"**VM Recovery:** {inc['vm_recovery_progress']}")
                st.write(f"**Max Temp:** {inc['cooling_temp_c']} °C")

                c1, c2 = st.columns(2)
                with c1:
                    if inc['status'] != "APPROVED_FOR_EXEC_CHANNEL":
                        if st.button("Approve", key=f"approve-{inc['incident_id']}"):
                            timeline.set_status(inc['incident_id'], "APPROVED_FOR_EXEC_CHANNEL")
                            _rerun()
                    else:
                        st.success("Approved for Exec Channel")

                with c2:
                    if st.button("Reset to Awaiting Approval", key=f"reset-{inc['incident_id']}"):
                        timeline.set_status(inc['incident_id'], "AWAITING_INCIDENT_COMMANDER_APPROVAL")
                        _rerun()

with col2:
    st.subheader("Drafts & Details")
    if incidents:
        selected = st.selectbox("Select Incident", [i['incident_id'] for i in incidents])
        inc = next(i for i in incidents if i['incident_id'] == selected)
        st.markdown("**Executive Brief (Draft):**")
        st.write(inc.get("exec_brief", ""))
        st.markdown("**SRE Handoff (Draft):**")
        st.code(inc.get("tech_notes", ""), language="markdown")
        st.divider()
        st.markdown("**Raw JSON:**")
        st.code(json.dumps(inc, indent=2), language="json")

st.markdown("---")
st.caption("Tip: Run `python run_demo.py` to add a new incident. Open multiple terminals to simulate parallel incidents.")
