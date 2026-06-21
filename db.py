import mysql.connector
from mysql.connector import Error

# ==============================================================================
# INAYOS: Live Cloud Database Configuration (Aiven MySQL Server)
# ==============================================================================
SERVER_CONFIG = {
    'host': 'mysql-d7c52b2-pgsocap-a101.i.aivencloud.com',
    'port': 22786,
    'user': 'avnadmin',
    'password': 'AVNS_lqpk9hxa3xlgjFSm0L-',
    'ssl_disabled': False  
}
DB_NAME = 'defaultdb'

def get_connection(connect_to_db=True):
    """Nagbabalik ng koneksyon sa MySQL Cloud Database."""
    try:
        config = SERVER_CONFIG.copy()
        if connect_to_db:
            config['database'] = DB_NAME
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"Unable to establish database connection: {e}")
        return None

def initialize_db():
    """Awtomatikong gagawa ng mga tables sa loob ng defaultdb cloud database kung wala pa."""
    conn = get_connection(connect_to_db=True)
    if conn is None:
        return
        
    try:
        cursor = conn.cursor()
        
        # ---- PANSAMANTALANG PANGLINIS (I-singit ito sa simula ng try block sa initialize_db) ----
        # Buburahin nito ang lahat ng users bukod sa totoong admin para makapag-signup ka ulit fresh!
        cursor.execute("DELETE FROM users WHERE username != 'admin'")
        conn.commit()
        print("🧹 Nalinis na ang mga multong accounts sa Cloud Database!")
        # --------------------------------------------------------------------------------------
        
        # Table 1: Users Table (Kasama na ang 'status' column para sa Admin Approval)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'encoder',
                status VARCHAR(20) DEFAULT 'approved'
            )
        ''')
        
        # Siguraduhing may status column kung luma ang table structure sa cloud
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'approved'")
            conn.commit()
        except Error:
            pass # Ibig sabihin may status column na, skip na natin
        
        # 🔑 INAYOS DITO: Siguraduhing may default admin at laging APPROVED ang status nito
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        user_admin = cursor.fetchone()
        if user_admin is None:
            cursor.execute("INSERT INTO users (username, password, role, status) VALUES ('admin', 'password123', 'admin', 'approved')")
        else:
            # KUNG MERON NANG ADMIN PERO NAKAPENDING SA DATABASE, IPILIT NATIN NA GAWING APPROVED!
            cursor.execute("UPDATE users SET status = 'approved', role = 'admin' WHERE username = 'admin'")
            
        # Maglagay ng default encoder1 para sa testing mo
        cursor.execute("SELECT * FROM users WHERE username = 'encoder1'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password, role, status) VALUES ('encoder1', 'encoder123', 'encoder', 'approved')")
            
        # Table 2: POW Projects Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pow_projects (
                pow_id INT AUTO_INCREMENT PRIMARY KEY,
                project_name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 3: POW Items Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pow_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                pow_id INT NOT NULL,
                qty INT NOT NULL,
                unit VARCHAR(50) NOT NULL,
                item_name VARCHAR(255) NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (pow_id) REFERENCES pow_projects(pow_id) ON DELETE CASCADE
            )
        ''')
        
        # Table 4: Master Items Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(255) UNIQUE NOT NULL,
                default_unit VARCHAR(50) NOT NULL,
                default_price DECIMAL(10, 2) NOT NULL
            )
        ''')
        
        conn.commit()
        print("Cloud Database tables at default accounts ay matagumpay na nailikha/na-update!")
            
    except Error as e:
        print(f"Database Initialization Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def authenticate_user(username, password):
    """Pinapapasok ang user kung TAMA ang credentials at 'approved' ang status (Maliban sa admin)."""
    conn = get_connection(connect_to_db=True)
    if conn is None: return None
    try:
        cursor = conn.cursor()
        query = "SELECT password, role, status FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user:
            db_password, role, status = user[0], user[1], user[2]
            
            if password == db_password:
                # Kung admin, laging pasok kahit anong status
                if username == "admin" or role == "admin":
                    return role
                
                # Kung encoder, kailangang 'approved' muna ng admin
                if status == "approved":
                    return role
                else:
                    print(f"Login Denied: {username} is still pending admin approval.")
                    return "pending" 
                    
        return None
    except Error as e:
        print(f"Auth Error: {e}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def register_user(username, password, role='encoder'):
    """Nagrerehistro ng bagong user ngunit may 'pending' na status para aprubahan ng Admin."""
    conn = get_connection(connect_to_db=True)
    if conn is None: return False, "Database connection error."
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            return False, "Username already exists!(GALING SA CLOUD DATABASE)"
            
        query = "INSERT INTO users (username, password, role, status) VALUES (%s, %s, %s, 'pending')"
        cursor.execute(query, (username, password, role))
        conn.commit()
        return True, "Account submitted! Waiting for Admin Approval."
    except Error as e:
        return False, f"Database Error: {e}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def approve_user_by_id(user_id):
    """Binabago ang status ng user mula 'pending' patungong 'approved'."""
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        query = "UPDATE users SET status = 'approved' WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Approval Error: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def get_all_encoders():
    """Kinukuha ang lahat ng users bukod sa kahit anong admin accounts para sa Approval Panel."""
    conn = get_connection(connect_to_db=True)
    if conn is None: return []
    try:
        cursor = conn.cursor()
        # INAYOS: Sinala natin pareho ang username at role para sure na ENCODERS lang ang lalabas
        query = """
            SELECT id, username, role, status 
            FROM users 
            WHERE LOWER(username) NOT LIKE '%admin%' 
              AND LOWER(role) != 'admin'
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def delete_user_by_id(user_id, username):
    """Inayos: Kumokonekta na rin sa Aiven Cloud Server para burahin ang user."""
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()

        # 1. Burahin muna sa tbl_user kung may table ka na ganito sa cloud db mo
        try:
            query_logs = "DELETE FROM tbl_user WHERE user_id = %s OR username = %s" 
            cursor.execute(query_logs, (user_id, username))
        except Error:
            pass # Kung walang ganitong table sa cloud mo, dedmahin lang

        # 2. Burahin sa users table sa cloud db
        query_user = "DELETE FROM users WHERE id = %s"
        cursor.execute(query_user, (user_id,))

        conn.commit()
        print(f"Mga naburang rows sa cloud: {cursor.rowcount}") 
        return True
    except Error as err:
        print(f"Cloud Database Delete Error: {err}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

# ==============================================================================
# MGA POW TRANSACTION AT UTILITY FUNCTIONS (HINDI GALAWIN)
# ==============================================================================
def save_pow_to_sql(project_name, location, items_list):
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        project_query = "INSERT INTO pow_projects (project_name, location) VALUES (%s, %s)"
        cursor.execute(project_query, (project_name, location))
        new_pow_id = cursor.lastrowid
        items_query = "INSERT INTO pow_items (pow_id, qty, unit, item_name, unit_price) VALUES (%s, %s, %s, %s, %s)"
        for item in items_list:
            cursor.execute(items_query, (new_pow_id, item['qty'], item['unit'], item['name'], item['price']))
        conn.commit()
        return True
    except Error as e:
        print(f"Failed to Save POW Transaction {e}")
        conn.rollback()
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def get_project_list():
    conn = get_connection(connect_to_db=True)
    if conn is None: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pow_id, project_name, location FROM pow_projects")
        return cursor.fetchall()
    except Error as e:
        print(f"Unable to fetch project list: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def add_new_master_item(user_role, name, unit, price):
    if user_role != "admin": return False
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO master_items (item_name, default_unit, default_price) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, unit, price))
        conn.commit()
        return True
    except Error as e:
        print(f"Error registering new item: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def get_items_by_project(pow_id):
    conn = get_connection(connect_to_db=True)
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = "SELECT qty, unit, item_name, unit_price FROM pow_items WHERE pow_id = %s"
        cursor.execute(query, (pow_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Unable to fetch items: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def delete_pow_from_sql(pow_id):
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM pow_projects WHERE pow_id = %s"
        cursor.execute(query, (pow_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Unable to delete POW: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def search_master_items(search_text=""):
    conn = get_connection(connect_to_db=True)
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = "SELECT item_name, default_unit, default_price FROM master_items WHERE item_name LIKE %s LIMIT 25"
        cursor.execute(query, (f"%{search_text}%",))
        return cursor.fetchall()
    except Error as e:
        print(f"Unable to fetch search results: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def get_project_details(pow_id):
    conn = get_connection(connect_to_db=True)
    if conn is None: return None
    try:
        cursor = conn.cursor()
        query = "SELECT project_name, location FROM pow_projects WHERE pow_id = %s"
        cursor.execute(query, (pow_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Unable to fetch project details: {e}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def update_project_main_details(pow_id, new_name, new_location):
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        query = "UPDATE pow_projects SET project_name = %s, location = %s WHERE pow_id = %s"
        cursor.execute(query, (new_name, new_location, pow_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Unable to save details: {e}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def update_project_items_batch(pow_id, updated_items_list):
    conn = get_connection(connect_to_db=True)
    if conn is None: return False
    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM pow_items WHERE pow_id = %s"
        cursor.execute(delete_query, (pow_id,))
        insert_query = "INSERT INTO pow_items (pow_id, qty, unit, item_name, unit_price) VALUES (%s, %s, %s, %s, %s)"
        for item in updated_items_list:
            cursor.execute(insert_query, (pow_id, item[0], item[1], item[2], item[3]))
        conn.commit()
        return True
    except Error as e:
        print(f"Batch operation failure: {e}")
        conn.rollback()
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

def get_all_pow_history():
    conn = get_connection(connect_to_db=True)
    if conn is None: return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT p.pow_id, p.project_name, p.location, 
                   COALESCE(SUM(i.qty * i.unit_price), 0.00) AS grand_total, p.created_at 
            FROM pow_projects p
            LEFT JOIN pow_items i ON p.pow_id = i.pow_id
            GROUP BY p.pow_id ORDER BY p.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Unable to fetch history: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()