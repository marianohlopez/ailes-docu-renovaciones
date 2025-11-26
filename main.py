from db import connect_db
from extract import extract_docs_renov
from tranform import export_excel, enviar_correo, tranform_data

def main():

  conn = connect_db()
  cursor = conn.cursor()
  data_sql = extract_docs_renov(cursor)
  data_renov = tranform_data(data_sql, cursor)
  archivo = export_excel(data_renov)
  enviar_correo(archivo)

if __name__ == "__main__":
  main()