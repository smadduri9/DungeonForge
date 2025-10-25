#!/usr/bin/env python3
"""
Game mechanics module for DungeonForge
Handles character stats, experience calculations, and dungeon generation
"""

import json
import random
from typing import Dict, List, Tuple


def load_config(config_path: str = "config.json") -> Dict:
    """
    Load game configuration from JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing game configuration
    """
    with open(config_path, 'r') as f:
        return json.load(f)


class Character:
    """Represents a game character with stats and progression."""
    
    def __init__(self, name: str, config: Dict):
        """
        Initialize a character with starting stats.
        
        Args:
            name: Character name
            config: Game configuration dictionary
        """
        self.name = name
        self.level = config['character']['starting_level']
        self.health = config['character']['starting_health']
        self.mana = config['character']['starting_mana']
        self.experience = 0
        self.max_level = config['character']['max_level']
        self.xp_config = config['experience']
    
    def calculate_xp_needed(self) -> int:
        """
        Calculate XP needed for next level.
        
        Returns:
            Amount of XP required to level up
        """
        base = self.xp_config['base_xp_requirement']
        multiplier = self.xp_config['xp_multiplier']
        return int(base * (multiplier ** (self.level - 1)))
    
    def gain_experience(self, amount: int) -> List[str]:
        """
        Add experience and handle level ups.
        
        Args:
            amount: Amount of XP to gain
            
        Returns:
            List of messages about level ups
        """
        messages = []
        self.experience += amount
        messages.append(f"{self.name} gained {amount} XP!")
        
        while self.experience >= self.calculate_xp_needed() and self.level < self.max_level:
            self.experience -= self.calculate_xp_needed()
            self.level += 1
            self.health += 20
            self.mana += 10
            messages.append(f"🎉 Level up! {self.name} is now level {self.level}!")
        
        return messages
    
    def __str__(self) -> str:
        """Return string representation of character."""
        return (f"{self.name} - Level {self.level} | "
                f"HP: {self.health} | MP: {self.mana} | "
                f"XP: {self.experience}/{self.calculate_xp_needed()}")


class Dungeon:
    """Represents a dungeon with rooms and encounters."""
    
    def __init__(self, config: Dict):
        """
        Initialize a dungeon.
        
        Args:
            config: Game configuration dictionary
        """
        self.config = config['dungeon']
        self.num_rooms = random.randint(
            self.config['min_rooms'],
            self.config['max_rooms']
        )
        self.rooms = self._generate_rooms()
    
    def _generate_rooms(self) -> List[Dict]:
        """
        Generate random dungeon rooms.
        
        Returns:
            List of room dictionaries
        """
        rooms = []
        for i in range(self.num_rooms):
            room = {
                'number': i + 1,
                'has_trap': random.random() < self.config['trap_chance'],
                'has_treasure': random.random() < self.config['treasure_chance'],
                'is_boss': i == self.num_rooms - 1
            }
            rooms.append(room)
        return rooms
    
    def get_room_description(self, room_number: int) -> str:
        """
        Get description of a specific room.
        
        Args:
            room_number: Room number (1-indexed)
            
        Returns:
            Description of the room
        """
        if room_number < 1 or room_number > len(self.rooms):
            return "Invalid room number!"
        
        room = self.rooms[room_number - 1]
        desc = f"Room {room['number']}: "
        
        if room['is_boss']:
            desc += "⚔️ Boss Chamber!"
        elif room['has_trap'] and room['has_treasure']:
            desc += "⚠️ Trapped treasure room!"
        elif room['has_trap']:
            desc += "⚠️ Dangerous trapped room!"
        elif room['has_treasure']:
            desc += "💎 Treasure room!"
        else:
            desc += "Empty room."
        
        return desc


def main():
    """Demonstrate game mechanics."""
    print("=== DungeonForge Game Mechanics Demo ===\n")
    
    # Load configuration
    config = load_config()
    
    # Create a character
    hero = Character("Aragorn", config)
    print(f"Created character: {hero}\n")
    
    # Generate a dungeon
    dungeon = Dungeon(config)
    print(f"Generated dungeon with {dungeon.num_rooms} rooms:\n")
    
    for i in range(1, dungeon.num_rooms + 1):
        print(dungeon.get_room_description(i))
    
    # Simulate gaining experience
    print(f"\n{hero}")
    messages = hero.gain_experience(250)
    for msg in messages:
        print(msg)
    print(f"{hero}")


if __name__ == "__main__":
    main()

