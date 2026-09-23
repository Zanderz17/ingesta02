import boto3
import mysql.connector
import csv
import os

# Configuración de base de datos MySQL en contenedor
# Estos valores coinciden con los que usaremos al crear el contenedor MySQL
db_host = os.environ.get('DB_HOST', 'mysql-db')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'rootpassword')
db_name = os.environ.get('DB_NAME', 'testdb')
table_name = os.environ.get('TABLE_NAME', 'usuarios')

# Configuración de S3
ficheroUpload = "data_exportada.csv"
# Reemplaza con tu nombre de bucket real si no lo pasas como variable
nombreBucket = os.environ.get('S3_BUCKET', 'san-2026')

print("Conectando a la base de datos MySQL local en Docker...")
try:
    conexion = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conexion.cursor()
    
    print(f"Consultando todos los registros de la tabla {table_name}...")
    cursor.execute(f"SELECT * FROM {table_name}")
    resultados = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    nombres_columnas = [i[0] for i in cursor.description]
    
    print("Escribiendo resultados en CSV...")
    with open(ficheroUpload, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(nombres_columnas)
        escritor_csv.writerows(resultados)
        
    print(f"Exportación a {ficheroUpload} completada.")
    
except mysql.connector.Error as err:
    print(f"Error al conectarse a MySQL: {err}")
    exit(1)
finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")

print("Subiendo archivo a S3...")
s3 = boto3.client('s3')
try:
    s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
    print("Archivo subido exitosamente a S3.")
except Exception as e:
    print(f"Error al subir a S3: {e}")

print("Ingesta completada")
