import streamlit as st
import db  # Gagamitin ang kinopya mong db.py sa parehong folder

# 1. I-initialize ang database sa unang load ng website
if 'db_ready' not in st.session_state:
    db.initialize_db()
    st.session_state.db_ready = True

# 2. State management para sa paglipat-lipat ng screen at user sessions
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- MGA PALANDINGAN O PAHINGA NG WEB APP (SCREENS) ---

def show_login():
    st.markdown("<h2 style='text-align: center; color: #2196F3;'>ACCOUNT LOGIN</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_user").strip()
    password = st.text_input("Password", type="password", key="login_pass").strip()
    
    # Login button layout
    if st.button("Login", use_container_width=True, type="primary"):
        if not username or not password:
            st.warning("⚠️ Attention! All input fields must be filled out before proceeding")
        else:
            # Dito tinatawag ang authenticate function mo mula sa db.py
            user_role = db.authenticate_user(username, password)
            
            if user_role:
                st.success(f"🎉 Success! Logged in as {user_role.upper()}.")
                st.session_state.username = username
                st.session_state.user_role = user_role
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("❌ Login Failed! Invalid username or password. Please try again.")
                
    st.markdown("---")
    # Link papuntang Sign Up
    if st.button("Don't have an account? Sign Up", use_container_width=True):
        st.session_state.page = 'signup'
        st.rerun()


def show_signup():
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)
    
    username = st.text_input("New Username", key="reg_user").strip()
    password = st.text_input("New Password", type="password", key="reg_pass").strip()
    
    if st.button("Register Account", use_container_width=True):
        if not username or not password:
            st.warning("⚠️ Attention! All fields are required to register an account.")
        else:
            # Dito tinatawag ang register function mo mula sa db.py
            success, message = db.register_user(username, password, role='encoder')
            
            if success:
                st.success(f"🎯 {message}")
                st.info("Maaari ka nang bumalik sa Login page para mag-sign in.")
            else:
                st.error(f"❌ Registration Failed! {message}")
                
    st.markdown("---")
    # Link pabalik ng Login
    if st.button("Already have an account? Log In", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()


def show_dashboard():
    st.markdown(f"<h1 style='color: #333;'>🏢 PGSO Dashboard</h1>", unsafe_allow_html=True)
    st.subheader(f"Welcome, {st.session_state.username}! ({st.session_state.user_role.upper()})")
    
    # -------------------------------------------------------------
    # 📝 PAALALA SA DASHBOARD:
    # pansamantala muna nating inilagay ito habang wala pa ang dashboard.py mo.
    st.info("Dito natin ilalagay ang mga input fields para sa data entry ng mga encoders mo mamaya.")
    # -------------------------------------------------------------

    st.markdown("---")
    if st.button("Logout", type="secondary"):
        st.session_state.page = 'login'
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()


# --- APP CONTROLLER (Katulad ng AppController class mo sa Tkinter) ---
# Ginawa nating malinis na card-style box para maganda tingnan sa mobile screen
with st.container():
    if st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'signup':
        show_signup()
    elif st.session_state.page == 'dashboard':
        show_dashboard()