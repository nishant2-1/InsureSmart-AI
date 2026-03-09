"""Seed script for local recruiter/demo setup.

Usage:
    cd backend
    python seed.py
"""

from app import create_app, db
from app.models import Policy, User


def seed_database():
    app = create_app()

    with app.app_context():
        db.create_all()

        demo_user = User.query.filter_by(email='demo@insuresmart.ai').first()
        if not demo_user:
            demo_user = User(email='demo@insuresmart.ai', full_name='Demo User')
            demo_user.set_password('DemoPass123!')
            db.session.add(demo_user)
            db.session.commit()

        existing_policies = Policy.query.filter_by(user_id=demo_user.id).count()
        if existing_policies == 0:
            sample_policies = [
                {
                    'policy_type': 'Health',
                    'coverage_amount': 150000,
                    'monthly_premium': 45,
                    'description': 'Standard family health cover',
                    'status': 'active'
                },
                {
                    'policy_type': 'Life',
                    'coverage_amount': 300000,
                    'monthly_premium': 40,
                    'description': 'Long-term life protection plan',
                    'status': 'active'
                },
                {
                    'policy_type': 'Auto',
                    'coverage_amount': 120000,
                    'monthly_premium': 28,
                    'description': 'Comprehensive vehicle insurance',
                    'status': 'active'
                },
                {
                    'policy_type': 'Home',
                    'coverage_amount': 350000,
                    'monthly_premium': 55,
                    'description': 'Property and contents protection',
                    'status': 'active'
                },
                {
                    'policy_type': 'Travel',
                    'coverage_amount': 80000,
                    'monthly_premium': 19,
                    'description': 'Multi-trip international travel cover',
                    'status': 'active'
                },
            ]

            for row in sample_policies:
                db.session.add(
                    Policy(
                        user_id=demo_user.id,
                        policy_type=row['policy_type'],
                        coverage_amount=row['coverage_amount'],
                        monthly_premium=row['monthly_premium'],
                        description=row['description'],
                        status=row['status'],
                    )
                )

            db.session.commit()
            print('Seed complete: created demo user and 5 sample policies.')
        else:
            print('Seed skipped: demo policies already exist.')


if __name__ == '__main__':
    seed_database()
