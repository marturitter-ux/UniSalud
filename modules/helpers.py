import pandas as pd
from database.database import connect, log_activity

def query_df(sql, params=()):
    with connect() as con:
        return pd.read_sql_query(sql, con, params=params)

def patient_options():
    df = query_df("SELECT id, document, full_name FROM patients ORDER BY full_name")
    return {f"{r.full_name} · DNI {r.document}": int(r.id) for r in df.itertuples()}

def add_patient(document, full_name, birth_date, phone, email, address, blood_group, notes, actor):
    with connect() as con:
        con.execute("""INSERT INTO patients(document,full_name,birth_date,phone,email,address,blood_group,notes)
        VALUES(?,?,?,?,?,?,?,?)""", (document,full_name,birth_date,phone,email,address,blood_group,notes))
    log_activity(actor, "Paciente registrado", full_name)

def add_study(patient_id, modality, body_region, study_date, institution, professional, status, report, file_name, actor):
    with connect() as con:
        con.execute("""INSERT INTO studies(patient_id,modality,body_region,study_date,institution,professional,status,report,file_name)
        VALUES(?,?,?,?,?,?,?,?,?)""", (patient_id,modality,body_region,study_date,institution,professional,status,report,file_name))
    log_activity(actor, "Estudio registrado", f"{modality} · paciente ID {patient_id}")

def add_appointment(patient_id, professional, institution, date, time, reason, status, actor):
    with connect() as con:
        con.execute("""INSERT INTO appointments(patient_id,professional,institution,appointment_date,appointment_time,reason,status)
        VALUES(?,?,?,?,?,?,?)""", (patient_id,professional,institution,date,time,reason,status))
    log_activity(actor, "Turno registrado", f"{date} {time}")

def add_professional(name, specialty, registration, email, phone, actor):
    with connect() as con:
        con.execute("INSERT INTO professionals(full_name,specialty,registration,email,phone) VALUES(?,?,?,?,?)",
                    (name,specialty,registration,email,phone))
    log_activity(actor, "Profesional registrado", name)

def add_institution(name, kind, city, address, contact, actor):
    with connect() as con:
        con.execute("INSERT INTO institutions(name,type,city,address,contact) VALUES(?,?,?,?,?)",
                    (name,kind,city,address,contact))
    log_activity(actor, "Institución registrada", name)

def add_consent(patient_id, consent_type, granted_to, date, status, notes, actor):
    with connect() as con:
        con.execute("INSERT INTO consents(patient_id,consent_type,granted_to,consent_date,status,notes) VALUES(?,?,?,?,?,?)",
                    (patient_id,consent_type,granted_to,date,status,notes))
    log_activity(actor, "Consentimiento registrado", consent_type)
