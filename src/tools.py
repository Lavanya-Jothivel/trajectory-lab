import ast
import operator
import re
import requests


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


# =========================================================
# CALCULATOR
# =========================================================

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(
        node.value,
        (int, float),
    ):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return OPERATORS[type(node.op)](
            left,
            right,
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )

        result = _evaluate(tree.body)

        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


# =========================================================
# EXACT KNOWLEDGE ANSWERS
# =========================================================

EXACT_ANSWERS = {
    "capital of japan": "Tokyo",
    "what is the capital of japan": "Tokyo",
    "capital of france": "Paris",
    "what is the capital of france": "Paris",
    "creator of python": "Guido van Rossum",
    "who is the creator of python": "Guido van Rossum",
    "who created python": "Guido van Rossum",
    "who invented python": "Guido van Rossum",
}


def _normalize_query(query: str) -> str:
    """
    Normalize a question for exact-match lookup.
    """

    normalized = query.strip().lower()

    normalized = normalized.rstrip("?.!")

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized


# =========================================================
# WIKIPEDIA LOOKUP
# =========================================================

def _clean_lookup_query(query: str) -> str:
    """
    Convert natural-language questions into
    Wikipedia-friendly search terms.
    """

    cleaned = query.strip()

    patterns = [
        r"^what is\s+",
        r"^what are\s+",
        r"^who is\s+",
        r"^who was\s+",
        r"^who created\s+",
        r"^who invented\s+",
        r"^tell me about\s+",
        r"^explain\s+",
        r"^define\s+",
    ]

    for pattern in patterns:
        cleaned = re.sub(
            pattern,
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

    return cleaned.strip(" ?.")


def _search_wikipedia(query: str):
    """
    Search Wikipedia and return the best page title.
    """

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": 5,
    }

    headers = {
        "User-Agent": "TrajectoryLab/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get(
        "query",
        {},
    ).get(
        "search",
        [],
    )

    if not results:
        return None

    return results[0]["title"]


def _get_wikipedia_summary(title: str):
    """
    Retrieve a short introduction from Wikipedia.
    """

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": True,
        "titles": title,
        "format": "json",
        "utf8": 1,
    }

    headers = {
        "User-Agent": "TrajectoryLab/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    pages = data.get(
        "query",
        {},
    ).get(
        "pages",
        {},
    )

    for page in pages.values():

        extract = page.get("extract")

        if not extract:
            continue

        sentences = re.split(
            r"(?<=[.!?])\s+",
            extract,
        )

        return " ".join(
            sentences[:2]
        )

    return None


def lookup(query: str) -> str:
    """
    Hybrid knowledge lookup.

    Known benchmark questions return concise
    deterministic answers.

    Other questions use Wikipedia dynamically.
    """

    normalized = _normalize_query(query)

    if normalized in EXACT_ANSWERS:
        return EXACT_ANSWERS[normalized]

    try:
        search_query = _clean_lookup_query(query)

        title = _search_wikipedia(
            search_query
        )

        if title is None:
            return (
                f"No Wikipedia result found for: {query}"
            )

        summary = _get_wikipedia_summary(
            title
        )

        if summary is None:
            return (
                f"No summary available for: {title}"
            )

        return summary

    except requests.exceptions.Timeout:
        return (
            "ERROR: Wikipedia request timed out"
        )

    except requests.exceptions.RequestException as error:
        return (
            "ERROR: Wikipedia request failed: "
            f"{error}"
        )

    except Exception as error:
        return f"Lookup error: {error}"


# =========================================================
# UNRELIABLE CALCULATOR
# =========================================================

def unreliable_calculator(expression: str) -> str:
    """
    Simulates an explicit calculator failure.
    """

    if "15" in expression:
        return (
            "ERROR: calculator temporarily unavailable"
        )

    return calculator(expression)


# =========================================================
# FAULTY CALCULATOR
# =========================================================

def faulty_calculator(expression: str) -> str:
    """
    Simulates a silent calculator error.
    """

    normalized = expression.replace(
        " ",
        "",
    )

    if "8*8" in normalized:
        return "63"

    return calculator(expression)


# =========================================================
# UNRELIABLE LOOKUP
# =========================================================

def unreliable_lookup(query: str) -> str:
    """
    Simulates an explicit knowledge lookup failure.
    """

    if "japan" in query.lower():
        return (
            "ERROR: lookup service temporarily unavailable"
        )

    return lookup(query)


# =========================================================
# FAULTY LOOKUP
# =========================================================

def faulty_lookup(query: str) -> str:
    """
    Simulates a silent factual error.
    """

    normalized = _normalize_query(query)

    if (
        "capital of france" in normalized
        or "france capital" in normalized
    ):
        return "Lyon"

    return lookup(query)


# =========================================================
# TOOL REGISTRY
# =========================================================

TOOLS = {
    "calculator": calculator,
    "unreliable_calculator": unreliable_calculator,
    "faulty_calculator": faulty_calculator,
    "lookup": lookup,
    "unreliable_lookup": unreliable_lookup,
    "faulty_lookup": faulty_lookup,
}


def run_tool(
    tool_name: str,
    tool_input: str,
) -> str:
    """Run a registered tool by name."""

    tool = TOOLS.get(tool_name)

    if tool is None:
        return (
            f"Unknown tool: {tool_name}"
        )

    return tool(tool_input)