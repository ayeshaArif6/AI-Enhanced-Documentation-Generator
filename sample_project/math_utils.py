"""Math utilities for demo."""

PI = 3.14159

def area_of_circle(r: float) -> float:
    """Return area of a circle with radius r."""
    return PI * r * r

class Accumulator:
    """Adds numbers and keeps a running total."""

    def __init__(self) -> None:
        self.total = 0

    def add(self, x: float) -> float:
        """Add x to total and return the new total."""
        self.total += x
        return self.total
