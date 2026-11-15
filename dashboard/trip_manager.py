import streamlit as st
from typing import List, Dict, Any

def render_saved_trips(trips: List[Dict[str, Any]]):
    """
    Renders user's saved expeditions with 1-click planner synchronization.
    """
    st.markdown("### 🧳 Trip Portfolio & Expeditions")
    st.caption("Access previous itineraries or load a trip directly into the AI Planner.")

    if not trips:
        st.info("No saved trips found. Plan your first trip using the planner!")
        return

    cols = st.columns(len(trips)) if len(trips) <= 3 else st.columns(3)

    for idx, trip in enumerate(trips):
        col = cols[idx % len(cols)]
        dest = trip.get("destination", "Goa")
        origin = trip.get("origin", "Hyderabad")
        duration = trip.get("duration", 3)
        mood = trip.get("mood", "Relaxed")
        mode = trip.get("mode", "Train")
        budget = trip.get("budget", 4950)
        status = trip.get("status", "Planned")
        img_url = trip.get("image", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80")
        highlights = trip.get("highlights", [])

        status_color = "#15803d" if status == "Upcoming" else ("#2563eb" if status == "Planned" else "#64748b")
        status_bg = "#f0fdf4" if status == "Upcoming" else ("#eff6ff" if status == "Planned" else "#f1f5f9")

        with col:
            st.markdown(f"""
            <div class="card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column; border-radius: 12px;">
                <div style="position: relative; height: 130px; overflow: hidden;">
                    <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" alt="{dest}"/>
                    <div style="position: absolute; top: 10px; right: 10px;">
                        <span style="background: {status_bg}; color: {status_color}; padding: 3px 8px; border-radius: 9999px; font-weight: 700; font-size: 0.72rem;">
                            {status}
                        </span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 12px; color: white;">
                        <div style="font-weight: 800; font-size: 1.25rem; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">{dest}</div>
                    </div>
                </div>
                <div style="padding: 14px; flex: 1;">
                    <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 6px;">
                        🛫 <strong>{origin}</strong> ➔ 🛬 <strong>{dest}</strong> ({mode})
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 8px; color: #1e3a8a;">
                        <span>📅 <strong>{duration} Days</strong> ({mood})</span>
                        <span style="font-weight: 800; color: #15803d;">₹{budget:,}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #475569; margin-bottom: 12px;">
                        <strong>Highlights:</strong> {', '.join(highlights[:2])}...
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            def _load_trip_callback(d=dest, o=origin, dur=duration, m=mode, md=mood):
                st.session_state["destination_input"] = d
                st.session_state["origin_input"] = o
                st.session_state["days_slider"] = dur
                st.session_state["mode_select"] = m
                mood_map = {
                    "Relaxed": "Relaxed 🏖️",
                    "Adventurous": "Adventurous 🧗",
                    "Romantic": "Romantic 🌅",
                    "Peaceful": "Peaceful 🧘"
                }
                if md in mood_map:
                    st.session_state["mood_select"] = mood_map[md]
                st.session_state["main_view_selection"] = "🗺️ AI Trip Planner & Heritage Radar"

            st.button(
                f"🔍 Load {dest} into Planner",
                key=f"btn_load_trip_{idx}",
                on_click=_load_trip_callback,
                use_container_width=True
            )
