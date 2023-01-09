import base64

import jwt
from jwt import DecodeError


class JWTGenerator:
    @staticmethod
    def encode(validated_data: dict) -> str:
        headers = validated_data.get("header")
        encoded_jwt = jwt.encode(payload=headers, key=base64.b64decode("c2VjcmV0"), algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decode(validated_data: dict) -> str:
        encoded_jwt = validated_data.get("jwt_token")
        try:
            decoded_jwt = jwt.decode(jwt=encoded_jwt, key=base64.b64decode("c2VjcmV0"), algorithms=["HS256"])
        except DecodeError:
            raise DecodeError("Invalid JWT token")
        return decoded_jwt
