#!/usr/bin/env python3
"""
Simple Python demonstration script
"""

def greet(name: str) -> str:
    """
    Returns a greeting message for the given name.
    
    Args:
        name: The name to greet
        
    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to DungeonForge!"


def main():
    """Main function to demonstrate the greeting."""
    print(greet("Adventurer"))
    print("\nDungeonForge - Your adventure begins here!")
    
    # Example of a simple calculation
    levels = [1, 2, 3, 4, 5]
    experience = [level ** 2 * 100 for level in levels]
    
    print("\nLevel progression:")
    for level, exp in zip(levels, experience):
        print(f"Level {level}: {exp} XP required")


if __name__ == "__main__":
    main()

