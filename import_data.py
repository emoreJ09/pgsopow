import openpyxl
import mysql.connector
import db  # Ginagamit ang connection details mula sa iyong db.py

def refresh_master_items():
    file_name = "mga_materyales.xlsx"  # 👈 Ang saktong pangalan ng Excel file mo, boss!
    
    print("🔄 Hakbang 1: Kumokonekta sa database...")
    try:
        conn = db.get_connection(connect_to_db=True)
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Error sa koneksyon ng database: {e}")
        return

    print("🗑️ Hakbang 2: Nililinis ang lumang laman ng master_items para sa bagong 'n.a' update...")
    try:
        # TRUNCATE ang pinakamabilis at malinis na paraan para burahin ang lumang data
        cursor.execute("TRUNCATE TABLE master_items;")
        conn.commit()
    except Exception as e:
        print(f"❌ Hindi ma-clear ang table: {e}")
        cursor.close()
        conn.close()
        return

    print(f"📂 Hakbang 3: Binabasa ang file na '{file_name}' gamit ang openpyxl...")
    try:
        wb = openpyxl.load_workbook(file_name)
        ws = wb.active
    except FileNotFoundError:
        print(f"❌ Error: Hindi nahanap ang file na '{file_name}'. Siguraduhing magkasama sila ng script na ito sa iisang folder.")
        cursor.close()
        conn.close()
        return

    print("📥 Hakbang 4: Isinusubo na ang mga bagong materyales sa database...")
    insert_query = """
        INSERT INTO master_items (item_name, default_unit, default_price) 
        VALUES (%s, %s, %s)
    """
    
    success_count = 0
    # Babasahin mula Row 2 para lagpasan ang Header ng Excel mo
    for row in ws.iter_rows(min_row=2, values_only=True):
        name = row[0]   # Column A: Pangalan ng Materyales (Dito na pinalitan ng n.a)
        unit = row[1]   # Column B: Unit (e.g., pcs, bags)
        price = row[2]  # Column C: Presyo
        
        # Siguraduhing may laman ang pangalan bago i-insert
        if name:
            # Kung sakaling walang presyo, lagyan ng 0.00 para hindi mag-error ang decimal column
            actual_price = float(price) if price is not None else 0.00
            
            try:
                cursor.execute(insert_query, (name, unit, actual_price))
                success_count += 1
            except Exception as e:
                print(f"⚠️ May lumaktaw na item dahil sa error: {name} ({e})")

    # I-commit o i-save nang tuluyan sa MySQL
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n==========================================================")
    print(f"🎉 TAGUMPAY, BOSS! Natapos na ang pag-import.")
    print(f"✅ {success_count} na mga materyales ang may 'n.a' na ngayon sa master_items table mo!")
    print("==========================================================")

if __name__ == "__main__":
    refresh_master_items()