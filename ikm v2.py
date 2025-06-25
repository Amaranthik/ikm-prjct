# Узел связного списка для реализации стека
class Node:
    def __init__(self, value):
        self.value = value  # значение узла
        self.next = None  # ссылка на следующий узел


# Стек, реализованный на основе связного списка
class Stack:
    def __init__(self):
        self.top = None  # вершина стека (верхний элемент)

    def push(self, value):
        node = Node(value)  # создаём новый узел
        node.next = self.top  # новый узел указывает на текущую вершину
        self.top = node  # обновляем вершину на новый узел

    def pop(self):
        if self.top is None:  # если стек пуст, нельзя извлечь элемент
            raise ValueError("Стек пуст")
        value = self.top.value  # сохраняем значение вершины
        self.top = self.top.next  # удаляем вершину, сдвигаем стек вниз
        return value  # возвращаем значение извлечённого элемента

    def clear(self):
        self.top = None  # очистка стека - просто обнуляем вершину

    def __len__(self):
        count = 0
        current = self.top
        while current:  # считаем количество элементов в стеке
            count += 1
            current = current.next
        return count


# Класс для вычисления выражения
class ExpressionEvaluator:
    def __init__(self):
        self.stack = Stack()

    def evaluate(self, expr):
        self.stack.clear()  # очищаем стек перед вычислением
        i = len(expr) - 1  # идём по строке справа налево

        while i >= 0:
            if expr[i].isdigit():  # если символ цифра
                number = ''
                # собираем полное число (многозначное)
                while i >= 0 and expr[i].isdigit():
                    number = expr[i] + number
                    i -= 1
                self.stack.push(int(number))  # кладём число в стек
            elif expr[i] in 'mM':  # если символ m или M — функция min или max
                op = expr[i]
                i -= 2  # пропускаем символ функции и '('
                a = self.stack.pop()
                b = self.stack.pop()
                # вычисляем min или max
                result = min(a, b) if op == 'm' else max(a, b)
                self.stack.push(result)  # кладём результат обратно в стек
            else:
                i -= 1  # пропускаем скобки и запятые

        if len(self.stack) != 1:  # в конце должен остаться ровно один элемент
            raise ValueError("Некорректное выражение: стек не сбалансирован.")
        return self.stack.pop()  # возвращаем результат вычисления


def main():
    print("🧮 Введите выражение с функциями m(...) и M(...), например: M(15,m(16,8))")

    evaluator = ExpressionEvaluator()

    while True:
        expr = input("Введите выражение без пробелов: ")

        try:
            # Проверяем допустимые символы
            allowed = "0123456789mM(),"
            for ch in expr:
                if ch not in allowed:
                    raise ValueError(f"Недопустимый символ: {ch}")

            # Проверка баланса скобок
            balance = 0
            for ch in expr:
                if ch == '(':
                    balance += 1
                elif ch == ')':
                    balance -= 1
                if balance < 0:  # если закрывающих скобок больше, чем открывающих
                    raise ValueError("Лишняя закрывающая скобка.")
            if balance != 0:  # если открывающих и закрывающих скобок разное количество
                raise ValueError("Несбалансированные скобки.")

            # Проверка, что у функций m/M ровно два аргумента
            i = 0
            while i < len(expr):
                if expr[i] in 'mM' and i + 1 < len(expr) and expr[i + 1] == '(':
                    i += 2  # пропускаем имя функции и '('
                    depth = 1  # считаем вложенность скобок
                    current = ''
                    args = []
                    while i < len(expr) and depth > 0:
                        if expr[i] == '(':
                            depth += 1
                            current += expr[i]
                        elif expr[i] == ')':
                            depth -= 1
                            if depth > 0:
                                current += expr[i]
                        elif expr[i] == ',' and depth == 1:
                            args.append(current.strip())  # добавляем аргумент в список
                            current = ''
                        else:
                            current += expr[i]
                        i += 1
                    args.append(current.strip())  # добавляем последний аргумент
                    if len(args) != 2:  # проверяем, что ровно два аргумента
                        raise ValueError("Функция m/M должна содержать ровно два аргумента.")
                else:
                    i += 1

            # Если все проверки пройдены, вычисляем выражение
            result = evaluator.evaluate(expr)
            print("✅ Результат вычисления:", result)
            break  # завершаем цикл при успешном вычислении

        except Exception as e:
            print("❌ Ошибка:", e)
            print("🔁 Повторите ввод.\n")


if __name__ == "__main__":
    main()
