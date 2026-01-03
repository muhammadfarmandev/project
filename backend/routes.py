# Flask routes for NSOS API
# All CRUD operations and endpoints

from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
import database as db
import utils
from datetime import datetime

routes = Blueprint('routes', __name__)


# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function


# Authentication routes
@routes.route('/api/login', methods=['POST'])
def login():
    """Admin login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    admin = db.get_admin_by_username(username)
    
    # Debug: check if admin exists and password verification
    if not admin:
        print(f"Login: Admin '{username}' not found in database")
        return jsonify({'error': 'Invalid credentials'}), 401
    
    print(f"Login: Admin found - ID: {admin['admin_id']}, Username: {admin['username']}")
    print(f"Login: Checking password...")
    
    password_valid = utils.check_password(password, admin['password_hash'])
    print(f"Login: Password valid: {password_valid}")
    
    if password_valid:
        # Set session data
        session['admin_id'] = admin['admin_id']
        session['username'] = admin['username']
        session.permanent = True
        session.modified = True
        
        # Debug: print session after setting
        print(f"Login: Session set - admin_id={session.get('admin_id')}, username={session.get('username')}")
        print(f"Login: Session dict = {dict(session)}")
        print(f"Login: Session permanent = {session.permanent}")
        print(f"Login: Session modified = {session.modified}")
        
        # Create response - Flask will automatically add session cookie to response
        response = jsonify({'message': 'Login successful', 'username': admin['username']})
        
        # Ensure session is saved (this happens automatically when response is returned)
        return response, 200
    else:
        print(f"Login: Password check failed for user '{username}'")
        return jsonify({'error': 'Invalid credentials'}), 401


@routes.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Logout"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@routes.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    # Always return 200, just indicate authentication status
    # Debug: print session contents (remove in production)
    print(f"Check-auth: Session contents: {dict(session)}")
    print(f"Check-auth: admin_id in session: {'admin_id' in session}")
    print(f"Check-auth: Request cookies: {list(request.cookies.keys())}")
    
    if 'admin_id' in session:
        print(f"Check-auth: User authenticated - {session.get('username')}")
        return jsonify({'authenticated': True, 'username': session.get('username')}), 200
    
    print(f"Check-auth: User NOT authenticated - no admin_id in session")
    return jsonify({'authenticated': False, 'debug': 'No admin_id in session'}), 200


# Officer routes
@routes.route('/api/officers', methods=['GET'])
@login_required
def get_officers():
    """Get all officers"""
    officers = db.get_all_officers()
    return jsonify(officers), 200


@routes.route('/api/officers/<int:officer_id>', methods=['GET'])
@login_required
def get_officer(officer_id):
    """Get officer by ID"""
    officer = db.get_officer_by_id(officer_id)
    if officer:
        return jsonify(officer), 200
    return jsonify({'error': 'Officer not found'}), 404


@routes.route('/api/officers', methods=['POST'])
@login_required
def create_officer():
    """Create new officer"""
    data = request.get_json()
    name = data.get('name')
    address = data.get('address', '')
    badge_no = data.get('badge_no')
    rank = data.get('rank', '')
    contact = data.get('contact', '')
    unit_id = data.get('unit_id')
    
    if not name or not badge_no:
        return jsonify({'error': 'Name and badge number required'}), 400
    
    officer_id = db.create_officer(name, address, badge_no, rank, contact, unit_id)
    if officer_id:
        return jsonify({'message': 'Officer created', 'officer_id': officer_id}), 201
    return jsonify({'error': 'Failed to create officer'}), 500


@routes.route('/api/officers/<int:officer_id>', methods=['PUT'])
@login_required
def update_officer(officer_id):
    """Update officer"""
    data = request.get_json()
    name = data.get('name')
    address = data.get('address', '')
    badge_no = data.get('badge_no')
    rank = data.get('rank', '')
    contact = data.get('contact', '')
    unit_id = data.get('unit_id')
    
    if not name or not badge_no:
        return jsonify({'error': 'Name and badge number required'}), 400
    
    success = db.update_officer(officer_id, name, address, badge_no, rank, contact, unit_id)
    if success:
        return jsonify({'message': 'Officer updated'}), 200
    return jsonify({'error': 'Failed to update officer'}), 500


@routes.route('/api/officers/<int:officer_id>', methods=['DELETE'])
@login_required
def delete_officer(officer_id):
    """Delete officer"""
    success = db.delete_officer(officer_id)
    if success:
        return jsonify({'message': 'Officer deleted'}), 200
    return jsonify({'error': 'Failed to delete officer'}), 500


# Criminal routes
@routes.route('/api/criminals', methods=['GET'])
@login_required
def get_criminals():
    """Get all criminals"""
    criminals = db.get_all_criminals()
    return jsonify(criminals), 200


@routes.route('/api/criminals/<int:criminal_id>', methods=['GET'])
@login_required
def get_criminal(criminal_id):
    """Get criminal by ID"""
    criminal = db.get_criminal_by_id(criminal_id)
    if criminal:
        return jsonify(criminal), 200
    return jsonify({'error': 'Criminal not found'}), 404


@routes.route('/api/criminals', methods=['POST'])
@login_required
def create_criminal():
    """Create new criminal"""
    data = request.get_json()
    name = data.get('name')
    address = data.get('address', '')
    cnic = data.get('cnic')
    notes = data.get('notes', '')
    
    if not name or not cnic:
        return jsonify({'error': 'Name and CNIC required'}), 400
    
    criminal_id = db.create_criminal(name, address, cnic, notes)
    if criminal_id:
        return jsonify({'message': 'Criminal created', 'criminal_id': criminal_id}), 201
    return jsonify({'error': 'Failed to create criminal'}), 500


@routes.route('/api/criminals/<int:criminal_id>', methods=['PUT'])
@login_required
def update_criminal(criminal_id):
    """Update criminal"""
    data = request.get_json()
    name = data.get('name')
    address = data.get('address', '')
    cnic = data.get('cnic')
    notes = data.get('notes', '')
    
    if not name or not cnic:
        return jsonify({'error': 'Name and CNIC required'}), 400
    
    success = db.update_criminal(criminal_id, name, address, cnic, notes)
    if success:
        return jsonify({'message': 'Criminal updated'}), 200
    return jsonify({'error': 'Failed to update criminal'}), 500


@routes.route('/api/criminals/<int:criminal_id>', methods=['DELETE'])
@login_required
def delete_criminal(criminal_id):
    """Delete criminal"""
    success = db.delete_criminal(criminal_id)
    if success:
        return jsonify({'message': 'Criminal deleted'}), 200
    return jsonify({'error': 'Failed to delete criminal'}), 500


# Case routes
@routes.route('/api/cases', methods=['GET'])
@login_required
def get_cases():
    """Get all cases"""
    cases = db.get_all_cases()
    return jsonify(cases), 200


@routes.route('/api/cases/<int:case_id>', methods=['GET'])
@login_required
def get_case(case_id):
    """Get case by ID"""
    case = db.get_case_by_id(case_id)
    if case:
        return jsonify(case), 200
    return jsonify({'error': 'Case not found'}), 404


@routes.route('/api/cases', methods=['POST'])
@login_required
def create_case():
    """Create new case"""
    data = request.get_json()
    case_number = data.get('case_number')
    title = data.get('title')
    description = data.get('description', '')
    filed_date = data.get('filed_date')
    filed_by = data.get('filed_by')
    suspect_id = data.get('suspect_id')
    status = data.get('status', 'Open')
    
    if not case_number or not title or not filed_date or not filed_by:
        return jsonify({'error': 'Case number, title, filed date, and filed by are required'}), 400
    
    case_id = db.create_case(case_number, title, description, filed_date, filed_by, suspect_id, status)
    if case_id:
        return jsonify({'message': 'Case created', 'case_id': case_id}), 201
    return jsonify({'error': 'Failed to create case'}), 500


@routes.route('/api/cases/<int:case_id>', methods=['PUT'])
@login_required
def update_case(case_id):
    """Update case"""
    data = request.get_json()
    case_number = data.get('case_number')
    title = data.get('title')
    description = data.get('description', '')
    filed_date = data.get('filed_date')
    filed_by = data.get('filed_by')
    suspect_id = data.get('suspect_id')
    status = data.get('status', 'Open')
    
    if not case_number or not title or not filed_date or not filed_by:
        return jsonify({'error': 'Case number, title, filed date, and filed by are required'}), 400
    
    success = db.update_case(case_id, case_number, title, description, filed_date, filed_by, suspect_id, status)
    if success:
        return jsonify({'message': 'Case updated'}), 200
    return jsonify({'error': 'Failed to update case'}), 500


@routes.route('/api/cases/<int:case_id>', methods=['DELETE'])
@login_required
def delete_case(case_id):
    """Delete case"""
    success = db.delete_case(case_id)
    if success:
        return jsonify({'message': 'Case deleted'}), 200
    return jsonify({'error': 'Failed to delete case'}), 500


# Case update routes
@routes.route('/api/cases/<int:case_id>/updates', methods=['GET'])
@login_required
def get_case_updates(case_id):
    """Get all updates for a case"""
    updates = db.get_case_updates(case_id)
    return jsonify(updates), 200


@routes.route('/api/cases/<int:case_id>/updates', methods=['POST'])
@login_required
def add_case_update(case_id):
    """Add update to case"""
    data = request.get_json()
    update_text = data.get('update_text')
    updated_by = data.get('updated_by')
    
    if not update_text or not updated_by:
        return jsonify({'error': 'Update text and updated by are required'}), 400
    
    update_id = db.add_case_update(case_id, update_text, updated_by)
    if update_id:
        return jsonify({'message': 'Update added', 'update_id': update_id}), 201
    return jsonify({'error': 'Failed to add update'}), 500


# Evidence routes
@routes.route('/api/evidence', methods=['GET'])
@login_required
def get_evidence():
    """Get all evidence"""
    case_id = request.args.get('case_id')
    if case_id:
        evidence = db.get_evidence_by_case(int(case_id))
    else:
        evidence = db.get_all_evidence()
    return jsonify(evidence), 200


@routes.route('/api/evidence', methods=['POST'])
@login_required
def create_evidence():
    """Create evidence with file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    case_id = request.form.get('case_id')
    description = request.form.get('description', '')
    
    if not case_id:
        return jsonify({'error': 'Case ID required'}), 400
    
    filename = utils.save_uploaded_file(file)
    if filename:
        evidence_id = db.create_evidence(int(case_id), filename, description)
        if evidence_id:
            return jsonify({'message': 'Evidence uploaded', 'evidence_id': evidence_id, 'file_name': filename}), 201
        return jsonify({'error': 'Failed to save evidence record'}), 500
    return jsonify({'error': 'Invalid file type'}), 400


# Duty routes
@routes.route('/api/duties', methods=['GET'])
@login_required
def get_duties():
    """Get all duties"""
    duties = db.get_all_duties()
    return jsonify(duties), 200


@routes.route('/api/duties', methods=['POST'])
@login_required
def create_duty():
    """Create duty assignment"""
    data = request.get_json()
    officer_id = data.get('officer_id')
    duty_date = data.get('duty_date')
    duty_time = data.get('duty_time')
    location = data.get('location')
    
    if not officer_id or not duty_date or not duty_time or not location:
        return jsonify({'error': 'All fields required'}), 400
    
    duty_id = db.create_duty(officer_id, duty_date, duty_time, location)
    if duty_id:
        return jsonify({'message': 'Duty assigned', 'duty_id': duty_id}), 201
    return jsonify({'error': 'Failed to assign duty'}), 500


@routes.route('/api/duties/<int:duty_id>', methods=['DELETE'])
@login_required
def delete_duty(duty_id):
    """Delete duty"""
    success = db.delete_duty(duty_id)
    if success:
        return jsonify({'message': 'Duty deleted'}), 200
    return jsonify({'error': 'Failed to delete duty'}), 500


# Unit routes
@routes.route('/api/units', methods=['GET'])
@login_required
def get_units():
    """Get all units"""
    units = db.get_all_units()
    return jsonify(units), 200


# Search routes
@routes.route('/api/search', methods=['GET'])
@login_required
def search():
    """Search cases and criminals"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')  # all, cases, criminals
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    results = {}
    if search_type in ['all', 'cases']:
        results['cases'] = db.search_cases(query)
    if search_type in ['all', 'criminals']:
        results['criminals'] = db.search_criminals(query)
    
    return jsonify(results), 200


# Audit log routes
@routes.route('/api/audit', methods=['GET'])
@login_required
def get_audit_logs():
    """Get audit logs"""
    limit = request.args.get('limit', 100, type=int)
    logs = db.get_audit_logs(limit)
    return jsonify(logs), 200

