import openpyxl
from mysql.connector import Error
import db  # 🔥 KAKANTAHIN NITO ANG CLOUD CONFIGS MO MULA SA DB.PY

def import_from_excel(excel_file_path):
    try:
        # 1. Gagamitin ang get_connection() mula sa db.py na naka-konekta sa Aiven Cloud
        print("Kumokonekta sa Aiven Cloud Database...")
        connection = db.get_connection(connect_to_db=True)
        
        if connection is not None and connection.is_connected():
            cursor = connection.cursor()
            
            # Linisin muna ang lumang talahanayan sa cloud bago mag-import ng bago
            print("Nililinis ang master_items table...")
            cursor.execute("TRUNCATE TABLE master_items;")
            
            # 2. Buksan ang Excel File gamit ang Relative Path
            wb = openpyxl.load_workbook(excel_file_path)
            sheet = wb.active # Kukunin ang unang sheet
            
            print("Nagsisimula nang mag-import ng mga totoong materyales mula sa Excel...")
            
            # 3. I-loop ang bawat row sa Excel (Magsimula sa Row 2 dahil may header ang Excel mo)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Siguraduhing may laman ang unang cell (Item Name) bago ipasok sa database
                if row[0] is not None:
                    name = str(row[0]).strip()
                    unit = str(row[1]).strip() if row[1] is not None else "pc"
                    price = float(row[2]) if row[2] is not None else 0.00
                    
                    sql_query = """INSERT INTO master_items (item_name, default_unit, default_price) 
                                   VALUES (%s, %s, %s)"""
                    cursor.execute(sql_query, (name, unit, price))
            
            connection.commit()
            print("=========================================================")
            print("🎉 TAGUMPAY! Ang iyong real list of materials ay nasa Cloud na!")
            print("=========================================================")

    except Error as e:
        print(f"❌ Nagka-error sa Database Connection: {e}")
    except FileNotFoundError:
        print(f"❌ Error: Hindi mahanap ang file na '{excel_file_path}' sa folder na ito. Paki-check ang spelling.")
    except Exception as e:
        print(f"❌ Nagka-error habang binabasa ang Excel: {e}")
    finally:
        if 'connection' in locals() and connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

# Siguraduhing ang 'master_items.xlsx' ay nasa loob mismo ng E:\jrm folder!
import_from_excel("master_items.xlsx")