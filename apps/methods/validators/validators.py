import re
import math
from ipaddress import IPv4Address, IPv6Address

from validate_email import validate_email


class Validator:
    @staticmethod
    def email_validator(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email is invalid")
        is_valid = validate_email(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_smtp=True,
            smtp_timeout=10,
            smtp_skip_tls=False,
            smtp_tls_context=None,
            smtp_debug=False,
            address_types=frozenset([IPv4Address, IPv6Address])
        )
        return bool(is_valid)

    @classmethod
    def imei_validator(cls, imei: str):
        check_imei, validation_digit, = imei[:-1], imei[-1]
        # Multiply every second element with 2
        check_imei = [int(num) * 2 if idx % 2 != 0 else int(num) for idx, num in enumerate(check_imei)]
        # Separate imei into single digits and sum them
        imei_sum = sum(list(map(int, ''.join(str(e) for e in check_imei))))
        # Round it up to the nearest multiple of ten
        rounded_imei = cls.round_up_multiple(imei_sum)
        # Subtract original number from the rounded-up number
        difference = rounded_imei - imei_sum
        # If two numbers match - imei is valid
        return True if difference == int(validation_digit) else False

    @staticmethod
    def round_up_multiple(number):
        return int(math.ceil(number / 10.0)) * 10
