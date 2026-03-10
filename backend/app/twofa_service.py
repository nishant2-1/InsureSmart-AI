"""
Two-Factor Authentication (2FA) Service using TOTP (Time-based One-Time Password).
Generates QR codes for authenticator apps like Google Authenticator, Authy, Microsoft Authenticator.
"""

import pyotp
import qrcode
import io
import base64


def generate_otp_secret():
    """Generate a random base32 secret for TOTP."""
    return pyotp.random_base32()


def get_totp_uri(email, secret, issuer_name="InsureSmart AI"):
    """
    Generate a provisioning URI for TOTP.
    This URI is used to generate QR codes for authenticator apps.
    """
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name=issuer_name
    )


def generate_qr_code_base64(uri):
    """
    Generate a QR code image from a provisioning URI.
    Returns base64-encoded PNG image for frontend rendering.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"


def verify_totp_token(secret, token):
    """
    Verify a TOTP token against the user's secret.
    Returns True if valid, False otherwise.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)  # Allow 1 time-step tolerance (±30 seconds)
