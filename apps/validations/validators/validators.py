import math
import re
from ipaddress import IPv4Address, IPv6Address

from rest_framework.exceptions import ValidationError
from validate_email import validate_email_or_fail
from validate_email.exceptions import DNSTimeoutError


class EmailValidator:

    def __call__(self, email: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Email is invalid")
        try:
            is_valid = validate_email_or_fail(
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
        except DNSTimeoutError:
            raise ValidationError("Service is unavailable")
        if not is_valid:
            raise ValidationError("Email is invalid")


class IMEIValidator:

    def __call__(self, imei: str):
        # Check IMEI length (15 digits)
        if not re.match(r"^\d{15}$", imei):
            raise ValidationError("IMEI is invalid")
        check_imei, validation_digit, = imei[:-1], imei[-1]
        # Multiply every second element with 2
        check_imei = [int(num) * 2 if idx % 2 != 0 else int(num) for idx, num in enumerate(check_imei)]
        # Separate imei into single digits and sum them
        imei_sum = sum(list(map(int, ''.join(str(e) for e in check_imei))))
        # Round it up to the nearest multiple of ten
        rounded_imei = self.round_up_multiple(imei_sum)
        # Subtract original number from the rounded-up number
        difference = rounded_imei - imei_sum
        # If two numbers match - imei is valid
        if not difference == int(validation_digit):
            raise ValidationError("IMEI is invalid")

    @staticmethod
    def round_up_multiple(number):
        return int(math.ceil(number / 10.0)) * 10
