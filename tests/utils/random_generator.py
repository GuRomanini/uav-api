import string
import random


class RandomGenerator:
    @staticmethod
    def generate_cpf():
        def _generate_first_digit(doc: list) -> str:
            sum = 0
            for i in range(10, 1, -1):
                sum += int(doc[10 - i]) * i
            sum = (sum * 10) % 11
            if sum == 10:
                sum = 0
            return str(sum)

        def _generate_second_digit(doc: list) -> str:
            sum = 0
            for i in range(11, 1, -1):
                sum += int(doc[11 - i]) * i
            sum = (sum * 10) % 11
            if sum == 10:
                sum = 0
            return str(sum)

        cpf = random.choices(string.digits, k=9)
        cpf.append(_generate_first_digit(cpf))
        cpf.append(_generate_second_digit(cpf))
        cpf = "".join(cpf)

        return cpf
