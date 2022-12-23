import math
import random


class ImeiGenerator:
    # noinspection DuplicatedCode
    def generate(self):
        imei = [random.randint(0, 9) for _ in range(14)]
        # Multiply every second element with 2
        check_imei = [int(num) * 2 if idx % 2 != 0 else int(num) for idx, num in enumerate(imei)]
        # Separate imei into single digits and sum them
        imei_sum = sum(list(map(int, ''.join(str(e) for e in check_imei))))
        # Round it up to the nearest multiple of ten
        rounded_imei = self.round_up_multiple(imei_sum)
        # Subtract original number from the rounded-up number
        difference = rounded_imei - imei_sum
        # Return generated imei
        return ''.join(str(e) for e in imei) + str(difference)

    @staticmethod
    def round_up_multiple(number):
        return int(math.ceil(number / 10.0)) * 10
