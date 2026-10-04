"""
The AI Apprentice: Interactive Web Application
7th Global AI Hackathon · ElevenLabs × Hack-Nation
Modules 1 (Capture), 2 (Map), and 3 (Teach)
"""

import streamlit as st
import pandas as pd
import json
import time
import os
import sys

# Ensure core imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.screen_vision import ScreenVisionExtractor
from core.elevenlabs_voice import ElevenLabsVoiceCompanion
from core.work_map_generator import WorkMapGenerator
from core.voice_tutor import VoiceTutorCoach
from core.privacy_filter import PrivacyFilter

# Page Setup
st.set_page_config(
    page_title="The AI Apprentice | ElevenLabs × Hack-Nation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .hero-header {
        background: linear-gradient(135deg, #065f46 0%, #047857 50%, #064e3b 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
    }
    .badge-sub {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(52, 211, 153, 0.3);
        display: inline-block;
        margin-right: 8px;
    }
    .step-card {
        background: #1e293b;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 16px;
    }
    .guardrail-card {
        background: #311042;
        padding: 14px;
        border-radius: 10px;
        border-left: 4px solid #a855f7;
        margin-top: 8px;
    }
    .intercept-card {
        background: #450a0a;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #ef4444;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "sample_data" not in st.session_state:
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "stuttgart_invoicing.json")
    if os.path.exists(sample_path):
        with open(sample_path, "r") as f:
            st.session_state.sample_data = json.load(f)
    else:
        st.session_state.sample_data = {}

if "work_map" not in st.session_state:
    wm_gen = WorkMapGenerator()
    st.session_state.work_map = wm_gen.generate_work_map([], [])

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/isometric-line/100/robot-2.png", width=64)
st.sidebar.title("The AI Apprentice")
st.sidebar.caption("ElevenLabs × Hack-Nation · 7th Global AI Hackathon")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Agent Settings")
voice_expressive = st.sidebar.selectbox("ElevenLabs Voice Model", ["ElevenAgents Expressive Mode (Curious & Patient)", "Scribe v2 Realtime Voice"])
pause_sensitivity = st.sidebar.slider("Natural Pause Sensitivity (sec)", 1.0, 3.0, 1.8)
pii_redaction = st.sidebar.toggle("Presidio PII Redaction Active", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Scenario**: Sabine (57, retiring in 18 months) teaching Lena (26, Day 4) at Stuttgart Machine Builder GmbH.")

# Hero Banner
st.markdown("""
<div class="hero-header">
    <div>
        <span class="badge-sub">ElevenLabs × Hack-Nation</span>
        <span class="badge-sub">7th Global AI Hackathon</span>
        <span class="badge-sub">Challenge 01</span>
    </div>
    <h1 style="margin-top: 12px; margin-bottom: 4px; color: #ffffff;">🤖 The AI Apprentice</h1>
    <p style="font-size: 1.1rem; color: #d1fae5; max-width: 900px;">
        Capture what experienced experts know while they work, map their unwritten judgment calls & guardrails 
        into a clickable Work Map, and coach the next generation with a real-time ElevenLabs Voice Tutor.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ Module 1: Capture (Screen + Voice Companion)",
    "🗺️ Module 2: Clickable Work Map",
    "🎓 Module 3: Teach (Voice Tutor Interceptor)",
    "🚀 The Moonshot Pitch"
])

# -----------------------------------------------------------------------------
# MODULE 1: CAPTURE
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("🎙️ Module 1: Live Expert Capture Session")
    st.write("Watch **Sabine** process 60 open accounts payable invoices two days before month-end close. The ElevenLabs voice agent stays quiet while she types, and asks *why* at natural pauses.")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### 📺 Live Expert Screen Share & Vision Parser")
        selected_inv = st.selectbox(
            "Select Invoice Case on Sabine's Screen:",
            ["Invoice #4471 (€7,200.00 Equipment - Stuttgart CNC)", "Invoice #4489 (€3,400.00 December - TechCzech GmbH)", "Invoice #4502 (€12,500.00 Subsidiary - Bohemia Logistics)"]
        )

        # Display Simulated Screen Workspace
        if "4471" in selected_inv:
            st.info("💻 **Screen View 03:12** | ERP Invoice Entry | Supplier: Stuttgart CNC | Amount: **€7,200.00** | Default: 4711 (OpEx)")
            action_type = "recoded_cost_center"
            val_before = "4711 (OpEx)"
            val_after = "0400 (CapEx)"
            amount = 7200.0
            supplier = "Stuttgart CNC Components GmbH"
        elif "4489" in selected_inv:
            st.warning("💻 **Screen View 05:45** | ERP Payment Queue | Supplier: TechCzech GmbH | Amount: **€3,400.00** | Action: Apply Hold")
            action_type = "applied_payment_hold"
            val_before = "Approved for Payment"
            val_after = "HOLD (December Double-Billing Policy)"
            amount = 3400.0
            supplier = "TechCzech GmbH"
        else:
            st.success("💻 **Screen View 07:20** | ERP Approval Matrix | Supplier: Bohemia Logistics | Amount: **€12,500.00** | Action: Dual Approval")
            action_type = "routed_approval"
            val_before = "Single Sign-off"
            val_after = "Dual Sign-off (Czech Subsidiary)"
            amount = 12500.0
            supplier = "Bohemia Logistics s.r.o."

        # Simulate Pause Button
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            typing_state = st.toggle("Expert is Typing", value=False)
        with col_act2:
            trigger_pause = st.button("⏱️ Trigger Natural Pause & Voice Prompt", use_container_width=True)

    with col2:
        st.markdown("#### 🗣️ ElevenLabs Voice Companion & Transcript")
        voice_comp = ElevenLabsVoiceCompanion()
        
        event_data = {
            "timestamp": "03:12",
            "invoice_id": selected_inv.split(" ")[0],
            "supplier": supplier,
            "amount_eur": amount,
            "action_type": action_type,
            "field_changed": "cost_center",
            "value_before": val_before,
            "value_after": val_after,
            "event_summary": f"Changed cost center from {val_before} to {val_after}"
        }

        if trigger_pause or not typing_state:
            prompt_res = voice_comp.detect_pause_and_prompt(event_data, is_typing=typing_state)
            if prompt_res["asked"]:
                st.success(f"🗣️ **ElevenLabs Voice Companion (Expressive Mode):**\n\n\"{prompt_res['question']}\"")
                st.caption(f"Category: {prompt_res['category']} | Voice ID: {prompt_res['audio_voice_id']}")
                
                # Show Expert Answer
                if amount > 5000:
                    st.write("💬 **Sabine (Expert Reply):** *\"Equipment over €5,000 is always CapEx. Lena, never leave it as 4711 unless you want to break month-end close.\"*")
                elif "TechCzech" in supplier:
                    st.write("💬 **Sabine (Expert Reply):** *\"This supplier double-bills every December without fail. Hold until January reconciliation.\"*")
                else:
                    st.write("💬 **Sabine (Expert Reply):** *\"Czech subsidiary invoices require secondary controller sign-off, no matter the amount.\"*")
            else:
                st.warning("🤫 Voice Agent stays quiet while Sabine types...")

# -----------------------------------------------------------------------------
# MODULE 2: MAP
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("🗺️ Module 2: Clickable Work Map & Debrief")
    st.write("The post-session debrief turns Sabine's actions and quotes into a structured Work Map linking every step to a screen moment, decision, and guardrail.")

    wm = st.session_state.work_map
    meta = wm["metadata"]

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        st.metric("Expert", meta["expert_name"])
    with col_meta2:
        st.metric("Guardrails Captured", meta["guardrails_captured"])
    with col_meta3:
        st.metric("Teach-Back Status", meta["expert_teach_back_status"])

    st.markdown("---")
    st.markdown("### 📌 Clickable Process Timeline & Guardrail Inventory")

    for step in wm["steps"]:
        st.markdown(f"""
        <div class="step-card">
            <h4 style="color: #34d399; margin-bottom: 4px;">Step {step['step_number']}: {step['title']}</h4>
            <p><b>Screen Moment:</b> <code>{step['screen_moment']}</code></p>
            <p><b>Decision Made:</b> {step['decision']}</p>
            <p><b>Expert Reason:</b> <i>"{step['expert_reason']}"</i></p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🛡️ Guardrails for Step {step['step_number']} ({len(step['guardrails'])} active rules)"):
            for g in step['guardrails']:
                st.markdown(f"- 🛑 **Guardrail Rule:** {g}")

    # Export JSON
    st.markdown("---")
    json_export = json.dumps(wm, indent=2)
    st.download_button(
        label="📄 Download Complete Work Map (JSON)",
        data=json_export,
        file_name="sabine_stuttgart_invoicing_work_map.json",
        mime="application/json"
    )

# -----------------------------------------------------------------------------
# MODULE 3: TEACH
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("🎓 Module 3: Voice Tutor Coaching Lab")
    st.write("Watch **Lena (New Hire, Day 4)** process a new, unseen invoice case on her own screen. The ElevenLabs Voice Tutor coaches her and **intercepts mistakes before they are saved**.")

    col_t1, col_t2 = st.columns([3, 2])

    with col_t1:
        st.markdown("#### 👩‍💻 Lena's Screen (New Hire Processing Unseen Case)")
        st.info("📋 **Case File**: Unseen Invoice #9910 | Amount: **€7,500.00** | Supplier: Industrial Equipment Direct")

        st.write("Lena selects cost center for this €7,500 equipment invoice:")
        lena_code = st.radio(
            "Select Cost Center Code:",
            ["4711 (OpEx - General Operational Expense)", "0400 (CapEx - Capitalized Equipment)"],
            index=0
        )
        has_asset = st.checkbox("Attach Asset Tag Number", value=True)
        attempt_save = st.button("💾 Attempt to Save Invoice to SAP", use_container_width=True)

    with col_t2:
        st.markdown("#### 🛡️ Voice Tutor Guardrail Interceptor")
        tutor = VoiceTutorCoach(st.session_state.work_map)

        if attempt_save:
            hire_action = {
                "amount_eur": 7500.0,
                "cost_center_selected": lena_code,
                "supplier": "Industrial Equipment Direct",
                "has_asset_tag": has_asset
            }
            res = tutor.evaluate_new_hire_action(hire_action)

            if res["intercepted"]:
                st.markdown(f"""
                <div class="intercept-card">
                    <h3 style="color: #ef4444; margin-top: 0;">🛑 MISTAKE INTERCEPTED BEFORE SAVE!</h3>
                    <p style="font-size: 1.1rem; color: #ffffff;"><b>Voice Tutor Speech:</b> {res['tutor_speech']}</p>
                    <hr style="border-color: #7f1d1d;">
                    <p style="color: #fca5a5;"><b>Expert Quote:</b> <i>"{res['expert_quote']}"</i></p>
                    <p style="color: #cbd5e1;"><b>Replaying Screen Moment:</b> <code>{res['replay_screen_moment']}</code></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ **Voice Tutor:** Perfect! You correctly applied Sabine's €5,000 CapEx rule. Invoice saved cleanly.")

        # Mastery Card
        report = tutor.get_mastery_report()
        st.markdown("---")
        st.metric("Lena's Process Mastery Score", f"{report['mastery_score']}%", delta="Guardrail Active")

# -----------------------------------------------------------------------------
# THE MOONSHOT PITCH
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("🚀 Think Bigger: The AI Apprentice Moonshot")
    
    st.markdown("""
    ### 🌌 The Living Company Memory & Global Operations Manual
    
    > *"Turn every retiring expert into a Work Map and a Voice Tutor instead of a farewell party."*
    
    #### 1. The Always-On Apprentice
    No scheduled interviews. The AI Apprentice silently observes everyday digital operations across Thousands of desks, asking **one question at the right moment** when it detects a new exception pattern.
    
    #### 2. People First, Then Safe Agents
    The Work Map's guardrails teach new human hires first. Once validated, routine steps are exported as agent-ready SOPs, letting autonomous agents execute repetitive tasks safely while humans retain high-judgment calls.
    
    #### 3. The World's Digital Operations Manual
    Anonymized Work Maps across thousands of enterprises mapping how digital work is *really* done, preserving decades of human wisdom for future generations.
    """)

st.markdown("---")
st.caption("Developed for 7th Global AI Hackathon · ElevenLabs × Hack-Nation Challenge 01")
