import streamlit as st
from database_cloud import init_db, add_medicine, get_all_medicines, delete_medicine, get_medicines_by_timing
st.set_page_config(
    page_title="Medicine Tracker",
    page_icon="💊",
    layout="wide"
)

# Initialize database
init_db()

# Custom CSS
st.markdown("""
    <style>
    .medicine-card {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #7c3aed;
    }
    .medicine-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .medicine-detail {
        font-size: 14px;
        color: #a0aec0;
        margin: 2px 0;
    }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-morning {
        background-color: #fef3c7;
        color: #92400e;
    }
    .badge-night {
        background-color: #dbeafe;
        color: #1e40af;
    }
    .badge-afternoon {
        background-color: #dcfce7;
        color: #166534;
    }
    .badge-default {
        background-color: #f3e8ff;
        color: #6b21a8;
    }
    .header-text {
        font-size: 13px;
        color: #6b7280;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/pill.png", width=60)
    st.title("Medicine Tracker")
    st.write("Your personal medicine manager.")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Today's Schedule", "My Medicines", "Add Medicine", "Check Interactions"],
        index=0
    )
    st.divider()
    medicines_count = len(get_all_medicines())
    st.metric("Total Medicines", medicines_count)


# Helper function for timing badge
def get_badge(timing):
    timing_lower = timing.lower()
    if "morning" in timing_lower:
        return f'<span class="badge badge-morning">🌅 {timing}</span>'
    elif "night" in timing_lower:
        return f'<span class="badge badge-night">🌙 {timing}</span>'
    elif "afternoon" in timing_lower:
        return f'<span class="badge badge-afternoon">☀️ {timing}</span>'
    else:
        return f'<span class="badge badge-default">⏰ {timing}</span>'


# Page: Add Medicine
if page == "Add Medicine":
    st.title("Add a New Medicine")
    st.markdown('<p class="header-text">Fill in the details below to add a medicine.</p>',
                unsafe_allow_html=True)

    with st.form("add_medicine_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Medicine Name *", placeholder="e.g. Paracetamol")
            dosage = st.text_input("Dosage", placeholder="e.g. 500mg")

        with col2:
            timing = st.text_input("Timing", placeholder="e.g. Morning, Night")
            notes = st.text_input("Notes", placeholder="e.g. After food")

        submitted = st.form_submit_button("Add Medicine", use_container_width=True)

        if submitted:
            if name.strip() == "":
                st.error("Medicine name cannot be empty.")
            else:
                add_medicine(name, dosage, timing, notes)
                st.success(f"✅ {name} added successfully!")
                st.balloons()


# Page: My Medicines
elif page == "My Medicines":
    st.title("My Medicines")
    st.markdown('<p class="header-text">All your medicines in one place.</p>',
                unsafe_allow_html=True)

    medicines = get_all_medicines()

    if len(medicines) == 0:
        st.info("No medicines added yet. Go to 'Add Medicine' to get started.")
    else:
        for med in medicines:
            med_id = med[0]
            med_name = med[1]
            med_dosage = med[2] if med[2] else "Not specified"
            med_timing = med[3] if med[3] else "Not specified"
            med_notes = med[4] if med[4] else "—"

            badge_html = get_badge(med_timing)

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"""
                    <div class="medicine-card">
                        <div class="medicine-name">💊 {med_name}</div>
                        <div class="medicine-detail">📦 Dosage: {med_dosage}</div>
                        <div class="medicine-detail">📝 Notes: {med_notes}</div>
                        <div style="margin-top:8px">{badge_html}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Delete", key=f"del_{med_id}"):
                    delete_medicine(med_id)
                    st.rerun()


# Page: Check Interactions
elif page == "Check Interactions":
    st.title("⚠️ Drug Interaction Checker")
    st.markdown('<p class="header-text">Check if your medicines are safe to take together.</p>',
                unsafe_allow_html=True)

    medicines = get_all_medicines()

    if len(medicines) < 2:
        st.warning("You need at least 2 medicines added to check interactions.")
    else:
        medicine_names = [med[1] for med in medicines]

        st.write("**Checking interactions between:**")
        cols = st.columns(4)
        for i, name in enumerate(medicine_names):
            with cols[i % 4]:
                st.markdown(f"""
                    <div style="background:#2d2d3f;padding:8px 12px;
                    border-radius:8px;text-align:center;margin:4px 0;
                    font-size:13px;color:#e2e8f0;">
                        💊 {name}
                    </div>
                """, unsafe_allow_html=True)

        st.write("")

        if st.button("Check for Interactions", use_container_width=True):
            with st.spinner("Checking medical database..."):
                from interaction import check_interactions
                interactions, not_found = check_interactions(medicine_names)

            if len(interactions) == 0:
                st.success("✅ No known interactions found between your medicines.")
                st.caption("Always consult a doctor or pharmacist for medical advice.")
            else:
                st.error(f"⚠️ {len(interactions)} interaction(s) found — please consult your doctor.")

                for interaction in interactions:
                    severity = interaction["severity"].lower()

                    if severity == "high":
                        color = "#ef4444"
                        icon = "🔴"
                    elif severity == "moderate":
                        color = "#f97316"
                        icon = "🟠"
                    else:
                        color = "#eab308"
                        icon = "🟡"

                    st.markdown(f"""
                        <div style="background:#1e1e2e;border-left:4px solid {color};
                        border-radius:8px;padding:16px 20px;margin:10px 0;">
                            <div style="font-weight:700;color:{color};
                            font-size:15px;margin-bottom:8px;">
                                {icon} {interaction['med1']} + {interaction['med2']}
                            </div>
                            <div style="color:#a0aec0;font-size:13px;line-height:1.6;">
                                {interaction['description']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.caption("⚕️ For informational purposes only. Always consult a doctor before making medication decisions.")
                # Page: Today's Schedule
elif page == "Today's Schedule":
    st.title("📅 Today's Schedule")
    st.markdown('<p class="header-text">Your medicines for today, organised by time of day.</p>',
                unsafe_allow_html=True)

    from datetime import datetime

    # Get current hour to determine current period
    current_hour = datetime.now().hour

    if 6 <= current_hour < 12:
        current_period = "morning"
    elif 12 <= current_hour < 18:
        current_period = "afternoon"
    elif 18 <= current_hour < 24:
        current_period = "night"
    else:
        current_period = "night"

    # Define the three periods
    periods = [
        {
            "name": "Morning",
            "keyword": "morning",
            "icon": "🌅",
            "time": "6:00 AM – 12:00 PM",
            "color": "#f59e0b"
        },
        {
            "name": "Afternoon",
            "keyword": "afternoon",
            "icon": "☀️",
            "time": "12:00 PM – 6:00 PM",
            "color": "#10b981"
        },
        {
            "name": "Night",
            "keyword": "night",
            "icon": "🌙",
            "time": "6:00 PM – 12:00 AM",
            "color": "#6366f1"
        }
    ]

    # Show current time
    now = datetime.now().strftime("%I:%M %p")
    st.info(f"🕐 Current time: {now}")
    st.write("")

    total_due = 0
    any_medicines = False

    for period in periods:
        medicines = get_medicines_by_timing(period["keyword"])

        if len(medicines) == 0:
            continue

        any_medicines = True
        is_current = period["keyword"] == current_period

        # Period header
        if is_current:
            st.markdown(f"""
                <div style="background:#1e1e2e;border-left:4px solid {period['color']};
                border-radius:8px;padding:12px 16px;margin:16px 0 8px 0;">
                    <span style="font-size:18px;font-weight:700;color:{period['color']};">
                        {period['icon']} {period['name']}
                    </span>
                    <span style="font-size:12px;color:#a0aec0;margin-left:10px;">
                        {period['time']}
                    </span>
                    <span style="font-size:11px;background:{period['color']}33;
                    color:{period['color']};padding:2px 8px;border-radius:10px;
                    margin-left:8px;font-weight:600;">
                        ⏰ DUE NOW
                    </span>
                </div>
            """, unsafe_allow_html=True)
            total_due += len(medicines)
        else:
            st.markdown(f"""
                <div style="background:#1e1e2e;border-left:4px solid #374151;
                border-radius:8px;padding:12px 16px;margin:16px 0 8px 0;">
                    <span style="font-size:18px;font-weight:700;color:#6b7280;">
                        {period['icon']} {period['name']}
                    </span>
                    <span style="font-size:12px;color:#4b5563;margin-left:10px;">
                        {period['time']}
                    </span>
                </div>
            """, unsafe_allow_html=True)

        # Show medicines for this period
        for med in medicines:
            med_name = med[1]
            med_dosage = med[2] if med[2] else "No dosage specified"
            med_notes = med[4] if med[4] else ""

            if is_current:
                st.markdown(f"""
                    <div style="background:#2d2d3f;border-radius:8px;
                    padding:12px 16px;margin:6px 0;
                    border:1px solid {period['color']}44;">
                        <span style="font-size:15px;font-weight:600;
                        color:#ffffff;">💊 {med_name}</span>
                        <span style="font-size:13px;color:#a0aec0;
                        margin-left:10px;">
                            {med_dosage}
                        </span>
                        {f'<span style="font-size:12px;color:#6b7280;margin-left:8px;">• {med_notes}</span>' if med_notes else ''}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background:#1a1a2e;border-radius:8px;
                    padding:12px 16px;margin:6px 0;
                    border:1px solid #2d2d3f;">
                        <span style="font-size:15px;color:#6b7280;">
                            💊 {med_name}
                        </span>
                        <span style="font-size:13px;color:#4b5563;
                        margin-left:10px;">
                            {med_dosage}
                        </span>
                    </div>
                """, unsafe_allow_html=True)

    if not any_medicines:
        st.info("No medicines scheduled yet. Add medicines with Morning, Afternoon, or Night in the timing field.")

    # Summary at bottom
    if any_medicines and total_due > 0:
        st.write("")
        st.warning(f"⚠️ You have {total_due} medicine(s) due right now. Please take them on time.")
    elif any_medicines:
        st.write("")
        st.success("✅ No medicines due right now.")