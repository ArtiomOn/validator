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
                address_types=frozenset([IPv4Address, IPv6Address]),
            )
        except DNSTimeoutError:
            raise ValidationError("Service is unavailable")
        except Exception:
            raise ValidationError("Email is invalid")
        else:
            if not is_valid:
                raise ValidationError("Email is invalid")
