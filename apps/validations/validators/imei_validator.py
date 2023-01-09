import math
import re

from rest_framework.exceptions import ValidationError


class IMEIValidator:

    # noinspection DuplicatedCode
    def __call__(self, imei: str):
        # Check IMEI length (15 digits)
        if not re.match(r"^\d{15}$", imei):
            raise ValidationError("IMEI is invalid")
        check_imei, validation_digit, = (
            imei[:-1],
            imei[-1],
        )
        # Multiply every second element with 2
        check_imei = [int(num) * 2 if idx % 2 != 0 else int(num) for idx, num in enumerate(check_imei)]
        # Separate imei into single digits and sum them
        imei_sum = sum(list(map(int, "".join(str(e) for e in check_imei))))
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
