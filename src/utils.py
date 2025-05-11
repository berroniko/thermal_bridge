from datetime import datetime

from prompt_toolkit import prompt


def is_nan(value) -> bool:
    if isinstance(value, float):
        if value != value:
            return True
        else:
            return False
    if not value:
        return True
    else:
        return False


def input_with_default(message: str, default: str) -> str:
    return prompt(message, default=default)


def parse_date(date_str: str) -> datetime:
    for fmt in ('%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    user_input = input_with_default(message="please correct this to the format dd.mm.yyyy:",
                                        default=date_str)
    return parse_date(user_input)


if __name__ == '__main__':
    # result = input_with_default("please correct: ", default="hällo")
    result = parse_date("34.12.2018")
    print(result)
