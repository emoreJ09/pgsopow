import streamlit as st
import db  # Gagamitin ang kinopya mong db.py sa parehong folder

# I-import ang mga ginawa nating modules sa parehong folder
import preview_pow_module
import preview_module

# Set up physical page space allocation
st.set_page_config(page_title="PGSO POW System", layout="wide")

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
if 'page_view_mode' not in st.session_state:
    st.session_state.page_view_mode = 'table_view'  # Sub-router view block flag

# --- MGA PALANDINGAN O PAHINGA NG WEB APP (SCREENS) ---

def show_login():
    st.markdown("<h2 style='text-align: center; color: #2196F3;'>ACCOUNT LOGIN</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_user").strip()
    password = st.text_input("Password", type="password", key="login_pass").strip()
    
    if st.button("Login", use_container_width=True, type="primary"):
        if not username or not password:
            st.warning("⚠️ Attention! All input fields must be filled out before proceeding")
        else:
            user_role = db.authenticate_user(username, password)
            
            if user_role:
                st.success(f"🎉 Success! Logged in as {user_role.upper()}.")
                st.session_state.username = username
                st.session_state.user_role = user_role
                st.session_state.page = 'dashboard'
                st.session_state.page_view_mode = 'table_view' # Reset to default view
                st.rerun()
            else:
                st.error("❌ Login Failed! Invalid username or password. Please try again.")
                
    st.markdown("---")
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
            success, message = db.register_user(username, password, role='encoder')
            
            if success:
                st.success(f"🎯 {message}")
                st.info("Maaari ka nang bumalik sa Login page para mag-sign in.")
            else:
                st.error(f"❌ Registration Failed! {message}")
                
    st.markdown("---")
    if st.button("Already have an account? Log In", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()


def show_dashboard():
    # --- SIDEBAR CONTROL CONTROL PANEL ---
    st.sidebar.markdown(f"### 👤 User: **{st.session_state.username.upper()}**")
    st.sidebar.caption(f"Role Profile: {st.session_state.user_role.upper()}")
    st.sidebar.write("---")
    
    # 🗂️ MAIN APP INTERACTIVE MENU DROPDOWN / RADIO SELECTOR
    menu_choice = st.sidebar.radio(
        "🗂️ Navigation Menu",
        ["Dashboard & POW List", "Create New POW (Form)"]
    )
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Logout Account", type="secondary", use_container_width=True):
        st.session_state.page = 'login'
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.page_view_mode = 'table_view'
        st.rerun()

    # --- MAIN ENGINE DISTRIBUTION INTERACTION ROUTER ---
    if menu_choice == "Dashboard & POW List":
        
        # Sub-routing para sa Print layout generator
        if st.session_state.page_view_mode == "print_preview":
            if st.button("⬅️ Back to Project Explorer Grid", type="secondary"):
                st.session_state.page_view_mode = "table_view"
                st.rerun()
            
            # Luwalan ng Print Preview module screen engine
            preview_module.render_excel_preview_module()
        
        else:
            # Ito ang papalit sa default screen mo! Dito lalabas ang Table at Data Editor grid
            preview_pow_module.render_preview_pow_module()
            
    elif menu_choice == "Create New POW (Form)":
        st.markdown(f"<h1 style='color: #333;'>🏢 PGSO Dashboard</h1>", unsafe_allow_html=True)
        st.subheader("➕ Create New Program of Work")
        st.info("Dito natin ilalagay ang mga input fields para sa data entry ng mga bagong proyekto (Form Builder) mo mamaya.")


# --- APP CONTROLLER ---
with st.container():
    if st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'signup':
        show_signup()
    elif st.session_state.page == 'dashboard':
        show_dashboard()
