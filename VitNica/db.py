import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=KENETH_GOMEZ\\SQLEXPRESS;"
            "DATABASE=VetNica_Resour;"
            "Trusted_Connection=yes;"
        )
        print("Conexion exitosa")
        return conn
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    get_connection()