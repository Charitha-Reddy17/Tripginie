import streamlit as st
from services.auth_service import authenticate_user, register_user, login_user

def render_login_page():
    """
    Renders professional CSP Project Login & Registration Portal in Navy & Amber styling.
    Clean input fields with empty initial values and standard email/password placeholders.
    """
    st.markdown("""
    <div style="max-width: 540px; margin: 1.5rem auto 1.5rem auto; text-align: center;">
        <span class="hero-badge" style="background: #2563eb; color: white !important; font-size: 11px; padding: 4px 12px; border-radius: 20px; font-weight: 700;">
            🎓 COMMUNITY SERVICE PROJECT (CSP)
        </span>
        <h1 style="font-size: 2.4rem; font-weight: 800; color: #1e3a8a; margin: 10px 0 4px 0; letter-spacing: -0.5px;">
            TripGenie Portal ✈️
        </h1>
        <p style="color: #64748b; font-size: 0.95rem; margin-top: 2px;">
            AI-Assisted Tourism & Heritage Trip Planning • Seshadri Rao Gudlavalleru Engg College
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #bfdbfe; border-top: 5px solid #2563eb; border-radius: 16px; padding: 26px; box-shadow: 0 10px 25px rgba(30, 58, 138, 0.08); margin-bottom: 24px;">
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔐 Sign In", "✨ Student / Traveler Register"])

        # TAB 1: LOGIN
        with tab_login:
            st.markdown("<p style='font-weight: 700; color: #1e3a8a; margin-top: 10px; margin-bottom: 12px;'>Enter your credentials</p>", unsafe_allow_html=True)

            login_input = st.text_input("📧 Email", key="login_email_input", placeholder="email")
            password_input = st.text_input("🔑 Password", type="password", key="login_pass_input", placeholder="password")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🚀 Access TripGenie Portal", key="btn_signin_submit", use_container_width=True):
                if not login_input or not password_input:
                    st.error("⚠️ Please enter both email and password.")
                else:
                    user = authenticate_user(login_input, password_input)
                    if user:
                        login_user(user)
                        st.success(f"🎉 Welcome, {user.get('name')}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please check your email and password.")

            st.markdown("<hr style='margin: 16px 0; border-color: #f1f5f9;'/>", unsafe_allow_html=True)

            # Quick 1-Click Access for Viva / Evaluations
            st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #64748b; text-align: center; margin-bottom: 8px;'>PROJECT EVALUATION ACCESS</p>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("⚡ 1-Click Demo Login", key="btn_demo_login", use_container_width=True):
                    demo_user = authenticate_user("charitha@tripgenie.com", "password123")
                    if demo_user:
                        login_user(demo_user)
                        st.success("🎉 Logged in as Charitha!")
                        st.rerun()
            with col_d2:
                if st.button("👤 Continue as Guest", key="btn_guest_login", use_container_width=True):
                    guest_user = {
                        "id": "usr_guest",
                        "name": "Guest Student",
                        "email": "guest@tripgenie.com",
                        "role": "Guest Explorer",
                        "home_city": "Hyderabad",
                        "travel_style": "Relaxed",
                        "avatar_emoji": "🧭"
                    }
                    login_user(guest_user)
                    st.success("👋 Welcome, Guest!")
                    st.rerun()

        # TAB 2: REGISTER
        with tab_register:
            st.markdown("<p style='font-weight: 700; color: #1e3a8a; margin-top: 10px; margin-bottom: 12px;'>Register New Student / Traveler Account</p>", unsafe_allow_html=True)

            reg_name = st.text_input("👤 Full Name", key="reg_name_input", placeholder="Full Name")
            reg_email = st.text_input("📧 Email Address", key="reg_email_input", placeholder="email")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                reg_city = st.text_input("📍 Origin / Home City", key="reg_city_input", placeholder="Origin City")
            with col_r2:
                reg_style = st.selectbox(
                    "🎭 Travel Mood",
                    ["Relaxed", "Adventurous", "Romantic", "Peaceful"],
                    key="reg_style_input"
                )

            reg_pass1 = st.text_input("🔑 Password", type="password", key="reg_pass1_input", placeholder="password")
            reg_pass2 = st.text_input("🔒 Confirm Password", type="password", key="reg_pass2_input", placeholder="password")

            if st.button("✨ Register & Launch", key="btn_register_submit", use_container_width=True):
                if not reg_name or not reg_email or not reg_pass1:
                    st.error("⚠️ All fields are required.")
                elif reg_pass1 != reg_pass2:
                    st.error("⚠️ Passwords do not match.")
                else:
                    success, msg = register_user(
                        name=reg_name,
                        email=reg_email,
                        password=reg_pass1,
                        travel_style=reg_style,
                        home_city=reg_city or "Hyderabad"
                    )
                    if success:
                        new_user = authenticate_user(reg_email, reg_pass1)
                        if new_user:
                            login_user(new_user)
                            st.success("🎉 Account created successfully!")
                            st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("</div>", unsafe_allow_html=True)

def render_user_profile_bar():
    """
    Renders top/sidebar status widget for authenticated student/user.
    """
    user = st.session_state.get("user_info")
    if not user:
        return

    name = user.get("name", "Traveler")
    email = user.get("email", "")
    role = user.get("role", "Traveler")
    emoji = user.get("avatar_emoji", "👤")

    st.sidebar.markdown(f"""
    <div style="background: #ffffff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 12px; padding: 12px 14px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05); display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 1.6rem; background: #eff6ff; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
            {emoji}
        </div>
        <div style="flex: 1; overflow: hidden;">
            <div style="font-weight: 700; color: #1e3a8a; font-size: 0.92rem; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{name}</div>
            <div style="font-size: 0.72rem; color: #64748b; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{email}</div>
            <span style="display: inline-block; background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-size: 0.65rem; font-weight: 700; padding: 1px 6px; border-radius: 12px; margin-top: 3px;">{role}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
        from services.auth_service import logout_user
        logout_user()
        st.rerun()
