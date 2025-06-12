class ExpressionEvaluator:
    def __init__(self):
        self.stack = []     # Стек для хранения чисел в процессе вычисления выражения


    def is_valid_expression(self, expr):
        """
        Проверка на корректность выражения:
        допустимые символы, сбалансированные скобки, корректные аргументы у функций
        """
        allowed = "0123456789mM(),"  # допустимые символы
        bracket_balance = 0  # счётчик открытых/закрытых скобок

        for char in expr:
            if char not in allowed:
                print("❌ Ошибка: недопустимый символ:", char)
                return False
            if char == '(':
                bracket_balance += 1
            elif char == ')':
                bracket_balance -= 1
            # если закрыли скобку раньше открытия — ошибка
            if bracket_balance < 0:
                print("❌ Ошибка: лишняя закрывающая скобка.")
                return False

        # проверка на несбалансированность скобок
        if bracket_balance != 0:
            print("❌ Ошибка: несбалансированные скобки.")
            return False

        # проверка, что каждая функция имеет ровно два аргумента
        if not self.has_valid_arguments(expr):
            print("❌ Ошибка: каждая функция m(...) и M(...) должна иметь ровно два аргумента.")
            return False

        return True

    # Проверка, что у всех функций m(...) и M(...) два аргумента
    def has_valid_arguments(self, expr):
        i = 0
        while i < len(expr):
            # ищем функцию вида m(...) или M(...)
            if expr[i] in 'mM' and i + 1 < len(expr) and expr[i + 1] == '(':
                i += 2  # пропускаем символ функции и открывающую скобку
                depth = 1  # отслеживаем глубину вложенности
                args = []  # список аргументов текущей функции
                current = ''  # текущий аргумент как строка

                # собираем содержимое функции до закрывающей скобки
                while i < len(expr) and depth > 0:
                    if expr[i] == '(':
                        depth += 1
                        current += expr[i]
                    elif expr[i] == ')':
                        depth -= 1
                        if depth > 0:
                            current += expr[i]
                    elif expr[i] == ',' and depth == 1:
                        # разделяем аргументы по запятой на верхнем уровне
                        args.append(current.strip())
                        current = ''
                    else:
                        current += expr[i]
                    i += 1

                args.append(current.strip())  # добавляем последний аргумент

                if len(args) != 2:
                    return False
            else:
                i += 1
        return True

    # Основной метод: вычисляет выражение, используя стек
    def evaluate(self, expr):
        self.stack.clear()  # очищаем стек перед вычислением
        i = len(expr) - 1  # начинаем обход выражения справа налево

        while i >= 0:
            if expr[i].isdigit():
                # считываем многозначное число справа налево
                number = ''
                while i >= 0 and expr[i].isdigit():
                    number = expr[i] + number  # цифры собираются в обратном порядке
                    i -= 1
                self.stack.append(int(number))  # кладём число в стек

            elif expr[i] in 'mM':
                op = expr[i]  # сохраняем тип операции: min или max
                i -= 2  # пропускаем 'm(' или 'M('

                # проверяем, что в стеке есть два числа для применения функции
                if len(self.stack) < 2:
                    raise ValueError(f"Недостаточно аргументов для функции {op}")

                # извлекаем два аргумента из стека
                a = self.stack.pop()
                b = self.stack.pop()

                # вычисляем min или max и сохраняем результат в стек
                result = min(a, b) if op == 'm' else max(a, b)
                self.stack.append(result)
            else:
                # пропускаем символы '(', ')', ',' и т.п.
                i -= 1

        # в конце в стеке должен остаться один элемент — результат
        if len(self.stack) != 1:
            raise ValueError("Некорректное выражение: стек не сбалансирован.")

        return self.stack[0]


# Пользовательский интерфейс
def main():
    print("🧮 Введите выражение с функциями m(...) и M(...), например: M(15,m(16,8))")

    evaluator = ExpressionEvaluator()

    while True:
        expression = input("Введите выражение без пробелов: ")

        # проверка корректности выражения
        if evaluator.is_valid_expression(expression):
            try:
                result = evaluator.evaluate(expression)
                print("✅ Результат вычисления:", result)
                break  # выходим после успешного вычисления
            except Exception as e:
                # ошибка при выполнении вычислений
                print("❌ Ошибка выполнения:", e)
                print("🔁 Повторите попытку.\n")
        else:
            # если выражение некорректно, повторяем ввод
            print("🔁 Повторите попытку.\n")


# Запуск основной функции
if __name__ == "__main__":
    main()