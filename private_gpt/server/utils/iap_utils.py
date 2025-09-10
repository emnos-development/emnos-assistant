import logging
from fastapi import HTTPException, Request, status
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

logger = logging.getLogger(__name__)

class IAPValidator:
    def __init__(self, audience: str):
        self.audience = audience
        self.request_adapter = grequests.Request()

    def validate_request(self, request: Request):
        """
        Validates the IAP-signed JWT in the incoming request headers.
        Raises HTTPException if invalid.
        """
        iap_jwt = request.headers.get("x-goog-iap-jwt-assertion")
        if not iap_jwt:
            logger.warning("Missing x-goog-iap-jwt-assertion header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing IAP token"
            )

        try:
            id_token.verify_token(
                iap_jwt,
                self.request_adapter,
                audience=self.audience
            )
            logger.info("IAP token validated successfully")
            return True  # valid
        except Exception as e:
            logger.error(f"Invalid IAP token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid IAP token"
            )