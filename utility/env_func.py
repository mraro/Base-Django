import os


def get_env_var(env_name, env_default=''):
    return os.environ.get(env_name, env_default)


def string_to_list(text_to_list):
    """ SE NÃO FOR TEXTO OU SE FOR VAZIO RETORNE []
    SE OS VALORES FOREM VALISDOS RETORNE UMA LISTA SEPARADA POR VIRGULA E RETIRE QUALQUER ESPAÇO DESNECESSARIO"""
    if text_to_list is None or not isinstance(text_to_list, str):
        return []
    return [string.strip() for string in text_to_list.split(",") if string]


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()
    """ teste """
    print(string_to_list(get_env_var("ALLOWED_HOSTS")))
    print(string_to_list(123))
    print(string_to_list("1,1 2, 3"))
