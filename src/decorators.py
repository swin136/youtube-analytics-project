def check_instance(function):
    """Проверяет чтобы второй аргумент функции был экземпляров того же класса, что и первый"""
    def inner(*args, **kwargs):
        if not isinstance(args[1], args[0].__class__):
            raise TypeError('Несоответствие типов для проведения арифметических '
                            '(логических) операций с экземплярами классов!')
        result = function(*args, **kwargs)
        return result

    return inner
