# Узел связного списка для стека
class Node:
    def __init__(self, value):
        self.value = value  # значение узла
        self.next = None    # ссылка на следующий узел

# Реализация стека на основе связного списка
class Stack:
    def __init__(self):
        self.top = None  # вершина стека (ссылка на верхний элемент)

    # Поместить значение в стек
    def push(self, value):
        node = Node(value)  # создаём новый узел
        node.next = self.top  # связываем новый узел с текущей вершиной
        self.top = node  # новый узел становится вершиной

    # Вытолкнуть значение из стека
    def pop(self):
        if self.top is None:
            raise ValueError("Стек пуст")  # защита от пустого стека
        value = self.top.value  # сохраняем значение текущей вершины
        self.top = self.top.next  # переходим к следующему элементу
        return value  # возвращаем значение

    # Очистить стек
    def clear(self):
        self.top = None

    # Подсчитать количество элементов в стеке
    def __len__(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count

# Основной класс — вычислитель выражений
class ExpressionEvaluator:
    def __init__(self):
        self.stack = Stack()

    # Проверка корректности введённого выражения
    def is_valid_expression(self, expr):
        allowed = "0123456789mM(),"
        bracket_balance = 0  # баланс открытых и закрытых скобок

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
            print("❌ Ошибка: у функций m/M должно быть два аргумента.")
            return False

        return True

    # Проверка, что у функций m и M два аргумента
    def has_valid_arguments(self, expr):
        i = 0
        while i < len(expr):
            if expr[i] in 'mM' and i + 1 < len(expr) and expr[i + 1] == '(':
                i += 2  # пропускаем имя функции и открывающую скобку
                depth = 1  # отслеживаем вложенность скобок
                args = []  # аргументы функции
                current = ''  # собираем текущий аргумент
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
                if len(args) != 2:  # проверяем, что аргументов ровно два
                    return False
            else:
                i += 1
        return True

    # Основной метод вычисления выражения
    def evaluate(self, expr):
        self.stack.clear()  # очищаем стек перед каждым вычислением
        i = len(expr) - 1  # обходим строку справа налево (обратный обход)

        while i >= 0:
            if expr[i].isdigit():
                number = ''
                # считываем число (учитываем многозначные числа)
                while i >= 0 and expr[i].isdigit():
                    number = expr[i] + number
                    i -= 1
                self.stack.push(int(number))
            elif expr[i] in 'mM':
                op = expr[i]
                i -= 2  # пропускаем символ функции и '('
                if len(self.stack) < 2:
                    raise ValueError(f"Недостаточно аргументов для функции {op}")
                a = self.stack.pop()
                b = self.stack.pop()
                # применяем min или max
                result = min(a, b) if op == 'm' else max(a, b)
                self.stack.push(result)
            else:
                # игнорируем скобки и запятые
                i -= 1

        if len(self.stack) != 1:
            raise ValueError("Некорректное выражение: стек не сбалансирован.")
        return self.stack.pop()

# Интерфейс пользователя
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

if __name__ == "__main__":
    main()