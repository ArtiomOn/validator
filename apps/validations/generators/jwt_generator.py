import base64

import jwt


class JWTGenerator:

    @staticmethod
    def generate(validated_data):
        headers = validated_data.get("header")
        encoded_jwt = jwt.encode(
            payload=headers,
            key=base64.b64decode('c2VjcmV0'),
            algorithm="HS256"
        )
        return encoded_jwt
