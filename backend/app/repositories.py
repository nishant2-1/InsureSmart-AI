from datetime import datetime, timedelta

from app import db
from app.models import ChatHistory, Claim, Policy, User


class UserRepository:
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def create_user(self, email, full_name, password):
        user = User(email=email, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


class PolicyRepository:
    def list_for_user(self, user_id):
        return Policy.query.filter_by(user_id=user_id).all()

    def get_for_user(self, policy_id, user_id):
        return Policy.query.filter_by(id=policy_id, user_id=user_id).first()

    def create_policy(self, user_id, data):
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
        return policy

    def list_claims_for_policy(self, policy_id):
        return Claim.query.filter_by(policy_id=policy_id).all()

    def create_claim(self, user_id, policy_id, data):
        claim = Claim(
            user_id=user_id,
            policy_id=policy_id,
            claim_amount=data['claim_amount'],
            description=data['description']
        )
        db.session.add(claim)
        db.session.commit()
        return claim


class ChatHistoryRepository:
    def create_entry(self, user_id, user_prompt, ai_summary, recommended_policy_name=None):
        entry = ChatHistory(
            user_id=user_id,
            user_prompt=user_prompt,
            ai_summary=ai_summary,
            recommended_policy_name=recommended_policy_name
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    def list_recent_for_user(self, user_id, limit=20):
        return (
            ChatHistory.query
            .filter_by(user_id=user_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
            .all()
        )


user_repository = UserRepository()
policy_repository = PolicyRepository()
chat_history_repository = ChatHistoryRepository()
