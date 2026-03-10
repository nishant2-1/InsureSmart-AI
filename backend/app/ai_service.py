import json
import os
import urllib.error
import urllib.request


OFFLINE_MESSAGE = 'The AI advisor is currently offline, please check our manual policy list.'


INSURANCE_POLICIES = [
    {
        'id': 1,
        'name': 'Basic Health',
        'monthly': 30,
        'coverage': 50000,
        'category': 'Health',
        'description': 'Best for individuals with basic medical coverage needs.'
    },
    {
        'id': 2,
        'name': 'Premium Health',
        'monthly': 50,
        'coverage': 200000,
        'category': 'Health',
        'description': 'Comprehensive plan for families and high medical coverage.'
    },
    {
        'id': 3,
        'name': 'Auto Shield',
        'monthly': 25,
        'coverage': 100000,
        'category': 'Auto',
        'description': 'Vehicle protection with roadside support and accident cover.'
    },
    {
        'id': 4,
        'name': 'Home Guard',
        'monthly': 35,
        'coverage': 300000,
        'category': 'Home',
        'description': 'Home and property protection against major incidents.'
    },
    {
        'id': 5,
        'name': 'Travel Secure',
        'monthly': 18,
        'coverage': 75000,
        'category': 'Travel',
        'description': 'Travel cover for medical, cancellations, and baggage delay.'
    }
]


def _keyword_fallback_recommendation(user_input, offline=False):
    text = user_input.lower()
    if 'health' in text or 'medical' in text:
        recommended = [policy for policy in INSURANCE_POLICIES if policy['category'] == 'Health']
    elif 'car' in text or 'auto' in text or 'vehicle' in text:
        recommended = [policy for policy in INSURANCE_POLICIES if policy['category'] == 'Auto']
    elif 'home' in text or 'house' in text or 'property' in text:
        recommended = [policy for policy in INSURANCE_POLICIES if policy['category'] == 'Home']
    elif 'travel' in text or 'trip' in text or 'flight' in text:
        recommended = [policy for policy in INSURANCE_POLICIES if policy['category'] == 'Travel']
    else:
        recommended = INSURANCE_POLICIES[:2]

    top_policy = recommended[0] if recommended else None
    return {
        'summary': OFFLINE_MESSAGE if offline else 'Recommendation generated from local policy rules.',
        'recommended_policy_name': top_policy['name'] if top_policy else None,
        'reason': 'The selected policy best matches your stated insurance intent and coverage needs.',
        'recommendations': recommended[:2],
        'provider': 'fallback'
    }


def _fallback_with_message(user_input, summary, reason):
    result = _keyword_fallback_recommendation(user_input, offline=False)
    result['summary'] = summary
    result['reason'] = reason
    return result


def _parse_ai_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find('{')
        end = content.rfind('}')
        if start >= 0 and end > start:
            return json.loads(content[start:end + 1])
        raise


def get_policy_advice(user_input):
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key or api_key.startswith('your_'):
        return _keyword_fallback_recommendation(user_input, offline=True)

    try:
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

        system_prompt = (
            'You are a professional insurance advisor. Use the provided JSON list of policies to '
            'recommend the best one to the user based on their needs. If no policy fits, explain why politely. '
            'Respond with valid JSON only using this schema: '
            '{"summary": string, "recommended_policy_name": string|null, "reason": string}.'
        )

        payload = {
            'model': model,
            'temperature': 0.2,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f'Policies JSON: {json.dumps(INSURANCE_POLICIES)}'},
                {'role': 'user', 'content': f'User request: {user_input}'}
            ]
        }

        request = urllib.request.Request(
            url='https://api.openai.com/v1/chat/completions',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )

        # Hard timeout prevents UI from hanging on "Consulting...".
        with urllib.request.urlopen(request, timeout=12) as response:
            response_data = json.loads(response.read().decode('utf-8'))

        content = response_data['choices'][0]['message']['content']
        parsed = _parse_ai_json(content)

        policy_name = parsed.get('recommended_policy_name')
        matched = []
        if policy_name:
            matched = [
                policy for policy in INSURANCE_POLICIES
                if policy['name'].lower() == str(policy_name).lower()
            ]

        return {
            'summary': parsed.get('summary', 'Recommendation generated.'),
            'recommended_policy_name': policy_name,
            'reason': parsed.get('reason', ''),
            'recommendations': matched,
            'provider': 'openai'
        }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"OpenAI HTTP error {e.code}: {error_body}")
        if e.code == 429:
            return _fallback_with_message(
                user_input,
                'AI advisor is in fallback mode because OpenAI quota is exhausted.',
                'Top matching policies are shown using local recommendation rules. Add billing or switch to a funded API key to restore live AI answers.'
            )
        if e.code in (401, 403):
            return _fallback_with_message(
                user_input,
                'AI advisor is in fallback mode because the OpenAI key is invalid or unauthorized.',
                'Update OPENAI_API_KEY in backend/.env with a valid key to restore live AI answers.'
            )
        return _keyword_fallback_recommendation(user_input, offline=True)
    except TimeoutError:
        print('OpenAI request timed out after 12s')
        return _keyword_fallback_recommendation(user_input, offline=True)
    except Exception as e:
        import traceback
        print(f"OpenAI error: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # Full traceback for debugging
        return _keyword_fallback_recommendation(user_input, offline=True)
