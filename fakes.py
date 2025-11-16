from faker import Faker

fake = Faker()

def generate_user_login():
    """Генерирует уникальное имя пользователя"""
    return fake.user_name()


def generate_random_password():
    """Генерирует случайный пароль числовой длины 4 цифры"""
    return fake.random_number(4)



def generate_first_name():
    """
    Генерирует случайное имя пользователя.
    """
    return fake.first_name()


