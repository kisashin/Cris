import pyodbc

def get_db_connection():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-6S05TRV\\SQLEXPRESS;"
        "DATABASE=ProyectoUsuarios;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)

# if __name__ == '__main__':
#     try:
#         conn = get_db_connection()
#         print("Conexión exitosa a SQL Server.")
#         conn.close()
#     except Exception as e:
#         print("Error de conexión:", e)

