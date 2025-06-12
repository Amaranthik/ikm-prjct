class ExpressionEvaluator:
    def __init__(self):
        self.stack = []

    # Проверка допустимости символов и баланса скобок
    def is_valid_expression(self, expr):
        allowed = "0123456789mM(),"
        bracket_balance = 0

        for char in expr:
            if char not in allowed:
                print("❌ Ошибка: недопустимый символ:", char)
                return False
            if char == '(':
                bracket_balance += 1
            elif char == ')':
                bracket_balance -= 1
            if bracket_balance < 0:
                print("❌ Ошибка: лишняя закрывающая скобка.")
                return False

        if bracket_balance != 0:
            print("❌ Ошибка: несбалансированные скобки.")
            return False

        if not self.has_valid_arguments(expr):
            print("❌ Ошибка: каждая функция m(...) и M(...) должна иметь ровно два аргумента.")
            return False

        return True

    # Проверка количества аргументов в функциях
    def has_valid_arguments(self, expr):
        i = 0
        while i < len(expr):
            if expr[i] in 'mM' and i + 1 < len(expr) and expr[i+1] == '(':
                i += 2
                depth = 1
                args = []
                current = ''
                while i < len(expr) and depth > 0:
                    if expr[i] == '(':
                        depth += 1
                        current += expr[i]
                    elif expr[i] == ')':
                        depth -= 1
                        if depth > 0:
                            current += expr[i]
                    elif expr[i] == ',' and depth == 1:
                        args.append(current.strip())
                        current = ''
                    else:
                        current += expr[i]
                    i += 1
                args.append(current.strip())
                if len(args) != 2:
                    return False
            else:
                i += 1
        return True

    # Вычисление значения выражения
    def evaluate(self, expr):
        self.stack.clear()
        i = len(expr) - 1

        while i >= 0:
            if expr[i].isdigit():
                number = ''
                while i >= 0 and expr[i].isdigit():
                    number = expr[i] + number
                    i -= 1
                self.stack.append(int(number))
            elif expr[i] in 'mM':
                op = expr[i]
                i -= 2  # Пропускаем 'm(' или 'M('

                if len(self.stack) < 2:
                    raise ValueError(f"Недостаточно аргументов для функции {op}")

                a = self.stack.pop()
                b = self.stack.pop()
                result = min(a, b) if op == 'm' else max(a, b)
                self.stack.append(result)
            else:
                i -= 1  # Пропускаем скобки и запятые

        if len(self.stack) != 1:
            raise ValueError("Некорректное выражение: стек не сбалансирован.")

        return self.stack[0]


# Интерфейс для пользователя
def main():
    print("🧮 Введите выражение с функциями m(...) и M(...), например: M(15,m(16,8))")

    evaluator = ExpressionEvaluator()

    while True:
        expression = input("Введите выражение без пробелов: ")

        if evaluator.is_valid_expression(expression):
            try:
                result = evaluator.evaluate(expression)
                print("✅ Результат вычисления:", result)
                break
            except Exception as e:
                print("❌ Ошибка выполнения:", e)
                print("🔁 Повторите попытку.\n")
        else:
            print("🔁 Повторите попытку.\n")


# Запуск программы
if __name__ == "__main__":
    main()