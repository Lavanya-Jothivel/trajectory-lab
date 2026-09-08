import ast
import operator
import re
from difflib import SequenceMatcher

import requests


# =========================================================
# CONFIGURATION
# =========================================================

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
DUCKDUCKGO_API = "https://api.duckduckgo.com/"

HEADERS = {
    "User-Agent": (
        "TrajectoryLab/2.1 "
        "(educational reliability-agent project)"
    )
}

REQUEST_TIMEOUT = 10


# =========================================================
# SAFE CALCULATOR
# =========================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


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
# DETERMINISTIC BENCHMARK ANSWERS
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
    normalized = query.strip().lower()

    normalized = normalized.rstrip(
        "?.!"
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized


# =========================================================
# QUERY CLEANING
# =========================================================

def _clean_lookup_query(query: str) -> str:
    """
    Convert natural-language questions into
    search-friendly queries.
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

    cleaned = cleaned.strip(
        " ?."
    )

    return cleaned


# =========================================================
# SPECIAL QUERY NORMALIZATION
# =========================================================

def _expand_search_query(query: str) -> str:
    """
    Improve ambiguous searches before sending them
    to Wikipedia.
    """

    cleaned = _clean_lookup_query(
        query
    )

    normalized = cleaned.lower()

    programming_languages = {
        "java": "Java programming language",
        "python": "Python programming language",
        "c": "C programming language",
        "c++": "C++ programming language",
        "javascript": "JavaScript programming language",
        "typescript": "TypeScript programming language",
        "rust": "Rust programming language",
        "go": "Go programming language",
        "golang": "Go programming language",
        "kotlin": "Kotlin programming language",
        "swift": "Swift programming language",
    }

    if normalized in programming_languages:
        return programming_languages[
            normalized
        ]

    if "programming language" in normalized:
        return cleaned

    return cleaned


# =========================================================
# WIKIPEDIA TITLE RANKING
# =========================================================

def _normalize_title(text: str) -> str:
    """
    Normalize titles for similarity comparison.
    """

    text = text.lower()

    text = re.sub(
        r"[\(\)\[\]\{\},:_\-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _title_score(
    search_query: str,
    title: str,
) -> float:
    """
    Score a Wikipedia result title based on how closely
    it matches the intended query.
    """

    query_normalized = _normalize_title(
        search_query
    )

    title_normalized = _normalize_title(
        title
    )

    score = 0.0

    # Exact normalized match
    if title_normalized == query_normalized:
        score += 100

    # Strong prefix match
    if title_normalized.startswith(
        query_normalized
    ):
        score += 40

    if query_normalized.startswith(
        title_normalized
    ):
        score += 25

    # Token overlap
    query_words = set(
        query_normalized.split()
    )

    title_words = set(
        title_normalized.split()
    )

    if query_words:
        overlap = len(
            query_words & title_words
        ) / len(query_words)

        score += overlap * 40

    # String similarity
    similarity = SequenceMatcher(
        None,
        query_normalized,
        title_normalized,
    ).ratio()

    score += similarity * 20

    # Prefer programming-language pages
    if (
        "programming language" in query_normalized
        and "programming language" in title_normalized
    ):
        score += 35

    # Penalize comparison/list pages
    unwanted_terms = [
        "comparison",
        "list of",
        "history of",
        "syntax",
        "criticisms",
        "versions",
    ]

    for term in unwanted_terms:
        if term in title_normalized:
            score -= 50

    return score


def _select_best_title(
    search_query: str,
    results: list,
):
    """
    Select the most relevant Wikipedia title.
    """

    if not results:
        return None

    scored_results = []

    for item in results:
        title = item.get(
            "title"
        )

        if not title:
            continue

        score = _title_score(
            search_query,
            title,
        )

        scored_results.append(
            (
                score,
                title,
            )
        )

    if not scored_results:
        return None

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return scored_results[0][1]


# =========================================================
# WIKIPEDIA SEARCH
# =========================================================

def _search_wikipedia(query: str):
    """
    Search Wikipedia and select the most relevant
    page title instead of blindly taking result #1.
    """

    search_query = _expand_search_query(
        query
    )

    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_query,
        "format": "json",
        "utf8": 1,
        "srlimit": 10,
    }

    response = requests.get(
        WIKIPEDIA_API,
        params=params,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    results = (
        data
        .get("query", {})
        .get("search", [])
    )

    return _select_best_title(
        search_query,
        results,
    )


def _get_wikipedia_summary(
    title: str,
):
    """
    Retrieve a short introduction from Wikipedia.
    """

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

    response = requests.get(
        WIKIPEDIA_API,
        params=params,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    pages = (
        data
        .get("query", {})
        .get("pages", {})
    )

    for page in pages.values():

        extract = page.get(
            "extract"
        )

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


def _wikipedia_lookup(
    query: str,
):
    """
    Try retrieving information from Wikipedia.
    """

    try:
        title = _search_wikipedia(
            query
        )

        if title is None:
            return None

        return _get_wikipedia_summary(
            title
        )

    except (
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
    ):
        return None


# =========================================================
# DUCKDUCKGO FALLBACK
# =========================================================

def _duckduckgo_lookup(
    query: str,
):
    """
    Secondary knowledge source used when Wikipedia
    is unavailable or rate-limited.
    """

    try:
        search_query = _expand_search_query(
            query
        )

        params = {
            "q": search_query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
            "no_redirect": 1,
        }

        response = requests.get(
            DUCKDUCKGO_API,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        abstract = data.get(
            "AbstractText",
            "",
        ).strip()

        if abstract:

            sentences = re.split(
                r"(?<=[.!?])\s+",
                abstract,
            )

            return " ".join(
                sentences[:2]
            )

        answer = str(
            data.get(
                "Answer",
                "",
            )
        ).strip()

        if answer:
            return answer

        definition = data.get(
            "Definition",
            "",
        ).strip()

        if definition:
            return definition

        related_topics = data.get(
            "RelatedTopics",
            [],
        )

        for topic in related_topics:

            if not isinstance(
                topic,
                dict,
            ):
                continue

            text = topic.get(
                "Text",
                "",
            ).strip()

            if text:
                return text

        return None

    except (
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
    ):
        return None


# =========================================================
# HYBRID KNOWLEDGE LOOKUP
# =========================================================

def lookup(
    query: str,
) -> str:
    """
    Reliable hybrid knowledge lookup.

    Priority:
    1. Deterministic benchmark answers
    2. Wikipedia with title ranking
    3. DuckDuckGo fallback
    """

    normalized = _normalize_query(
        query
    )

    if normalized in EXACT_ANSWERS:
        return EXACT_ANSWERS[
            normalized
        ]

    wikipedia_result = (
        _wikipedia_lookup(
            query
        )
    )

    if wikipedia_result:
        return wikipedia_result

    fallback_result = (
        _duckduckgo_lookup(
            query
        )
    )

    if fallback_result:
        return fallback_result

    return (
        "ERROR: No knowledge source "
        "could answer this query."
    )


# =========================================================
# UNRELIABLE CALCULATOR
# =========================================================

def unreliable_calculator(
    expression: str,
) -> str:
    """
    Controlled explicit calculator failure.
    """

    if "15" in expression:
        return (
            "ERROR: calculator temporarily unavailable"
        )

    return calculator(
        expression
    )


# =========================================================
# FAULTY CALCULATOR
# =========================================================

def faulty_calculator(
    expression: str,
) -> str:
    """
    Controlled silent calculator error.
    """

    normalized = expression.replace(
        " ",
        "",
    )

    if "8*8" in normalized:
        return "63"

    return calculator(
        expression
    )


# =========================================================
# UNRELIABLE LOOKUP
# =========================================================

def unreliable_lookup(
    query: str,
) -> str:
    """
    Controlled explicit knowledge-tool failure.
    """

    if "japan" in query.lower():
        return (
            "ERROR: lookup service temporarily unavailable"
        )

    return lookup(
        query
    )


# =========================================================
# FAULTY LOOKUP
# =========================================================

def faulty_lookup(
    query: str,
) -> str:
    """
    Controlled silent factual error.
    """

    normalized = _normalize_query(
        query
    )

    if (
        "capital of france" in normalized
        or "france capital" in normalized
    ):
        return "Lyon"

    return lookup(
        query
    )


# =========================================================
# TOOL REGISTRY
# =========================================================

TOOLS = {
    "calculator": calculator,
    "unreliable_calculator": (
        unreliable_calculator
    ),
    "faulty_calculator": (
        faulty_calculator
    ),
    "lookup": lookup,
    "unreliable_lookup": (
        unreliable_lookup
    ),
    "faulty_lookup": (
        faulty_lookup
    ),
}


def run_tool(
    tool_name: str,
    tool_input: str,
) -> str:
    """Run a registered tool."""

    tool = TOOLS.get(
        tool_name
    )

    if tool is None:
        return (
            f"Unknown tool: {tool_name}"
        )

    return tool(
        tool_input
    )