import streamlit as st
import requests

st.set_page_config(layout="wide")

API_URL = "http://127.0.0.1:8000"

# -------------------- PREMIUM CSS --------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(10,15,25,0.6), rgba(10,15,25,0.8)),
                url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    color: white;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    border-radius: 15px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
}

/* Logo */
.logo {
    font-size: 20px;
    font-weight: bold;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    margin-bottom: 15px;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
}

/* Chat bubbles */
.user {
    background: #2563eb;
    padding: 10px;
    border-radius: 10px;
    text-align: right;
    margin-bottom: 5px;
}

.ai {
    background: rgba(255,255,255,0.1);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}

/* Title */
.title {
    font-size: 32px;
    font-weight: 600;
}

.subtitle {
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# -------------------- NAVBAR --------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

col1, col2, col3 = st.columns([2,4,1])

with col1:
    st.markdown("🔷 **Adaptive AI OS**")

with col2:
    nav1, nav2, nav3 = st.columns(3)
    if nav1.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if nav2.button("AI Orchestrator"):
        st.session_state.page = "AI"
    if nav3.button("Analytics"):
        st.session_state.page = "Analytics"

with col3:
    st.markdown("👤 JR")

# -------------------- DASHBOARD --------------------
if st.session_state.page == "Dashboard":

    st.markdown("<div class='title'>Good afternoon.</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your AI is actively managing your workflow.</div>", unsafe_allow_html=True)

    colA, colB = st.columns([4,1])

    with colA:
        ai_level = st.slider("AI Sensitivity", 0, 100, 65)

    with colB:
        if st.button("+ New Task"):
            requests.post(f"{API_URL}/add_task", json={
                "title": "Task",
                "time": 10,
                "priority": "High"
            })

    # Personnel
    st.markdown("### Personnel")

    people = [
        ("Alex", "Meeting", 78),
        ("Sarah", "Interview", 62),
        ("Jordan", "Focus", 85),
        ("Mia", "Design", 45),
    ]

    cols = st.columns(len(people))
    for i, p in enumerate(people):
        with cols[i]:
            st.markdown(f"""
            <div class='card'>
            <b>{p[0]}</b><br>
            {p[1]}<br>
            Load: {p[2]}%
            </div>
            """, unsafe_allow_html=True)

    # Timeline + Stats
    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown("<div class='card'><b>Workflow Timeline</b></div>", unsafe_allow_html=True)

        tasks = requests.get(
            f"{API_URL}/schedule",
            params={"ai_level": ai_level}
        ).json()

        for t in tasks:
            st.markdown(f"""
            <div class='card'>
            🕒 {t['time']}:00<br>
            📌 {t['title']}<br>
            ⚡ {t['priority']}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'><b>Stats</b></div>", unsafe_allow_html=True)

        raw = requests.get(f"{API_URL}/get_tasks").json()

        st.markdown(f"""
        <div class='card'>
        Tasks: {len(raw)}<br>
        Completed: {len([t for t in raw if t.get("status")=="completed"])}
        </div>
        """, unsafe_allow_html=True)

# -------------------- AI ORCHESTRATOR --------------------
if st.session_state.page == "AI":

    st.markdown("<div class='card'><b>AI Orchestrator</b></div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    msg = st.text_input("Enter command")

    if st.button("Send") and msg:
        res = requests.get(f"{API_URL}/chat", params={"query": msg})
        response = res.json()["response"]

        st.session_state.messages.append(("user", msg))
        st.session_state.messages.append(("ai", response))

    for role, m in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='user'>{m}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai'>{m}</div>", unsafe_allow_html=True)

# -------------------- ANALYTICS --------------------
if st.session_state.page == "Analytics":

    st.markdown("<div class='card'><b>Analytics</b></div>", unsafe_allow_html=True)

    st.line_chart([60, 65, 75, 85, 90])
    st.bar_chart([10, 5])