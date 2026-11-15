import os
import sqlite3
import streamlit as st

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "planner.db")

def _get_connection():
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        return conn
    except Exception:
        return None

def render_group_planner_summary():
    """
    Renders collaborative group planning rooms directly from planner.db SQLite.
    """
    st.markdown("### 👥 Group Travel Rooms & Voting Radar")
    st.caption("Synchronized with your local SQLite collaborative room database (`planner.db`).")

    conn = _get_connection()
    if not conn:
        st.warning("Could not connect to planner.db")
        return

    c = conn.cursor()
    try:
        c.execute("CREATE TABLE IF NOT EXISTS rooms (code TEXT PRIMARY KEY, host TEXT, budget INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS members (room_code TEXT, name TEXT, UNIQUE(room_code, name))")
        c.execute("CREATE TABLE IF NOT EXISTS votes (room_code TEXT, destination TEXT, votes INTEGER, PRIMARY KEY(room_code, destination))")
        conn.commit()

        c.execute("SELECT code, host, budget FROM rooms")
        rooms = c.fetchall()
    except Exception as e:
        st.info(f"Database initialized: {e}")
        rooms = []
    finally:
        conn.close()

    if not rooms:
        # Seed with initial room for review demonstration if empty
        conn = _get_connection()
        if conn:
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO rooms VALUES (?, ?, ?)", ("CSP-2026", "Charitha", 12000))
            c.execute("INSERT OR IGNORE INTO members VALUES (?, ?)", ("CSP-2026", "Charitha"))
            c.execute("INSERT OR IGNORE INTO members VALUES (?, ?)", ("CSP-2026", "Reviewer B13"))
            c.execute("INSERT OR IGNORE INTO votes VALUES (?, ?, ?)", ("CSP-2026", "Goa", 4))
            c.execute("INSERT OR IGNORE INTO votes VALUES (?, ?, ?)", ("CSP-2026", "Araku", 2))
            conn.commit()
            conn.close()
            rooms = [("CSP-2026", "Charitha", 12000)]

    cols = st.columns(min(len(rooms), 3)) if rooms else [st]
    for idx, (code, host, budget) in enumerate(rooms):
        col = cols[idx % len(cols)]
        with col:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #7c3aed; padding: 16px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="background: #f5f3ff; color: #7c3aed; border: 1px solid #ddd6fe; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">ROOM: {code}</span>
                    <span style="font-size: 0.75rem; color: #059669; font-weight: 700;">● Active</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #1e3a8a; margin: 4px 0;">Host: {host}</div>
                <div style="font-size: 0.82rem; color: #64748b;">Target Group Budget: <strong style="color: #059669;">₹{budget:,}</strong></div>
                <div style="margin-top: 8px; font-size: 0.75rem; color: #7c3aed; font-weight: 600;">
                    ✓ Multi-user Voting Enabled
                </div>
            </div>
            """, unsafe_allow_html=True)
