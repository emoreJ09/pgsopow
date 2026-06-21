import tkinter as tk
from tkinter import messagebox
import db  # Siniguradong naka-import ang database module mo
from modules.pow.preview_pow import PreviewPowModule
from modules.pow.add_pow import AddPowModule 
from modules.pow.list_pow import POWListModule 

class OfficeDashboard(tk.Frame):
    def __init__(self, parent, username, user_role, on_logout):  
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.user_role = user_role  
        self.on_logout = on_logout
        
        self.parent.title("PGSO Management System - Main Dashboard")
        self.parent.state('zoomed')
        
        # --- SIDEBAR FRAME ---
        self.sidebar = tk.Frame(self, bg="#1a365d", width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand_lbl = tk.Label(self.sidebar, text="🏛️PGSO PORTAL", font=("Segoe UI", 13, "bold"), fg="white", bg="#1a365d", pady=25)
        brand_lbl.pack(fill="x")
        
        tk.Frame(self.sidebar, bg="#2a4365", height=1).pack(fill="x", padx=10)

        # MGA MENU BUTTONS
        self.add_menu_btn("➕   ADD POW", self.load_add_pow_module)
        self.add_menu_btn("👁️PREVIEW POW", self.load_preview_pow_module)
        self.add_menu_btn("📋 POW (Program of Work)", self.load_list_pow_module)
        
        tk.Label(self.sidebar, text="DOCUMENTS & FORMS", font=("Segoe UI", 8, "bold"), fg="#718096", bg="#1a365d", anchor="w", padx=20, pady=10).pack(fill="x")
        
        self.add_menu_btn("📋 POW (Program of Work)", self.future_update_notice)
        self.add_menu_btn("🛒 PR (Purchase Request)", self.future_update_notice)
        self.add_menu_btn("🚗 TO (Travel Order)", self.future_update_notice)
        
        tk.Label(self.sidebar, text="SYSTEM", font=("Segoe UI", 8, "bold"), fg="#718096", bg="#1a365d", anchor="w", padx=20, pady=10).pack(fill="x")
        
        self.add_menu_btn("⚙️ SETTINGS", self.future_update_notice)
        
        # 🔥 TAMANG PAG-PASTE NG ADMIN FEATURE RESTRICTION
        if self.user_role == "admin":
            self.add_menu_btn("👥 MANAGE USERS", self.open_user_management)

        btn_logout = tk.Button(self.sidebar, text="🚪 Mag-Logout", font=("Segoe UI", 10, "bold"), bg="#e53e3e", fg="white", bd=0, activebackground="#c53030", activeforeground="white", pady=12, cursor="hand2", command=self.on_logout)
        btn_logout.pack(side="bottom", fill="x", padx=15, pady=20)

        # --- TOPBAR FRAME ---
        self.topbar = tk.Frame(self, bg="white", height=65, bd=1, relief="groove")
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)

        self.section_title = tk.Label(self.topbar, text="Main Dashboard Overview", font=("Segoe UI", 14, "bold"), fg="#2d3748", bg="white")
        self.section_title.pack(side="left", padx=25, pady=15)

        # In-adjust din natin ito para ipakita kung ADMIN o STAFF ang active account
        user_lbl = tk.Label(self.topbar, text=f"Active Account: {self.username} ({self.user_role.upper()})", font=("Segoe UI", 10, "bold"), fg="#4a5568", bg="white")
        user_lbl.pack(side="right", padx=25, pady=20)

        # --- MAIN CONTENT AREA ---
        self.content_area = tk.Frame(self, bg="#f7fafc", padx=30, pady=30)
        self.content_area.pack(side="right", fill="both", expand=True)

        self.show_welcome_message()

    def add_menu_btn(self, text, command):
        """Gumagawa ng Menu Button sa Sidebar nang walang side-effects."""
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10), bg="#1a365d", fg="#e2e8f0", bd=0, activebackground="#2a4365", activeforeground="white", anchor="w", padx=20, pady=12, cursor="hand2", command=command)
        btn.pack(fill="x")

    def show_welcome_message(self):
        welcome_card = tk.LabelFrame(self.content_area, text=" PGSO Portal System Info ", font=("Segoe UI", 10, "bold"), bg="white", padx=25, pady=25, bd=1, relief="solid")
        welcome_card.pack(fill="both", expand=True)

        lbl_title = tk.Label(welcome_card, text="Main Dashboard Workspace", font=("Segoe UI", 18, "bold"), fg="#1a365d", bg="white")
        lbl_title.pack(anchor="w", pady=(0, 15))

        guide_text = (
            "All necessary workspace menus have been successfully initialized on the left-side panel (Sidebar) for your office operations:\n\n"
            "• ADD / EDIT / PREVIEW – For managing all master data records and transactional data entry.\n"
            "• POW / PR / TO – For processing operational program of works, purchase requests, and travel orders.\n"
            "• SETTINGS – For system configuration and environment adjustments.\n\n"
            "These navigation controls are currently armed and fully optimized, standing ready for your backend integration and localized database transaction routines.\n\n"
            "📘 Complete System Guide & Structural Architecture:\n"
            "The data administration module acts as the gatekeeper of your operational storage layer. "
            "Basic inputs are validated locally prior to executing transactions against the integrated database structures."
        )

        lbl_instructions = tk.Label(
            welcome_card, 
            text=guide_text, 
            font=("Segoe UI", 11), 
            fg="#4a5568", 
            bg="white", 
            justify="left", 
            wraplength=700
        )
        lbl_instructions.pack(anchor="w")
        
    def load_add_pow_module(self):
        self.clear_content_area()
        self.section_title.config(text="Encoding Area - Add New POW")
        self.current_active_module = AddPowModule(self.content_area)
        self.current_active_module.pack(fill="both", expand=True)
        
    def load_list_pow_module(self):
        self.clear_content_area()
        self.section_title.config(text="Office Records - POW Masterlist History")
        self.current_active_module = POWListModule(self.content_area)
        self.current_active_module.pack(fill="both", expand=True)
        
    def load_preview_pow_module(self):
        self.clear_content_area()
        self.section_title.config(text="Data Viewer - Preview POW Records")
        self.current_active_module = PreviewPowModule(self.content_area)
        self.current_active_module.pack(fill="both", expand=True)

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def future_update_notice(self):
        messagebox.showinfo("Future Update", "Ang function na ito ay kasalukuyang inihahanda para sa susunod na update.")
        
    def open_edit_pow_modal(self):
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        if not hasattr(self, 'current_selected_pow_id') or not self.current_selected_pow_id:
            messagebox.showwarning("Walang Napili", "Pumili muna ng proyekto sa listahan bago mag-edit, boss.")
            return

        selected_item = self.proj_tree.selection()[0]
        row_values = self.proj_tree.item(selected_item, 'values')
        
        current_project_name = row_values[1]
        current_location = self.proj_tree.item(selected_item, 'tags')[0]
        
        associated_items = db.get_items_by_project(self.current_selected_pow_id)

        edit_win = tk.Toplevel(self)
        edit_win.title("✏️ EDIT MODE - Update POW Record")
        edit_win.geometry("900x650")
        edit_win.configure(bg="#f7fafc")
        edit_win.grab_set()

        top_frame = tk.LabelFrame(edit_win, text=" Mga Pangunahing Detalye ng POW ", font=("Segoe UI", 10, "bold"), bg="#f7fafc", fg="#2d3748", padx=15, pady=10)
        top_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(top_frame, text="Project Title / Name:", font=("Segoe UI", 10), bg="#f7fafc").grid(row=0, column=0, sticky="w", pady=5)
        ent_proj_name = tk.Entry(top_frame, font=("Segoe UI", 11), width=50)
        ent_proj_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ent_proj_name.insert(0, current_project_name) 

        tk.Label(top_frame, text="Project Location:", font=("Segoe UI", 10), bg="#f7fafc").grid(row=1, column=0, sticky="w", pady=5)
        ent_location = tk.Entry(top_frame, font=("Segoe UI", 11), width=50)
        ent_location.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ent_location.insert(0, current_location) 

        items_frame = tk.LabelFrame(edit_win, text=" Listahan ng mga Aytem ", font=("Segoe UI", 10, "bold"), bg="#f7fafc", fg="#2d3748", padx=15, pady=10)
        items_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("qty", "unit", "description", "price")
        edit_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=10)
        edit_tree.heading("qty", text="QTY")
        edit_tree.heading("unit", text="UNIT")
        edit_tree.heading("description", text="ITEM DESCRIPTION")
        edit_tree.heading("price", text="UNIT PRICE")
        
        edit_tree.column("qty", width=70, anchor="center")
        edit_tree.column("unit", width=70, anchor="center")
        edit_tree.column("description", width=450, anchor="w")
        edit_tree.column("price", width=120, anchor="e")
        edit_tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(items_frame, orient="vertical", command=edit_tree.yview)
        sb.pack(fill="y", side="right")
        edit_tree.configure(yscrollcommand=sb.set)

        for item in associated_items:
            edit_tree.insert("", "end", values=(item[0], item[1], item[2], f"{float(item[3]):.2f}"))

        form_frame = tk.Frame(edit_win, bg="#f7fafc")
        form_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(form_frame, text="QTY:", bg="#f7fafc").grid(row=0, column=0, padx=2)
        ent_qty = tk.Entry(form_frame, width=8, font=("Segoe UI", 10))
        ent_qty.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="UNIT:", bg="#f7fafc").grid(row=0, column=2, padx=2)
        ent_unit = tk.Entry(form_frame, width=8, font=("Segoe UI", 10))
        ent_unit.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="DESCRIPTION:", bg="#f7fafc").grid(row=0, column=4, padx=2)
        ent_desc = tk.Entry(form_frame, width=40, font=("Segoe UI", 10))
        ent_desc.grid(row=0, column=5, padx=5)

        tk.Label(form_frame, text="PRICE:", bg="#f7fafc").grid(row=0, column=6, padx=2)
        ent_price = tk.Entry(form_frame, width=12, font=("Segoe UI", 10))
        ent_price.grid(row=0, column=7, padx=5)

        def on_edit_row_select(event):
            sel = edit_tree.selection()
            if not sel: return
            v = edit_tree.item(sel[0], 'values')
            ent_qty.delete(0, tk.END); ent_qty.insert(0, v[0])
            ent_unit.delete(0, tk.END); ent_unit.insert(0, v[1])
            ent_desc.delete(0, tk.END); ent_desc.insert(0, v[2])
            ent_price.delete(0, tk.END); ent_price.insert(0, v[3])

        edit_tree.bind("<<TreeviewSelect>>", on_edit_row_select)

        def apply_row_change():
            sel = edit_tree.selection()
            if not sel:
                messagebox.showwarning("Puna", "Pumili muna ng linya sa table na nais mong baguhin, boss.")
                return
            edit_tree.item(sel[0], values=(ent_qty.get(), ent_unit.get(), ent_desc.get(), ent_price.get()))
            clear_entry_fields()

        def add_new_row():
            if not ent_desc.get():
                messagebox.showwarning("Puna", "Lagyan ng Description ang bagong aytem bago i-add, boss.")
                return
            qty_val = ent_qty.get() if ent_qty.get() else "0"
            price_val = ent_price.get() if ent_price.get() else "0.00"
            edit_tree.insert("", "end", values=(qty_val, ent_unit.get(), ent_desc.get(), price_val))
            clear_entry_fields()

        def clear_entry_fields():
            ent_qty.delete(0, tk.END); ent_unit.delete(0, tk.END)
            ent_desc.delete(0, tk.END); ent_price.delete(0, tk.END)

        btn_apply = tk.Button(form_frame, text="🔄 Update Selected Line", bg="#3182ce", fg="white", font=("Segoe UI", 9, "bold"), command=apply_row_change)
        btn_apply.grid(row=0, column=8, padx=5)

        btn_add_line = tk.Button(form_frame, text="➕ Add as New Line", bg="#38a169", fg="white", font=("Segoe UI", 9, "bold"), command=add_new_row)
        btn_add_line.grid(row=0, column=9, padx=5)

        bottom_frame = tk.Frame(edit_win, bg="#f7fafc")
        bottom_frame.pack(fill="x", side="bottom", pady=15)

        def save_all_updates_to_db():
            new_name = ent_proj_name.get().strip()
            new_loc = ent_location.get().strip()
            
            if not new_name or not new_loc:
                messagebox.showerror("Error", "Hindi pwedeng iwanang blangko ang Project Name at Location, boss.")
                return

            final_items_to_save = []
            for row in edit_tree.get_children():
                vals = edit_tree.item(row, 'values')
                try:
                    q = float(vals[0])
                    u = str(vals[1])
                    d = str(vals[2])
                    p = float(vals[3])
                    final_items_to_save.append((q, u, d, p))
                except ValueError:
                    messagebox.showerror("Format Error", "Siguraduhing tama (numero) ang QTY at PRICE na nilagay mo, boss.")
                    return

            confirm = messagebox.askyesno("Kumpirmasyon", "Sigurado ka ba na nais mong i-overwrite ang mga pagbabago sa proyektong ito sa database?")
            if not confirm: return

            success_main = db.update_project_main_details(self.current_selected_pow_id, new_name, new_loc)
            success_items = db.update_project_items_batch(self.current_selected_pow_id, final_items_to_save)

            if success_main and success_items:
                messagebox.showinfo("Tagumpay", "Matagumpay na na-overwrite at na-update ang buong data, boss!")
                edit_win.destroy() 
                self.load_projects_from_db() 
            else:
                messagebox.showerror("SQL Error", "Muntik na! May error sa database query. Pakisuri kung tugma ang table names.")

        btn_final_save = tk.Button(bottom_frame, text="💾 SAVE ALL CHANGES & OVERWRITE DATABASE", font=("Segoe UI", 11, "bold"), bg="#e53e3e", fg="white", padx=20, pady=8, command=save_all_updates_to_db)
        btn_final_save.pack(anchor="center")

    # 👥 USER MANAGEMENT PANEL (INAYOS ANG INDENTATION AT REFRESH CALL)
    def open_user_management(self):
        """Bubukas ang isang listahan ng mga registered users para pwedeng i-delete o i-approve ng Admin."""
        manage_win = tk.Toplevel(self)
        manage_win.title("Admin - User Management Panel")
        manage_win.geometry("500x450")
        manage_win.configure(bg="#f7fafc")
        manage_win.grab_set()
        
        tk.Label(manage_win, text="REGISTERED ENCODERS LIST", font=("Segoe UI", 12, "bold"), fg="#e53e3e", bg="#f7fafc").pack(pady=15)
        
        list_frame = tk.Frame(manage_win, bg="#f7fafc")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 🟢 Gumawa ng inner function para sa pag-refresh ng listahan
        def refresh_list():
            for widget in list_frame.winfo_children():
                widget.destroy()
                
            users = db.get_all_encoders()
            
            if not users:
                tk.Label(list_frame, text="No other registered users found.", font=("Segoe UI", 10, "italic"), fg="grey", bg="#f7fafc").pack(pady=20)
                return
                
            for user in users:
                # Kinuha ang 4 na records mula sa get_all_encoders()
                u_id, u_name, u_role, u_status = user[0], user[1], user[2], user[3]

                row_frame = tk.Frame(list_frame, pady=5, bg="#f7fafc")
                row_frame.pack(fill="x", anchor="w")

                # Ipakita ang status sa tabi ng pangalan
                user_info = f"👤 {u_name} | Role: {u_role.upper()} | Status: {u_status.upper()}"
                tk.Label(row_frame, text=user_info, font=("Segoe UI", 10), bg="#f7fafc").pack(side="left", padx=5)

                # BUTTON 1: DELETE (Laging andiyan)
                btn_del = tk.Button(
                    row_frame, text="Delete", bg="#e53e3e", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=10, cursor="hand2",
                    command=lambda uid=u_id, uname=u_name: trigger_delete(uid, uname)
                )
                btn_del.pack(side="right", padx=5)

                # BUTTON 2: APPROVE (Lalabas LANG kapag PENDING pa ang user)
                if u_status == "pending":
                    btn_approve = tk.Button(
                        row_frame, text="Approve", bg="#28a745", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=10, cursor="hand2",
                        command=lambda uid=u_id, uname=u_name: trigger_approve(uid, uname)
                    )
                    btn_approve.pack(side="right", padx=5)
                    
                # Divider line para malinis tingnan
                tk.Frame(list_frame, height=1, bg="#E0E0E0").pack(fill="x", pady=5)

        # 🔵 Inner functions para sa delete at approve para madaling ma-refresh ang listahan
        def trigger_delete(uid, uname):
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete user '{uname}'?", parent=manage_win)
            if confirm:
                if db.delete_user_by_id(uid, uname): 
                    messagebox.showinfo("Deleted!", f"User '{uname}' has been successfully erased.", parent=manage_win)
                    refresh_list() # <--- I-re-refresh na nito ang window matapos burahin
                else:
                    messagebox.showerror("Error", "Failed to delete user.", parent=manage_win)
                    
        def trigger_approve(uid, uname):
            confirm = messagebox.askyesno("Confirm Approval", f"Do you want to approve user '{uname}' to fully access the system?", parent=manage_win)
            if confirm:
                if db.approve_user_by_id(uid):
                    messagebox.showinfo("Approved!", f"User '{uname}' is now activated!", parent=manage_win)
                    refresh_list() # <--- I-re-refresh na nito ang window matapos i-approve
                else:
                    messagebox.showerror("Error", "Failed to approve user.", parent=manage_win)

        # 🔥 ITO ANG MAHALAGA NA NAWALA KANINA: Tinawag dapat ang refresh_list() sa dulo para mag-load ang records!
        refresh_list()