from string import ascii_letters
from random import choice
from faker import Faker
from faker.providers import internet

def get_fake():
    fake = Faker('ko_KR')
    fake.add_provider(internet)
    return fake


def snake2pascal(string: str):
    """String Convert: snake_case to PascalCase"""
    return (
        string
        .replace("_", " ")
        .title()
        .replace(" ", "")
    )


def pascal2snake(string: str):
    """String Convert: PascalCase to snake_case"""
    return ''.join(
        word.title() for word in string.split('_')
    )


def get_random_id():
    """Get Random String for Identification"""
    string_pool = ascii_letters + "0123456789"
    rand_string = [choice(string_pool) for _ in range(15)]
    return "".join(rand_string)


if __name__ == '__main__':
    pass