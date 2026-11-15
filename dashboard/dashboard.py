import streamlit as st
from services.auth_service import get_current_user, get_user_trips
from .stats_card import render_kpi_metrics
from .trip_manager import render_saved_trips
from .group_planner_card import render_group_planner_summary

def render_travel_dashboard(current_dest: str = "Goa", dest_meta: dict = None):
    """
    Renders the Executive Travel & Academic Review Dashboard.
    """
    user = get_current_user() or {
        "name": "Explorer",
        "email": "student@tripgenie.com",
        "role": "Student Researcher",
        "travel_style": "Relaxed",
        "home_city": "Hyderabad"
    }

    user_name = user.get("name", "Student Explorer")
    user_email = user.get("email", "")
    trips = get_user_trips(user_email)

    # 1. Welcome & Project Review Banner
    st.markdown(f"""
    <div class="hero-block" style="padding: 24px 28px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="hero-badge">🎓 EXECUTIVE CSP DASHBOARD</span>
                <div class="hero-title" style="font-size: 26px; margin-top: 6px;">Welcome back, {user_name}! 👋</div>
                <div class="hero-subtitle" style="font-size: 14.5px; margin-bottom: 0;">
                    Community Service Project • Tourism Analytics, Heritage Preservation & Budget Planning
                </div>
            </div>
            <div style="text-align: right; background: rgba(255,255,255,0.15); padding: 10px 18px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; font-weight: 700;">CURRENT FOCUS</div>
                <div style="font-size: 20px; font-weight: 800; color: #ffffff;">📍 {current_dest.title()}</div>
                <div style="font-size: 11px; color: #bbf7d0; font-weight: 600;">Radar Synced</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. KPI Metrics Summary
    stats = {
        "total_trips": len(trips) if trips else 3,
        "total_budget": sum(t.get("budget", 4500) for t in trips) if trips else 17950,
        "heritage_sites": 16,
        "group_rooms": 2
    }
    render_kpi_metrics(stats)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. Quick Action Hub
    st.markdown("#### ⚡ Quick Actions & Tools")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🗺️ Open AI Itinerary Planner", key="dash_qa_planner", use_container_width=True):
            st.info("💡 Switch to the **'🗺️ AI Trip Planner & Heritage Radar'** tab to generate day-wise itineraries.")
    with qa2:
        if st.button("👥 Collaborative Room Voting", key="dash_qa_group", use_container_width=True):
            st.info("💡 Switch to the **'👥 Collaborative Group Room Voting'** tab to create or vote in trip rooms.")
    with qa3:
        if st.button("🤖 Ask AI Travel Genie", key="dash_qa_ai", use_container_width=True):
            st.info("💡 Switch to the Planner tab to chat with TripGenie AI assistant.")

    st.markdown("<hr style='border-color: #e2e8f0; margin: 18px 0;'/>", unsafe_allow_html=True)

    # 4. Saved Trip Portfolio
    render_saved_trips(trips)

    st.markdown("<hr style='border-color: #e2e8f0; margin: 18px 0;'/>", unsafe_allow_html=True)

    # 5. Collaborative Group Rooms from planner.db
    render_group_planner_summary()

    st.markdown("<br/>", unsafe_allow_html=True)

    # 6. Profile & Heritage Insight Card
    col_p, col_h = st.columns([1, 1.2])
    with col_p:
        st.markdown(f"""
        <div class="card" style="height: 100%;">
            <h4 style="margin: 0 0 10px 0; color: #1e3a8a;">👤 Student Researcher Profile</h4>
            <div style="font-size: 0.88rem; color: #475569; line-height: 1.8;">
                • <strong>Name:</strong> {user.get('name', 'Explorer')}<br/>
                • <strong>Email:</strong> {user.get('email', 'student@tripgenie.com')}<br/>
                • <strong>Origin Hub:</strong> {user.get('home_city', 'Hyderabad')}<br/>
                • <strong>Travel Mood Preference:</strong> {user.get('travel_style', 'Relaxed')}<br/>
                • <strong>Institution:</strong> SRGEC (Autonomous) • Batch B13
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_h:
        heritage_text = dest_meta.get("heritage", "Iconic historical monuments and cultural heritage") if dest_meta else "Iconic historical monuments and cultural heritage"
        
        # Load heritage image from catalog if available
        import os, json
        cat_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "heritage_catalog.json")
        h_img, h_name = None, None
        if os.path.exists(cat_file):
            try:
                with open(cat_file, "r", encoding="utf-8") as f:
                    cat = json.load(f)
                    c_key = current_dest.lower().strip()
                    if c_key == "vizag": c_key = "visakhapatnam"
                    if c_key == "bangalore": c_key = "bengaluru"
                    if c_key in cat and cat[c_key]:
                        first = cat[c_key][0]
                        loc = first.get("local_path")
                        full_loc = os.path.join(os.path.dirname(os.path.dirname(__file__)), loc) if loc else ""
                        h_img = full_loc if (full_loc and os.path.exists(full_loc)) else first.get("remote_url")
                        h_name = first.get("title")
            except Exception:
                pass

        st.markdown(f"""
        <div class="card" style="border-left: 4px solid #f59e0b; background: #fffdf5; padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #92400e;">🏛️ Heritage Highlight: {current_dest.title()}</h4>
                <span style="background: #fef3c7; color: #92400e; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 12px; border: 1px solid #fde68a;">CSP VERIFIED</span>
            </div>
            <div style="font-size: 0.86rem; color: #78350f; line-height: 1.6; margin-bottom: 10px;">
                {heritage_text}
            </div>
            <div style="font-size: 0.78rem; color: #047857; font-weight: 600;">
                🌱 Community Objective: Encouraging students and budget travelers to explore and preserve indigenous heritage sites.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if h_img:
            st.image(h_img, caption=f"Historic Landmark: {h_name or current_dest.title()}", use_container_width=True)
