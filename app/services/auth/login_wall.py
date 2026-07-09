import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            display: flex;
            align-items: center;
            min-height: 92vh;
        }
        .login-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(245, 178, 60, 0.35);
            color: #F5B23C;
            padding: 4px 14px;
            font-size: 0.75rem;
            letter-spacing: 0.12em;
            margin-bottom: 22px;
        }
        .login-tag .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #F5B23C;
            display: inline-block;
        }
        .login-title {
            font-size: 2.6rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #ffffff 0%, #F5B23C 55%, #6FE3D8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-sub {
            color: #9a9aa2;
            font-size: 1.02rem;
            margin-bottom: 28px;
        }
        [data-testid="stForm"] {
            background: #12151d !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 2rem !important;
            margin-top: 0.5rem !important;
        }
        [data-testid="stForm"] label p {
            color: #c8c8ce !important;
            font-size: 0.85rem !important;
            letter-spacing: 0.04em;
        }
        [data-testid="stForm"] button {
            background: linear-gradient(90deg, #F5B23C, #e89b1f) !important;
            color: #14100a !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em;
        }
        [data-testid="stForm"] button:hover {
            filter: brightness(1.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="login-tag"><span class="dot"></span>AI-POWERED &middot; REAL-TIME &middot; GYM COACH</div>
        <div class="login-title">AI Real-time<br>Gym Coach</div>
        <div class="login-sub">Enter a username to start your session.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("NAME (UNIQUE)", placeholder="e.g. ridanshi")
        submit_button = st.form_submit_button("Start Session →", width="stretch")

    if submit_button:
        if not username:
            st.error("Name cannot be empty.")
            return False

        user = get_or_create_user(username)

        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    return False