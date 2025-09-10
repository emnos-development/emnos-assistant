import logging
import requests
import jwt
from fastapi import HTTPException, Request, status
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

logger = logging.getLogger(__name__)
IAP_JWK_URL = "https://www.gstatic.com/iap/verify/public_key-jwk"

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
            unverified_claims = jwt.decode(
                iap_jwt,
                options={"verify_signature": False}
            )
            logger.info(f"IAP JWT unverified claims: aud={unverified_claims.get('aud')}")

             # 1. Fetch Google's IAP JWKS
            jwks = requests.get(IAP_JWK_URL).json()
            kid_to_key = {key["kid"]: key for key in jwks["keys"]}
            unverified_header = id_token.get_unverified_header(iap_jwt)
            kid = unverified_header["kid"]
            if kid not in kid_to_key:
                raise HTTPException(status_code=403, detail=f"No matching JWK for kid {kid}")

            # 3. Build public key
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(kid_to_key[kid])
            # 4. Verify the JWT
            jwt.decode(
                iap_jwt,
                key=public_key,
                algorithms=["ES256", "RS256"],  # IAP uses RS256
                audience=self.audience,
                issuer="https://cloud.google.com/iap"
            )
            logger.info("IAP token validated successfully")
            return True  # valid
        except Exception as e:
            logger.error(f"Invalid IAP token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid IAP token"
            )