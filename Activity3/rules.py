
# IT405L - Activity 3
# A Rule Engine - Facts, Rules, Queries and Backward Chaining
# Student: Mark James M. Fiel
# Student Number: 2310228-1
# Assigned Slip: B03-1

from itertools import count


# STEP 1: Eight personalized family facts.
# Each fact means parent(older, younger).

FACTS = [
    ("parent", "mara", "sela"),
    ("parent", "mara", "rey"),
    ("parent", "mara", "pia"),
    ("parent", "sela", "dina"),
    ("parent", "dina", "jom"),
    ("parent", "sela", "ana"),
    ("parent", "jom", "fritz"),
    ("parent", "fritz", "gina"),
]


# STEP 2: Check whether a term is a variable.

def is_var(term):
    return isinstance(term, str) and term[:1].isupper()


# STEP 2: Match a pattern against a fact.

def matches(pattern, fact):
    if len(pattern) != len(fact):
        return None

    bindings = {}

    for pattern_term, fact_term in zip(pattern, fact):

        if is_var(pattern_term):
            if pattern_term in bindings:
                if bindings[pattern_term] != fact_term:
                    return None
            else:
                bindings[pattern_term] = fact_term

        elif pattern_term != fact_term:
            return None

    return bindings


# STEP 4: Represent family rules.
# Each rule has a head and a list of conditions.

RULES = [
    # X is the grandparent of Z if
    # X is the parent of Y and Y is the parent of Z.
    (
        ("grandparent", "X", "Z"),
        [
            ("parent", "X", "Y"),
            ("parent", "Y", "Z"),
        ]
    ),

    # STEP 7: A parent is also an ancestor.
    (
        ("ancestor", "X", "Z"),
        [
            ("parent", "X", "Z"),
        ]
    ),

    # STEP 7: Recursive ancestor rule.
    (
        ("ancestor", "X", "Z"),
        [
            ("parent", "X", "Y"),
            ("ancestor", "Y", "Z"),
        ]
    ),
]


# Follow a variable's bindings to its final value.

def resolve(term, bindings):
    while is_var(term) and term in bindings:
        term = bindings[term]

    return term


# Match two terms while keeping existing bindings.

def unify(left, right, bindings):
    if len(left) != len(right):
        return None

    found = bindings.copy()

    for a, b in zip(left, right):
        a = resolve(a, found)
        b = resolve(b, found)

        if a == b:
            continue

        if is_var(a):
            found[a] = b

        elif is_var(b):
            found[b] = a

        else:
            return None

    return found


# Give every use of a rule fresh variable names.

def fresh_rule(rule, number):
    head, conditions = rule
    names = {}

    def rename(term):
        if is_var(term):
            if term not in names:
                names[term] = f"{term}_{number}"

            return names[term]

        return term

    new_head = tuple(rename(x) for x in head)

    new_conditions = [
        tuple(rename(x) for x in goal)
        for goal in conditions
    ]

    return new_head, new_conditions


# STEP 5: Query the facts and rules using backward chaining.

def query(goal, facts=None, rules=None, max_depth=50):
    database = FACTS if facts is None else facts
    knowledge = RULES if rules is None else rules

    serial = count(1)
    answers = []

    variable_names = list(
        dict.fromkeys(
            x for x in goal if is_var(x)
        )
    )

    def solve(goals, bindings, depth):

        # Prevent unlimited recursion.
        if depth > max_depth:
            raise RecursionError(
                "Depth limit reached: possible cyclic ancestor rule"
            )

        # All conditions have been satisfied.
        if not goals:
            yield bindings
            return

        first, *remaining = goals

        # Try matching facts first.
        for fact in database:
            updated = unify(first, fact, bindings)

            if updated is not None:
                yield from solve(
                    remaining,
                    updated,
                    depth + 1
                )

        # Then try the rules.
        for rule in knowledge:
            rule_head, conditions = fresh_rule(
                rule,
                next(serial)
            )

            updated = unify(
                first,
                rule_head,
                bindings
            )

            if updated is not None:
                yield from solve(
                    conditions + remaining,
                    updated,
                    depth + 1
                )

    # Collect results without duplicates.
    for solution in solve([goal], {}, 0):
        answer = {
            name: resolve(name, solution)
            for name in variable_names
        }

        if answer not in answers:
            answers.append(answer)

    return answers
