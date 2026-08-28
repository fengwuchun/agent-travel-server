from langchain_core.tools import tool


@tool
def calculator_add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def calculator_subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number."""
    return a - b


@tool
def calculator_multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def calculator_divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b