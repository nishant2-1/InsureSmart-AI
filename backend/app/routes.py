from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.repositories import user_repository, policy_repository, chat_history_repository
from app.ai_service import get_policy_advice

# Blueprints
core_bp = Blueprint('core', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
policy_bp = Blueprint('policy', __name__, url_prefix='/api/policies')
ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


def _get_current_user_id():
    # JWT identity is stored as string for compatibility with strict JWT validators.
    return int(get_jwt_identity())


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
    data = request.get_json() or {}
    
    if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if user_repository.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409

    user = user_repository.create_user(
        email=data['email'],
        full_name=data['full_name'],
        password=data['password']
    )
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = user_repository.get_by_email(data['email'])

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = _get_current_user_id()
    user = user_repository.get_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# Policy Routes
@policy_bp.route('', methods=['GET'])
@jwt_required()
def get_policies():
    user_id = _get_current_user_id()
    policies = policy_repository.list_for_user(user_id)
    
    return jsonify([policy.to_dict() for policy in policies]), 200


@policy_bp.route('', methods=['POST'])
@jwt_required()
def create_policy():
    user_id = _get_current_user_id()
    data = request.get_json() or {}
    
    required_fields = ['policy_type', 'coverage_amount', 'monthly_premium']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    policy = policy_repository.create_policy(user_id, data)
    
    return jsonify({'message': 'Policy created', 'policy': policy.to_dict()}), 201


@policy_bp.route('/<int:policy_id>', methods=['GET'])
@jwt_required()
def get_policy(policy_id):
    user_id = _get_current_user_id()
    policy = policy_repository.get_for_user(policy_id, user_id)
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    return jsonify(policy.to_dict()), 200


# Claims Routes (under policies as they're related)
@policy_bp.route('/<int:policy_id>/claims', methods=['GET'])
@jwt_required()
def get_claims(policy_id):
    user_id = _get_current_user_id()
    policy = policy_repository.get_for_user(policy_id, user_id)
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    claims = policy_repository.list_claims_for_policy(policy_id)
    return jsonify([claim.to_dict() for claim in claims]), 200


@policy_bp.route('/<int:policy_id>/claims', methods=['POST'])
@jwt_required()
def create_claim(policy_id):
    user_id = _get_current_user_id()
    policy = policy_repository.get_for_user(policy_id, user_id)
    
    if not policy:
        return jsonify({'error': 'Policy not found'}), 404
    
    data = request.get_json() or {}
    
    if not data or not data.get('claim_amount') or not data.get('description'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    claim = policy_repository.create_claim(user_id, policy_id, data)
    
    return jsonify({'message': 'Claim submitted', 'claim': claim.to_dict()}), 201


# AI Routes
@ai_bp.route('/policy-advisor', methods=['POST'])
@jwt_required()
def policy_advisor():
    user_id = _get_current_user_id()
    data = request.get_json() or {}
    user_input = data.get('user_input', '').strip()

    if not user_input:
        return jsonify({'error': 'user_input is required'}), 400

    advisor_result = get_policy_advice(user_input)

    chat_entry = chat_history_repository.create_entry(
        user_id=user_id,
        user_prompt=user_input,
        ai_summary=advisor_result['summary'],
        recommended_policy_name=advisor_result.get('recommended_policy_name')
    )

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
    user_id = _get_current_user_id()
    history_rows = chat_history_repository.list_recent_for_user(user_id, limit=20)

    return jsonify([entry.to_dict() for entry in history_rows]), 200
