
# IT405L - Activity 1
# Logical Operators and an Expression Evaluator
# Student Number: 2310228-1

import importlib
import sys
import traceback


# STEP 2: Logical operators using comparisons only.

def my_and(a, b):
    if a == True:
        return b == True
    return False


def my_or(a, b):
    if a == True:
        return True
    return b == True


def my_not(a):
    return a == False


# STEP 3: Implication operator.

def my_implies(a, b):
    if a == True:
        return b == True
    return True


# STEP 5: Evaluate nested logical expressions.

def evaluate(expr):
    if isinstance(expr, bool):
        return expr

    op = expr[0]

    if op == "not":
        value = evaluate(expr[1])
        return my_not(value)

    left = evaluate(expr[1])
    right = evaluate(expr[2])

    if op == "and":
        return my_and(left, right)

    if op == "or":
        return my_or(left, right)

    if op == "implies":
        return my_implies(left, right)

    raise ValueError(f"Unknown operator: {op}")


if __name__ == "__main__":

    # STEP 1: Record the installed Python version.

    print("STEP 1 - PYTHON VERSION")
    print(sys.version.split()[0])

    # STEP 4: Test logical operators.

    values = (True, False)

    print("\nSTEP 4 - LOGICAL OPERATOR TRUTH TABLES")

    print("\nMY_NOT")
    for a in values:
        print(f"my_not({a}) = {my_not(a)}")

    print("\nMY_AND")
    for a in values:
        for b in values:
            print(f"my_and({a}, {b}) = {my_and(a, b)}")

    print("\nMY_OR")
    for a in values:
        for b in values:
            print(f"my_or({a}, {b}) = {my_or(a, b)}")

    print("\nMY_IMPLIES")
    for a in values:
        for b in values:
            print(f"my_implies({a}, {b}) = {my_implies(a, b)}")

    # STEP 6: Test at least six logical expressions.
    # Load the original personalized parameters.

    personal_file = importlib.import_module(
        "IT405_A01_2310228-1"
    )

    personalized_expr = personal_file.EXPR

    tests = [
        (("and", True, ("not", False)), True),

        (("or", False, False), False),

        (("implies", True, False), False),

        (("implies", False, False), True),

        (("not", ("and", True,
                  ("or", False, True))), False),

        (personalized_expr, True),
    ]

    print("\nSTEP 6 - LOGICAL EXPRESSION TESTS")

    for number, (expression, expected) in enumerate(
        tests, start=1
    ):
        actual = evaluate(expression)

        if actual == expected:
            status = "PASS"
        else:
            status = "FAIL"

        print(f"\nTEST {number}")
        print(f"Expression: {expression}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        print(f"Result: {status}")

    print("\nPERSONALIZED EXPRESSION:")
    print(personal_file.EXPR_TEXT)

    # STEP 7: Run the specified expression.
    # Record the exact error reported by Python.

    print("\nSTEP 7 - EXPECTED DIVISION ERROR")
    print('Expression: ("or", True, ("and", 1/0, False))')

    try:
        expression = ("or", True, ("and", 1/0, False))
        result = evaluate(expression)
        print(f"Result: {result}")

    except ZeroDivisionError:
        print("\nACTUAL PYTHON ERROR:")
        traceback.print_exc(file=sys.stdout)
