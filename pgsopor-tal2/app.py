import streamlit as st
import pandas as pd
import os
import subprocess
from openpyxl import load_workbook
import io

# Siguraduhing naka-set up ang database function references mula sa db
import db 

st.set_page_config(page_title="PGSO POW System", layout="wide")

# Initialize global system states
if 'db_ready' not in st.session_state:
    db.initialize_db()
    st.session_state.db_ready = True

if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'page_view_mode' not in st.session_state:
    st.session_state.page_view_mode = 'table_view'

# ==============================================================================
# SECTION 1: LOGIN VIEWS FUNCTION
# ==============================================================================
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
                st.session_state.page_view_mode = 'table_view'
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

# ==============================================================================
# SECTION 2: PREVIEW POW MODULE (Dating hiwalay na file, isinama na rito)
# ==============================================================================
def render_preview_pow_module():
    st.markdown("## 📋 PREVIEW SAVED PROGRAM OF WORK (POW)")
    st.caption("Pamahalaan, i-edit, o burahin ang mga naka-save na structural projects sa database system.")

    projects = db.get_project_list()
    if not projects:
        st.info("🗹 Walang mahanap na aktibong proyekto sa database. Gumawa muna ng bago.")
        return

    project_options = {f"ID: {p[0]} | {p[1]}": {"id": p[0], "name": p[1], "location": p[2]} for p in projects}
    selected_label = st.selectbox("🎯 Pumili ng Proyekto sa Listahan:", options=list(project_options.keys()))
    
    current_proj = project_options[selected_label]
    pow_id = current_proj["id"]
    project_name = current_proj["name"]
    location = current_proj["location"]

    st.markdown(f"**📍 Lokasyon:** `{location}`")

    associated_items = db.get_items_by_project(pow_id)
    table_data = []
    grand_total = 0.0
    
    for idx, item in enumerate(associated_items, start=1):
        qty = float(item[0])
        unit = item[1]
        name = item[2]
        price = float(item[3])
        total = qty * price
        grand_total += total
        
        table_data.append({
            "#": idx, "Qty": qty, "Unit": unit, "Item Description": name, "Unit Price (₱)": price, "Total Price (₱)": total
        })

    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df.style.format({"Qty": "{:.2f}", "Unit Price (₱)": "{:,.2f}", "Total Price (₱)": "{:,.2f}"}), use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Walang laman na mga aytem ang proyektong ito.")

    st.metric(label="PROJECT TOTAL COST", value=f"₱ {grand_total:,.2f}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👁️ Open Layout Preview & Download Suite", use_container_width=True, type="primary"):
            st.session_state.page_view_mode = "print_preview"
            st.rerun()
    with col2:
        if st.button("✏️ Edit POW Record / Update Items", use_container_width=True):
            trigger_edit_modal_dialog(pow_id, project_name, location, associated_items)
    with col3:
        if st.button("❌ Delete Entire POW", use_container_width=True, type="secondary"):
            st.session_state.confirm_delete_id = pow_id

    if "confirm_delete_id" in st.session_state and st.session_state.confirm_delete_id == pow_id:
        st.error(f"⚠️ **KUMPIRMASYON:** Sigurado ka bang buburahin ang buong proyekto?")
        c_del1, c_del2 = st.columns(2)
        with c_del1:
            if st.button("Oo, Burahin", type="primary", use_container_width=True):
                if db.delete_pow_from_sql(pow_id):
                    st.success("Record deleted.")
                    del st.session_state.confirm_delete_id
                    st.rerun()
        with c_del2:
            if st.button("I-cancel", use_container_width=True):
                del st.session_state.confirm_delete_id
                st.rerun()

@st.dialog("✏️ EDIT MODE - Update POW Record", width="large")
def trigger_edit_modal_dialog(pow_id, current_name, current_location, associated_items):
    st.markdown("### 🏢 Details of POW")
    new_name = st.text_input("Project Title / Name:", value=current_name)
    new_loc = st.text_input("Project Location:", value=current_location)

    edit_rows = [{"QTY": float(i[0]), "UNIT": str(i[1]), "ITEM DESCRIPTION": str(i[2]), "UNIT PRICE": float(i[3]), "ORIGINAL NAME": str(i[2])} for i in associated_items]
    df_editable = pd.DataFrame(edit_rows)
    edited_df = st.data_editor(df_editable, num_rows="dynamic", use_container_width=True)

    if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True):
        final_items = []
        for index, row in edited_df.iterrows():
            final_items.append((float(row["QTY"]), str(row["UNIT"]).upper(), str(row["ITEM DESCRIPTION"]).strip(), float(row["UNIT PRICE"])))
        
        success_main = db.update_project_main_details(pow_id, new_name.strip().title(), new_loc.strip().title())
        success_items = db.update_project_items_batch(pow_id, final_items)
        if success_main and success_items:
            st.success("Database Updated Successfully!")
            st.rerun()

# ==============================================================================
# SECTION 3: EXCEL PREVIEW GENERATOR (Dating hiwalay na preview_module.py)
# ==============================================================================
def render_excel_preview_module():
    st.markdown("## 📊 POW Print Preview Layout")
    st.info("Ito ang pormal na structural print rendering engine ng iyong POW System.")
    # Dito pwedeng ilagay ang openpyxl formatting script mo kung kinakailangan

# ==============================================================================
# SECTION 4: MAIN DASHBOARD ROUTER CONTROLLER
# ==============================================================================
def show_dashboard():
    st.sidebar.markdown(f"### 👤 User: **{st.session_state.username.upper()}**")
    st.sidebar.caption(f"Role Profile: {st.session_state.user_role.upper()}")
    st.sidebar.write("---")
    
    menu_choice = st.sidebar.radio("🗂️ Navigation Menu", ["Dashboard & POW List", "Create New POW (Form)"])
    
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Logout Account", type="secondary", use_container_width=True):
        st.session_state.page = 'login'
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.page_view_mode = 'table_view'
        st.rerun()

    if menu_choice == "Dashboard & POW List":
        if st.session_state.page_view_mode == "print_preview":
            if st.button("⬅️ Back to Table View", type="secondary"):
                st.session_state.page_view_mode = "table_view"
                st.rerun()
            render_excel_preview_module()
        else:
            render_preview_pow_module()
    elif menu_choice == "Create New POW (Form)":
        st.subheader("➕ Create New Program of Work")
        st.info("Form configuration details map layer section.")

# --- CORE RENDER GATE ---
if st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'dashboard':
    show_dashboard()
