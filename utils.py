#!/usr/bin/env python3
"""
Utility functions for DungeonForge
Common helper functions used throughout the game
"""

import random
import time
from typing import List, Any, Callable
from functools import wraps


def roll_dice(sides: int = 6, count: int = 1) -> int:
    """
    Roll dice and return the sum.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        
    Returns:
        Sum of all dice rolls
    """
    return sum(random.randint(1, sides) for _ in range(count))


def calculate_damage(base_damage: int, critical_chance: float = 0.1) -> int:
    """
    Calculate damage with critical hit chance.
    
    Args:
        base_damage: Base damage amount
        critical_chance: Probability of critical hit (0.0 to 1.0)
        
    Returns:
        Final damage amount
    """
    is_critical = random.random() < critical_chance
    multiplier = 2.0 if is_critical else 1.0
    damage = int(base_damage * multiplier)
    
    if is_critical:
        print("💥 Critical Hit!")
    
    return damage


def weighted_choice(choices: List[tuple]) -> Any:
    """
    Make a weighted random choice.
    
    Args:
        choices: List of (item, weight) tuples
        
    Returns:
        Randomly selected item based on weights
    """
    items, weights = zip(*choices)
    return random.choices(items, weights=weights, k=1)[0]


def format_time(seconds: int) -> str:
    """
    Format seconds into a readable time string.
    
    Args:
        seconds: Number of seconds
        
    Returns:
        Formatted time string (e.g., "1h 23m 45s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))


def percentage(part: float, whole: float) -> float:
    """
    Calculate percentage.
    
    Args:
        part: Part value
        whole: Whole value
        
    Returns:
        Percentage (0-100)
    """
    if whole == 0:
        return 0.0
    return (part / whole) * 100


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.
    
    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    return start + (end - start) * clamp(t, 0.0, 1.0)


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️  {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper


def generate_random_name(prefix: str = "", suffix: str = "") -> str:
    """
    Generate a random fantasy name.
    
    Args:
        prefix: Optional prefix for the name
        suffix: Optional suffix for the name
        
    Returns:
        Generated name
    """
    syllables = [
        "ar", "el", "on", "thar", "dor", "gar", "mor", "kal",
        "zen", "rith", "ax", "thor", "drak", "vor", "zul"
    ]
    
    name_parts = [random.choice(syllables) for _ in range(random.randint(2, 4))]
    name = "".join(name_parts).capitalize()
    
    if prefix:
        name = f"{prefix} {name}"
    if suffix:
        name = f"{name} {suffix}"
    
    return name


def progress_bar(current: int, total: int, width: int = 30) -> str:
    """
    Create a text-based progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        width: Width of the progress bar in characters
        
    Returns:
        Formatted progress bar string
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(progress * 100)
    
    return f"[{bar}] {percent}%"


def colorize_text(text: str, color: str = "white") -> str:
    """
    Add color to text using ANSI codes (for terminal display).
    
    Args:
        text: Text to colorize
        color: Color name
        
    Returns:
        Colorized text string
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    
    color_code = colors.get(color.lower(), colors["white"])
    reset_code = colors["reset"]
    
    return f"{color_code}{text}{reset_code}"


def main():
    """Demonstrate utility functions."""
    print("=== DungeonForge Utilities Demo ===\n")
    
    # Dice rolling
    print(f"Rolling 2d6: {roll_dice(6, 2)}")
    print(f"Rolling 1d20: {roll_dice(20)}\n")
    
    # Damage calculation
    print("Calculating damage (base 50, 30% crit):")
    for _ in range(3):
        dmg = calculate_damage(50, 0.3)
        print(f"  Damage: {dmg}")
    print()
    
    # Weighted choice
    loot_table = [
        ("Common Item", 50),
        ("Rare Item", 30),
        ("Epic Item", 15),
        ("Legendary Item", 5)
    ]
    print("Random loot drops:")
    for _ in range(5):
        loot = weighted_choice(loot_table)
        print(f"  Found: {loot}")
    print()
    
    # Random names
    print("Generated fantasy names:")
    for _ in range(3):
        print(f"  {generate_random_name()}")
    print()
    
    # Progress bar
    print("Progress bars:")
    for i in [0, 25, 50, 75, 100]:
        print(f"  {progress_bar(i, 100)}")
    print()
    
    # Colored text
    print("Colored text:")
    print(f"  {colorize_text('Health restored!', 'green')}")
    print(f"  {colorize_text('Warning: Low health!', 'yellow')}")
    print(f"  {colorize_text('Critical damage!', 'red')}")


if __name__ == "__main__":
    main()

