from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Policy, Claim
from datetime import datetime, timedelta

# Blueprints
core_bp = Blueprint('core', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
policy_bp = Blueprint('policy', __name__, url_prefix='/api/policies')
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@core_bp.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({
        'message': 'Hello from InsureSmart AI backend',
        'service': 'Flask API',
        'status': 'ok'
    }), 200

# Auth Routes
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    user = User(email=data['email'], full_name=data['full_name'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# Policy Routes
@policy_bp.route('', methods=['GET'])
@jwt_required()
def get_policies():
    user_id = get_jwt_identity()
    policies = Policy.query.filter_by(user_id=user_id).all()
    
    return jsonify([policy.to_dict() for policy in policies]), 200


@policy_bp.route('', methods=['POST'])
@jwt_required()
def create_policy():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['policy_type', 'coverage_amount', 'monthly_premium']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    policy = Policy(
        user_id=user_id,
        policy_type=data['policy_type'],
        coverage_amount=data['coverage_amount'],
        monthly_premium=data['monthly_premium'],
        description=data.get('description', ''),
        end_date=datetime.utcnow() + timedelta(days=365)
    )
    
    db.session.add(policy)
    db.session.commit()
    
    return jsonify({'message': 'Policy created', 'policy': policy.to_dict()}), 201


@policy_bp.route('/<int:policy_id>', methods=['GET'])
@jwt_required()
def get_policy(policy_id):
    user_id = get_jwt_identity()
    policy = Policy.query.filter_by(id=policy_id, user_id=user_id).first()
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    return jsonify(policy.to_dict()), 200


# Claims Routes (under policies as they're related)
@policy_bp.route('/<int:policy_id>/claims', methods=['GET'])
@jwt_required()
def get_claims(policy_id):
    user_id = get_jwt_identity()
    policy = Policy.query.filter_by(id=policy_id, user_id=user_id).first()
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    claims = Claim.query.filter_by(policy_id=policy_id).all()
    return jsonify([claim.to_dict() for claim in claims]), 200


@policy_bp.route('/<int:policy_id>/claims', methods=['POST'])
@jwt_required()
def create_claim(policy_id):
    user_id = get_jwt_identity()
    policy = Policy.query.filter_by(id=policy_id, user_id=user_id).first()
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('claim_amount') or not data.get('description'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    claim = Claim(
        user_id=user_id,
        policy_id=policy_id,
        claim_amount=data['claim_amount'],
        description=data['description']
    )
    
    db.session.add(claim)
    db.session.commit()
    
    return jsonify({'message': 'Claim submitted', 'claim': claim.to_dict()}), 201


# AI Routes
@ai_bp.route('/policy-advisor', methods=['POST'])
def policy_advisor():
    data = request.get_json()
    user_input = data.get('user_input', '')
    
    # Predefined policies (in production, use OpenAI API)
    policies_db = [
        {'id': 1, 'name': 'Basic Health', 'monthly':30, 'coverage': 50000, 'description': 'Best for individuals'},
        {'id': 2, 'name': 'Premium Health', 'monthly': 50, 'coverage': 200000, 'description': 'Full family coverage'},
        {'id': 3, 'name': 'Auto Shield', 'monthly': 25, 'coverage': 100000, 'description': 'Car insurance'},
        {'id': 4, 'name': 'Home Guard', 'monthly': 35, 'coverage': 300000, 'description': 'Property protection'},
    ]
    
    # Simple keyword matching (replace with OpenAI later)
    keywords = user_input.lower()
    if 'health' in keywords:
        recommended = [p for p in policies_db if 'health' in p['name'].lower()]
    elif 'car' in keywords or 'auto' in keywords:
        recommended = [p for p in policies_db if 'auto' in p['name'].lower()]
    elif 'home' in keywords or 'house' in keywords:
        recommended = [p for p in policies_db if 'home' in p['name'].lower()]
    else:
        recommended = policies_db
    
    return jsonify({
        'message': f'Found {len(recommended)} policies for you',
        'recommendations': recommended[:2]
    }), 200
