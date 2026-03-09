from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Policy, Claim, ChatHistory
from app.ai_service import get_policy_advice
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
@jwt_required()
def policy_advisor():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    user_input = data.get('user_input', '').strip()

    if not user_input:
        return jsonify({'error': 'user_input is required'}), 400

    advisor_result = get_policy_advice(user_input)

    chat_entry = ChatHistory(
        user_id=user_id,
        user_prompt=user_input,
        ai_summary=advisor_result['summary'],
        recommended_policy_name=advisor_result.get('recommended_policy_name')
    )
    db.session.add(chat_entry)
    db.session.commit()

    recommendations = advisor_result.get('recommendations', [])
    return jsonify({
        'message': advisor_result['summary'],
        'reason': advisor_result.get('reason', ''),
        'provider': advisor_result.get('provider', 'fallback'),
        'recommendations': recommendations,
        'chat_entry': chat_entry.to_dict()
    }), 200


@ai_bp.route('/history', methods=['GET'])
@jwt_required()
def get_advisor_history():
    user_id = get_jwt_identity()
    history_rows = (
        ChatHistory.query
        .filter_by(user_id=user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(20)
        .all()
    )

    return jsonify([entry.to_dict() for entry in history_rows]), 200
