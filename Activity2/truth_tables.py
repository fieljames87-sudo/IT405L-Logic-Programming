
# IT405L - Activity 2
# Truth Tables and Deciding Equivalence by Code
# Student Number: 2310228-1
# Assigned Slip: B03-1

import ast
from itertools import product
from logic_ops import evaluate


# STEP 1: Generate all True and False assignments.

def assignments(variables):
    combinations = product(
        (True, False),
        repeat=len(variables)
    )

    rows = []

    for combination in combinations:
        row = dict(zip(variables, combination))
        rows.append(row)

    return rows


# STEP 3: Read expressions and convert them to tuples.

def convert_expression(node, values):
    if isinstance(node, ast.Name):
        return values[node.id]

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return node.value

        raise ValueError("Only True and False are allowed.")

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return (
                "not",
                convert_expression(node.operand, values)
            )

    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            operator = "and"

        elif isinstance(node.op, ast.Or):
            operator = "or"

        else:
            raise ValueError("Unknown logical operator.")

        result = convert_expression(
            node.values[0],
            values
        )

        for next_value in node.values[1:]:
            result = (
                operator,
                result,
                convert_expression(next_value, values)
            )

        return result

    raise ValueError("Unsupported expression.")


# STEP 3: Replace variables with True or False.

def substitute(expr, values):
    if isinstance(expr, bool):
        return expr

    if isinstance(expr, str):
        if expr in values:
            return values[expr]

        parsed = ast.parse(expr, mode="eval")

        return convert_expression(
            parsed.body,
            values
        )

    if isinstance(expr, tuple):
        operator = expr[0]

        parts = [
            substitute(part, values)
            for part in expr[1:]
        ]

        return (operator, *parts)

    raise ValueError("Invalid expression.")


# STEP 3: Print a complete truth table.

def truth_table(expr, variables):
    print("EXPRESSION:", expr)
    print()

    header = " | ".join(variables)

    print(header + " | Result")
    print("-" * (len(header) + 10))

    for values in assignments(variables):
        filled_expr = substitute(expr, values)

        result = evaluate(filled_expr)

        row = " | ".join(
            str(values[name])
            for name in variables
        )

        print(row + " | " + str(result))

    print()


# STEP 5: Check if two expressions are equivalent.

def equivalent(expr1, expr2, variables):
    for values in assignments(variables):

        first_expr = substitute(expr1, values)
        second_expr = substitute(expr2, values)

        first_result = evaluate(first_expr)
        second_result = evaluate(second_expr)

        if first_result != second_result:
            return False

    return True
