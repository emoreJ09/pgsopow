import db
from mysql.connector import Error

def add_role_column():
    print("Kumokonekta sa Aiven Cloud para i-update ang table...")
    conn = db.get_connection(connect_to_db=True)
    if conn is None:
        return
        
    try:
        cursor = conn.cursor()
        # Utusan ang MySQL na isingit ang 'role' column sa kasalukuyang users table
        print("Idinaragdag ang 'role' column sa users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'encoder';")
        
        # Gawing 'admin' ang kasalukuyang 'admin' account mo doon
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin';")
        
        conn.commit()
        print("=========================================================")
        print("🎉 TAGUMPAY! Matagumpay na naidagdag ang 'role' column!")
        print("=========================================================")
        
    except Error as e:
        print(f"❌ Error habang ina-update ang table: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn and conn.is_connected(): conn.close()

if __name__ == '__main__':
    add_role_column()