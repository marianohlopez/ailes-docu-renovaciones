import pandas as pd
from datetime import datetime, date
import os
from dotenv import load_dotenv
import yagmail

load_dotenv()

MAIL_AUTOR = os.getenv("MAIL_AUTOR")
APP_GMAIL_PASS = os.getenv("APP_GMAIL_PASS")
MAIL_DESTINO = os.getenv("MAIL_DESTINO")

today = datetime.now()

def tranform_data(rows, cursor):

  columns = [col[0] for col in cursor.description]  # nombres de columnas SQL
  df = pd.DataFrame(rows, columns=columns)

  date_cols = ['cred_dni', 'cred_cud', 'cred_os', 'rhc', 'car', 'ord_med', 'otros']

  for col in date_cols:
      df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce').dt.strftime('%d/%m/%Y')

  df['prestacion_renueva_prox'] = df['prestacion_renueva_prox'].replace('s/d', '-')

  return df

def export_excel(data_docs):
    
  # Hoja 1 - Renovaciones

  headers_renov = ["PRESTACION_ID", "AÑO", "TIPO", "TERAPIAS", "ALUMNO_ID", "APELLIDO", 
                      "NOMBRE", "MAIL", "DNI", "TURNO", "RENUEVA", "OS", "LOCALIDAD", "PARTIDO", 
                      "CRED_DNI", "CUD", "CRED_OS", "RHC", "CAR", "ORD_MED", "OTROS", "ESTADO"]
  
 # Aplicar los headers en mayúsculas al exportar
  data_docs.columns = headers_renov

  today = date.today()
  file_name = f"Renovacion_2026_{today.strftime('%Y-%m-%d')}.xlsx"

  data_docs.to_excel(file_name, index=False, sheet_name="Renovación 2026")

  print(f"Archivo Excel generado: {file_name}")
  return file_name

def enviar_correo(nombre_archivo):
  try:
    yag = yagmail.SMTP(MAIL_AUTOR, APP_GMAIL_PASS)
    yag.send(
      to=MAIL_DESTINO,
      subject="Reporte de renovaciones 2026",
      contents= """Buenos días, se adjunta el reporte de renovaciones para el area de Documentación.
              \nSaludos,\nMariano López - Ailes Inclusión.""",
      attachments=nombre_archivo
    )
    print("Correo enviado correctamente.")
  except Exception as e:
    print("Error al enviar el correo:", e)