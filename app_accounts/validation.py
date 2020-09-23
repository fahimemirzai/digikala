from django.core.exceptions import ValidationError


def validate_order_number(value):  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    if value.startswith('DKC-'):
        return value
    else:
        raise ValidationError


def validate_mailing_code(value):  # 222222222222222222222222222222
    if value.isdigit():
        return value
    else:
        raise ValidationError('must be all digit')  # 222222222222222222222222222222


def validate_cellphone(value):
    if value.startswith('09') and value.isdigit():
        return value
    else:
        raise ValidationError('must start with 09')


def validate_national_code(value):  # 222222222222222222222222222222
    code = value
    if len(code) != 10 or not (code.isdigit()):
        raise ValidationError("false")

    cn = int(code[9])
    number = ''
    for i in range(9):
        number += code[i]

    number = number + '00'

    number = number[::-1]
    total = 0
    for i in range(10, 1, -1):
        total += i * int(number[i])

    remaining = total % 11

    if remaining < 2 and remaining == cn:
        return value

    elif remaining >= 2 and cn == (11 - remaining):
        return value

    else:
        raise ValidationError("false")
