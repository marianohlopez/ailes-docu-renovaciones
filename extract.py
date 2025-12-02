def extract_docs_renov(cursor):
  query = """ 
  SELECT
    p.prestacion_id, p.prestacion_anio, p.prestipo_nombre_corto,
    GROUP_CONCAT(DISTINCT t.terapia_nombre ORDER BY t.terapia_nombre SEPARATOR ', ') AS terapias,
    p.prestacion_alumno, p.alumno_apellido, p.alumno_nombre, a.alumno_mail, a.alumno_dni,
    p.prestacion_escuela_turno, p.prestacion_renueva_prox, o.os_nombre, l.localidad_nombre,
    par.partido_nombre,
    MAX(CASE WHEN docs.docalumnobuzon_desc IN ('DNI', 'DNI_FREN') THEN docs.docalumnobuzon_fec_carga END) AS cred_dni,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'CUD' THEN docs.docalumnobuzon_fec_carga END) AS cred_cud,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'CREDENCIAL_OS_ALUMNO' THEN docs.docalumnobuzon_fec_carga END) AS cred_os,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'RESUM_HIST_CLIN' THEN docs.docalumnobuzon_fec_carga END) AS rhc,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'CONST_ALUMNO_REG' THEN docs.docalumnobuzon_fec_carga END) AS car,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'ORDEN_MED' THEN docs.docalumnobuzon_fec_carga END) AS ord_med,
    MAX(CASE WHEN docs.docalumnobuzon_desc = 'OTROS' THEN docs.docalumnobuzon_fec_carga END) AS otros,
    p.prestacion_estado_descrip
  FROM v_prestaciones p
  LEFT JOIN v_terapias t 
    ON p.prestacion_id = t.presterapia_prestacion
  LEFT JOIN v_alumnos a
    ON p.prestacion_alumno = a.alumno_id
  LEFT JOIN v_os o 
    ON p.prestacion_os = o.os_id
  LEFT JOIN v_escuelas e  
    ON p.prestacion_escuela = e.escuela_id
  LEFT JOIN v_localidades l 
    ON e.escuela_localidad = l.localidad_id
  LEFT JOIN v_partidos par 
    ON l.localidad_partido = par.partido_id
  LEFT JOIN v_docs_alumno_buzon_familia docs
    ON a.alumno_id = docs.docalumnobuzon_alumno
      AND docs.ubicacion = 'en-buzon'
  WHERE 
    p.prestacion_anio IN (2025,2026)
    AND p.prestacion_estado IN (0,1)
    AND p.prestacion_alumno != 522
  GROUP BY
    p.prestacion_id,
    p.prestacion_anio,
    p.prestipo_nombre_corto
  ORDER BY
    p.prestacion_id,
    p.prestacion_anio
  """

  cursor.execute(query)
  return cursor.fetchall()