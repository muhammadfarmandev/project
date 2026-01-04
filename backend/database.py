# Database connection and CRUD operations
# Using pyodbc for SQL Server

import pyodbc
from config import get_connection_string
from datetime import datetime


def get_db_connection():
    """Get database connection using pyodbc"""
    try:
        conn = pyodbc.connect(get_connection_string())
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def log_audit(action, table_name, record_id):
    """Log action to audit log table"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO AuditLog (action, table_name, record_id, action_date)
                VALUES (?, ?, ?, ?)
            """, (action, table_name, record_id, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Audit log error: {e}")
            if conn:
                conn.close()


# Admin CRUD
def get_admin_by_username(username):
    """Get admin by username"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT admin_id, username, password_hash FROM Admin WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {'admin_id': row[0], 'username': row[1], 'password_hash': row[2]}
        except Exception as e:
            print(f"Error getting admin: {e}")
            if conn:
                conn.close()
    return None


# Officer CRUD operations
def get_all_officers():
    """Get all officers"""
    conn = get_db_connection()
    officers = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.officer_id, o.name, o.address, o.badge_no, o.rank, o.contact, o.unit_id, u.unit_name
                FROM Officer o
                LEFT JOIN Unit u ON o.unit_id = u.unit_id
                ORDER BY o.officer_id
            """)
            for row in cursor.fetchall():
                officers.append({
                    'officer_id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'badge_no': row[3],
                    'rank': row[4],
                    'contact': row[5],
                    'unit_id': row[6],
                    'unit_name': row[7]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting officers: {e}")
            if conn:
                conn.close()
    return officers


def get_officer_by_id(officer_id):
    """Get officer by ID"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.officer_id, o.name, o.address, o.badge_no, o.rank, o.contact, o.unit_id, u.unit_name
                FROM Officer o
                LEFT JOIN Unit u ON o.unit_id = u.unit_id
                WHERE o.officer_id = ?
            """, (officer_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    'officer_id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'badge_no': row[3],
                    'rank': row[4],
                    'contact': row[5],
                    'unit_id': row[6],
                    'unit_name': row[7]
                }
        except Exception as e:
            print(f"Error getting officer: {e}")
            if conn:
                conn.close()
    return None


def create_officer(name, address, badge_no, rank, contact, unit_id):
    """Create new officer"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Officer (name, address, badge_no, rank, contact, unit_id)
                OUTPUT INSERTED.officer_id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, address, badge_no, rank, contact, unit_id))
            officer_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'Officer', officer_id)
            conn.close()
            return officer_id
        except Exception as e:
            print(f"Error creating officer: {e}")
            if conn:
                conn.close()
    return None


def update_officer(officer_id, name, address, badge_no, rank, contact, unit_id):
    """Update officer"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Officer 
                SET name = ?, address = ?, badge_no = ?, rank = ?, contact = ?, unit_id = ?
                WHERE officer_id = ?
            """, (name, address, badge_no, rank, contact, unit_id, officer_id))
            conn.commit()
            log_audit('UPDATE', 'Officer', officer_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating officer: {e}")
            if conn:
                conn.close()
    return False


def delete_officer(officer_id):
    """Delete officer"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Officer WHERE officer_id = ?", (officer_id,))
            conn.commit()
            log_audit('DELETE', 'Officer', officer_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting officer: {e}")
            if conn:
                conn.close()
    return False


# Criminal CRUD operations
def get_all_criminals():
    """Get all criminals"""
    conn = get_db_connection()
    criminals = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT criminal_id, name, address, cnic, notes FROM Criminal ORDER BY criminal_id")
            for row in cursor.fetchall():
                criminals.append({
                    'criminal_id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'cnic': row[3],
                    'notes': row[4]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting criminals: {e}")
            if conn:
                conn.close()
    return criminals


def get_criminal_by_id(criminal_id):
    """Get criminal by ID"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT criminal_id, name, address, cnic, notes FROM Criminal WHERE criminal_id = ?", (criminal_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    'criminal_id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'cnic': row[3],
                    'notes': row[4]
                }
        except Exception as e:
            print(f"Error getting criminal: {e}")
            if conn:
                conn.close()
    return None


def create_criminal(name, address, cnic, notes):
    """Create new criminal"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Criminal (name, address, cnic, notes)
                OUTPUT INSERTED.criminal_id
                VALUES (?, ?, ?, ?)
            """, (name, address, cnic, notes))
            criminal_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'Criminal', criminal_id)
            conn.close()
            return criminal_id
        except Exception as e:
            print(f"Error creating criminal: {e}")
            if conn:
                conn.close()
    return None


def update_criminal(criminal_id, name, address, cnic, notes):
    """Update criminal"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Criminal 
                SET name = ?, address = ?, cnic = ?, notes = ?
                WHERE criminal_id = ?
            """, (name, address, cnic, notes, criminal_id))
            conn.commit()
            log_audit('UPDATE', 'Criminal', criminal_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating criminal: {e}")
            if conn:
                conn.close()
    return False


def delete_criminal(criminal_id):
    """Delete criminal"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Criminal WHERE criminal_id = ?", (criminal_id,))
            conn.commit()
            log_audit('DELETE', 'Criminal', criminal_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting criminal: {e}")
            if conn:
                conn.close()
    return False


# Case CRUD operations
def get_all_cases():
    """Get all cases"""
    conn = get_db_connection()
    cases = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.case_id, c.case_number, c.title, c.description, c.filed_date,
                       c.filed_by, o.name as officer_name, c.suspect_id, cr.name as suspect_name, c.status
                FROM [Case] c
                LEFT JOIN Officer o ON c.filed_by = o.officer_id
                LEFT JOIN Criminal cr ON c.suspect_id = cr.criminal_id
                ORDER BY c.case_id DESC
            """)
            for row in cursor.fetchall():
                cases.append({
                    'case_id': row[0],
                    'case_number': row[1],
                    'title': row[2],
                    'description': row[3],
                    'filed_date': str(row[4]) if row[4] else None,
                    'filed_by': row[5],
                    'officer_name': row[6],
                    'suspect_id': row[7],
                    'suspect_name': row[8],
                    'status': row[9]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting cases: {e}")
            if conn:
                conn.close()
    return cases


def get_case_by_id(case_id):
    """Get case by ID"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.case_id, c.case_number, c.title, c.description, c.filed_date,
                       c.filed_by, o.name as officer_name, c.suspect_id, cr.name as suspect_name, c.status
                FROM [Case] c
                LEFT JOIN Officer o ON c.filed_by = o.officer_id
                LEFT JOIN Criminal cr ON c.suspect_id = cr.criminal_id
                WHERE c.case_id = ?
            """, (case_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    'case_id': row[0],
                    'case_number': row[1],
                    'title': row[2],
                    'description': row[3],
                    'filed_date': str(row[4]) if row[4] else None,
                    'filed_by': row[5],
                    'officer_name': row[6],
                    'suspect_id': row[7],
                    'suspect_name': row[8],
                    'status': row[9]
                }
        except Exception as e:
            print(f"Error getting case: {e}")
            if conn:
                conn.close()
    return None


def create_case(case_number, title, description, filed_date, filed_by, suspect_id, status):
    """Create new case"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO [Case] (case_number, title, description, filed_date, filed_by, suspect_id, status)
                OUTPUT INSERTED.case_id
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (case_number, title, description, filed_date, filed_by, suspect_id, status))
            case_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'Case', case_id)
            conn.close()
            return case_id
        except Exception as e:
            print(f"Error creating case: {e}")
            if conn:
                conn.close()
    return None


def update_case(case_id, case_number, title, description, filed_date, filed_by, suspect_id, status):
    """Update case"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE [Case]
                SET case_number = ?, title = ?, description = ?, filed_date = ?,
                    filed_by = ?, suspect_id = ?, status = ?
                WHERE case_id = ?
            """, (case_number, title, description, filed_date, filed_by, suspect_id, status, case_id))
            conn.commit()
            log_audit('UPDATE', 'Case', case_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating case: {e}")
            if conn:
                conn.close()
    return False


def delete_case(case_id):
    """Delete case"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM [Case] WHERE case_id = ?", (case_id,))
            conn.commit()
            log_audit('DELETE', 'Case', case_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting case: {e}")
            if conn:
                conn.close()
    return False


# Case Update operations
def get_case_updates(case_id):
    """Get all updates for a case"""
    conn = get_db_connection()
    updates = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cu.update_id, cu.update_text, cu.update_date, cu.updated_by, o.name as officer_name
                FROM CaseUpdate cu
                LEFT JOIN Officer o ON cu.updated_by = o.officer_id
                WHERE cu.case_id = ?
                ORDER BY cu.update_date DESC
            """, (case_id,))
            for row in cursor.fetchall():
                updates.append({
                    'update_id': row[0],
                    'update_text': row[1],
                    'update_date': str(row[2]) if row[2] else None,
                    'updated_by': row[3],
                    'officer_name': row[4]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting case updates: {e}")
            if conn:
                conn.close()
    return updates


def add_case_update(case_id, update_text, updated_by):
    """Add update to case"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO CaseUpdate (case_id, update_text, update_date, updated_by)
                OUTPUT INSERTED.update_id
                VALUES (?, ?, ?, ?)
            """, (case_id, update_text, datetime.now(), updated_by))
            update_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'CaseUpdate', update_id)
            conn.close()
            return update_id
        except Exception as e:
            print(f"Error adding case update: {e}")
            if conn:
                conn.close()
    return None


# Evidence operations
def get_all_evidence():
    """Get all evidence"""
    conn = get_db_connection()
    evidence_list = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.evidence_id, e.case_id, c.case_number, e.file_name, e.description, e.upload_date
                FROM Evidence e
                LEFT JOIN [Case] c ON e.case_id = c.case_id
                ORDER BY e.upload_date DESC
            """)
            for row in cursor.fetchall():
                evidence_list.append({
                    'evidence_id': row[0],
                    'case_id': row[1],
                    'case_number': row[2],
                    'file_name': row[3],
                    'description': row[4],
                    'upload_date': str(row[5]) if row[5] else None
                })
            conn.close()
        except Exception as e:
            print(f"Error getting evidence: {e}")
            if conn:
                conn.close()
    return evidence_list


def get_evidence_by_case(case_id):
    """Get evidence for a specific case"""
    conn = get_db_connection()
    evidence_list = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT evidence_id, case_id, file_name, description, upload_date
                FROM Evidence
                WHERE case_id = ?
                ORDER BY upload_date DESC
            """, (case_id,))
            for row in cursor.fetchall():
                evidence_list.append({
                    'evidence_id': row[0],
                    'case_id': row[1],
                    'file_name': row[2],
                    'description': row[3],
                    'upload_date': str(row[4]) if row[4] else None
                })
            conn.close()
        except Exception as e:
            print(f"Error getting evidence: {e}")
            if conn:
                conn.close()
    return evidence_list


def create_evidence(case_id, file_name, description):
    """Create evidence record"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Evidence (case_id, file_name, description, upload_date)
                OUTPUT INSERTED.evidence_id
                VALUES (?, ?, ?, ?)
            """, (case_id, file_name, description, datetime.now()))
            evidence_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'Evidence', evidence_id)
            conn.close()
            return evidence_id
        except Exception as e:
            print(f"Error creating evidence: {e}")
            if conn:
                conn.close()
    return None


# Duty operations
def get_all_duties():
    """Get all duties"""
    conn = get_db_connection()
    duties = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.duty_id, d.officer_id, o.name as officer_name, d.duty_date, d.duty_time, d.location
                FROM Duty d
                LEFT JOIN Officer o ON d.officer_id = o.officer_id
                ORDER BY d.duty_date DESC, d.duty_time DESC
            """)
            for row in cursor.fetchall():
                duties.append({
                    'duty_id': row[0],
                    'officer_id': row[1],
                    'officer_name': row[2],
                    'duty_date': str(row[3]) if row[3] else None,
                    'duty_time': str(row[4]) if row[4] else None,
                    'location': row[5]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting duties: {e}")
            if conn:
                conn.close()
    return duties


def create_duty(officer_id, duty_date, duty_time, location):
    """Create duty assignment"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Duty (officer_id, duty_date, duty_time, location)
                OUTPUT INSERTED.duty_id
                VALUES (?, ?, ?, ?)
            """, (officer_id, duty_date, duty_time, location))
            duty_id = cursor.fetchone()[0]
            conn.commit()
            log_audit('INSERT', 'Duty', duty_id)
            conn.close()
            return duty_id
        except Exception as e:
            print(f"Error creating duty: {e}")
            if conn:
                conn.close()
    return None


def delete_duty(duty_id):
    """Delete duty"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Duty WHERE duty_id = ?", (duty_id,))
            conn.commit()
            log_audit('DELETE', 'Duty', duty_id)
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting duty: {e}")
            if conn:
                conn.close()
    return False


# Unit operations
def get_all_units():
    """Get all units"""
    conn = get_db_connection()
    units = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT unit_id, unit_name FROM Unit ORDER BY unit_name")
            for row in cursor.fetchall():
                units.append({
                    'unit_id': row[0],
                    'unit_name': row[1]
                })
            conn.close()
        except Exception as e:
            print(f"Error getting units: {e}")
            if conn:
                conn.close()
    return units


# Search operations
def search_cases(query):
    """Search cases by case number or officer name"""
    conn = get_db_connection()
    cases = []
    if conn:
        try:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT c.case_id, c.case_number, c.title, c.description, c.filed_date,
                       c.filed_by, o.name as officer_name, c.suspect_id, cr.name as suspect_name, c.status
                FROM [Case] c
                LEFT JOIN Officer o ON c.filed_by = o.officer_id
                LEFT JOIN Criminal cr ON c.suspect_id = cr.criminal_id
                WHERE c.case_number LIKE ? OR o.name LIKE ? OR c.title LIKE ?
                ORDER BY c.case_id DESC
            """, (search_term, search_term, search_term))
            for row in cursor.fetchall():
                cases.append({
                    'case_id': row[0],
                    'case_number': row[1],
                    'title': row[2],
                    'description': row[3],
                    'filed_date': str(row[4]) if row[4] else None,
                    'filed_by': row[5],
                    'officer_name': row[6],
                    'suspect_id': row[7],
                    'suspect_name': row[8],
                    'status': row[9]
                })
            conn.close()
        except Exception as e:
            print(f"Error searching cases: {e}")
            if conn:
                conn.close()
    return cases


def search_criminals(query):
    """Search criminals by name or CNIC"""
    conn = get_db_connection()
    criminals = []
    if conn:
        try:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT criminal_id, name, address, cnic, notes
                FROM Criminal
                WHERE name LIKE ? OR cnic LIKE ?
                ORDER BY criminal_id
            """, (search_term, search_term))
            for row in cursor.fetchall():
                criminals.append({
                    'criminal_id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'cnic': row[3],
                    'notes': row[4]
                })
            conn.close()
        except Exception as e:
            print(f"Error searching criminals: {e}")
            if conn:
                conn.close()
    return criminals


# Audit log
def get_audit_logs(limit=100):
    """Get audit logs"""
    conn = get_db_connection()
    logs = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT log_id, action, table_name, record_id, action_date
                FROM AuditLog
                ORDER BY action_date DESC
            """)
            for row in cursor.fetchall():
                logs.append({
                    'log_id': row[0],
                    'action': row[1],
                    'table_name': row[2],
                    'record_id': row[3],
                    'action_date': str(row[4]) if row[4] else None
                })
            conn.close()
        except Exception as e:
            print(f"Error getting audit logs: {e}")
            if conn:
                conn.close()
    return logs[:limit]

