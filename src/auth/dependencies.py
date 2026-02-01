"""Authentication dependencies for FastAPI."""

from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status

from src.auth.firebase import (
    FirebaseAuthError,
    TokenPayload,
    is_firebase_configured,
    verify_firebase_token,
)
from src.config import get_settings

# Simple API key storage (in production, use a database or secrets manager)
# These would be loaded from environment variables
VALID_API_KEYS = {
    "dev-api-key-12345": "development",
    # Add more API keys as needed
}


def extract_token(authorization: str = Header(None)) -> Optional[str]:
    """Extract Bearer token from Authorization header."""
    if authorization is None:
        return None
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]


def verify_api_key(x_api_key: str = Header(None)) -> Optional[str]:
    """Verify API key from X-API-Key header."""
    if x_api_key is None:
        return None
    
    if x_api_key in VALID_API_KEYS:
        return VALID_API_KEYS[x_api_key]
    
    return None


async def get_current_user(
    authorization: str = Header(None),
    x_api_key: str = Header(None),
) -> Optional[TokenPayload]:
    """
    Get the current authenticated user.

    Supports both:
    - Firebase JWT tokens (Authorization: Bearer <token>)
    - API keys (X-API-Key: <key>)

    Returns None if no authentication provided and auth is not required.
    """
    settings = get_settings()
    
    # Try API key first (simpler)
    if x_api_key:
        env = verify_api_key(x_api_key)
        if env:
            # Create a pseudo-token payload for API key auth
            return TokenPayload(
                uid=f"api-key-{env}",
                email=None,
                claims={"auth_type": "api_key", "environment": env},
            )
    
    # Try Firebase token
    token = extract_token(authorization)
    if token:
        if not is_firebase_configured():
            # In development without Firebase, create a mock user
            if settings.debug:
                return TokenPayload(
                    uid="dev-user-mock",
                    email="dev@example.com",
                    claims={"auth_type": "mock", "debug": True},
                )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service not configured",
            )
        
        try:
            return verify_firebase_token(token)
        except FirebaseAuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.message,
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return None


async def require_auth(
    user: Annotated[Optional[TokenPayload], Depends(get_current_user)]
) -> TokenPayload:
    """
    Require authentication.

    Use this dependency for endpoints that require authentication.
    Raises 401 if no valid authentication provided.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def require_admin(
    user: Annotated[TokenPayload, Depends(require_auth)]
) -> TokenPayload:
    """
    Require admin privileges.

    Use this dependency for admin-only endpoints.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user


# Type aliases for easier use in endpoints
CurrentUser = Annotated[Optional[TokenPayload], Depends(get_current_user)]
RequiredUser = Annotated[TokenPayload, Depends(require_auth)]
AdminUser = Annotated[TokenPayload, Depends(require_admin)]
