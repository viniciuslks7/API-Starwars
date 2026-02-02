"""Firebase Admin SDK initialization and JWT verification."""

import os
from functools import lru_cache
from typing import Optional

from src.config import get_settings

# Firebase Admin SDK will be imported conditionally
_firebase_admin = None
_firebase_auth = None


def _get_firebase():
    """Lazily import and initialize Firebase Admin SDK."""
    global _firebase_admin, _firebase_auth

    if _firebase_admin is None:
        try:
            import firebase_admin
            from firebase_admin import auth, credentials

            _firebase_admin = firebase_admin
            _firebase_auth = auth

            # Check if already initialized
            try:
                firebase_admin.get_app()
            except ValueError:
                # Not initialized, initialize now
                settings = get_settings()

                if settings.firebase_credentials_path and os.path.exists(
                    settings.firebase_credentials_path
                ):
                    # Use service account credentials
                    cred = credentials.Certificate(settings.firebase_credentials_path)
                    firebase_admin.initialize_app(cred)
                elif settings.gcp_project_id:
                    # Use Application Default Credentials (for GCP environments)
                    firebase_admin.initialize_app(options={"projectId": settings.gcp_project_id})
                else:
                    # No credentials available - will skip auth
                    return None, None

        except ImportError:
            # Firebase Admin SDK not installed
            return None, None

    return _firebase_admin, _firebase_auth


class FirebaseAuthError(Exception):
    """Firebase authentication error."""

    def __init__(self, message: str, code: str = "UNAUTHORIZED"):
        self.message = message
        self.code = code
        super().__init__(message)


class TokenPayload:
    """Decoded JWT token payload."""

    def __init__(self, uid: str, email: Optional[str], claims: dict):
        self.uid = uid
        self.email = email
        self.claims = claims
        self.is_admin = claims.get("admin", False)

    def __repr__(self) -> str:
        return f"TokenPayload(uid={self.uid}, email={self.email})"


def verify_firebase_token(token: str) -> TokenPayload:
    """
    Verify a Firebase ID token.

    Args:
        token: Firebase ID token (JWT)

    Returns:
        TokenPayload with user information

    Raises:
        FirebaseAuthError: If token is invalid or expired
    """
    _, auth_module = _get_firebase()

    if auth_module is None:
        raise FirebaseAuthError("Firebase Admin SDK not configured", "FIREBASE_NOT_CONFIGURED")

    try:
        decoded_token = auth_module.verify_id_token(token)
        return TokenPayload(
            uid=decoded_token["uid"],
            email=decoded_token.get("email"),
            claims=decoded_token,
        )
    except auth_module.ExpiredIdTokenError:
        raise FirebaseAuthError("Token expired", "TOKEN_EXPIRED")
    except auth_module.RevokedIdTokenError:
        raise FirebaseAuthError("Token revoked", "TOKEN_REVOKED")
    except auth_module.InvalidIdTokenError:
        raise FirebaseAuthError("Invalid token", "INVALID_TOKEN")
    except Exception as e:
        raise FirebaseAuthError(f"Token verification failed: {str(e)}", "VERIFICATION_FAILED")


def is_firebase_configured() -> bool:
    """Check if Firebase is properly configured."""
    admin, auth = _get_firebase()
    return admin is not None and auth is not None
