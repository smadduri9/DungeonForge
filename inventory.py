#!/usr/bin/env python3
"""
Inventory management system for DungeonForge
Handles items, equipment, and character inventory
"""

from enum import Enum
from typing import List, Optional, Dict
from dataclasses import dataclass


class ItemType(Enum):
    """Types of items available in the game."""
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    SCROLL = "scroll"
    TREASURE = "treasure"
    QUEST = "quest"


class Rarity(Enum):
    """Item rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Item:
    """Represents an item in the game."""
    name: str
    item_type: ItemType
    rarity: Rarity
    value: int
    description: str
    stats: Optional[Dict[str, int]] = None
    stackable: bool = False
    quantity: int = 1
    
    def __str__(self) -> str:
        """Return string representation of item."""
        rarity_emoji = {
            Rarity.COMMON: "⚪",
            Rarity.UNCOMMON: "🟢",
            Rarity.RARE: "🔵",
            Rarity.EPIC: "🟣",
            Rarity.LEGENDARY: "🟠"
        }
        emoji = rarity_emoji.get(self.rarity, "⚪")
        
        qty = f" x{self.quantity}" if self.stackable and self.quantity > 1 else ""
        return f"{emoji} {self.name}{qty} - {self.value}g"
    
    def get_details(self) -> str:
        """Return detailed item information."""
        details = [
            f"{self}",
            f"Type: {self.item_type.value.title()}",
            f"Rarity: {self.rarity.value.title()}",
            f"Description: {self.description}"
        ]
        
        if self.stats:
            details.append("Stats:")
            for stat, value in self.stats.items():
                sign = "+" if value >= 0 else ""
                details.append(f"  {stat.title()}: {sign}{value}")
        
        return "\n".join(details)


class Inventory:
    """Manages character inventory."""
    
    def __init__(self, max_slots: int = 20):
        """
        Initialize inventory.
        
        Args:
            max_slots: Maximum number of inventory slots
        """
        self.max_slots = max_slots
        self.items: List[Item] = []
        self.gold = 0
        self.equipped: Dict[str, Optional[Item]] = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
    
    def add_item(self, item: Item) -> bool:
        """
        Add an item to inventory.
        
        Args:
            item: Item to add
            
        Returns:
            True if item was added, False if inventory is full
        """
        # Check if item is stackable and already in inventory
        if item.stackable:
            for inv_item in self.items:
                if inv_item.name == item.name:
                    inv_item.quantity += item.quantity
                    return True
        
        # Check if inventory has space
        if len(self.items) >= self.max_slots:
            return False
        
        self.items.append(item)
        return True
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Remove an item from inventory.
        
        Args:
            item_name: Name of item to remove
            quantity: Number of items to remove
            
        Returns:
            True if item was removed, False if not found
        """
        for item in self.items:
            if item.name == item_name:
                if item.stackable and item.quantity > quantity:
                    item.quantity -= quantity
                    return True
                elif item.stackable and item.quantity == quantity or not item.stackable:
                    self.items.remove(item)
                    return True
        return False
    
    def get_item(self, item_name: str) -> Optional[Item]:
        """
        Get an item from inventory by name.
        
        Args:
            item_name: Name of the item
            
        Returns:
            The item if found, None otherwise
        """
        for item in self.items:
            if item.name == item_name:
                return item
        return None
    
    def equip_item(self, item_name: str) -> bool:
        """
        Equip an item from inventory.
        
        Args:
            item_name: Name of item to equip
            
        Returns:
            True if equipped successfully, False otherwise
        """
        item = self.get_item(item_name)
        if not item:
            return False
        
        if item.item_type == ItemType.WEAPON:
            if self.equipped["weapon"]:
                self.add_item(self.equipped["weapon"])
            self.equipped["weapon"] = item
            self.items.remove(item)
            return True
        elif item.item_type == ItemType.ARMOR:
            if self.equipped["armor"]:
                self.add_item(self.equipped["armor"])
            self.equipped["armor"] = item
            self.items.remove(item)
            return True
        
        return False
    
    def get_total_value(self) -> int:
        """
        Calculate total value of all items in inventory.
        
        Returns:
            Total gold value
        """
        total = self.gold
        for item in self.items:
            total += item.value * item.quantity
        for item in self.equipped.values():
            if item:
                total += item.value
        return total
    
    def display_inventory(self) -> str:
        """
        Get formatted inventory display.
        
        Returns:
            Formatted string of inventory contents
        """
        lines = [
            "=== INVENTORY ===",
            f"Gold: {self.gold}g",
            f"Slots Used: {len(self.items)}/{self.max_slots}",
            "",
            "Equipped:"
        ]
        
        for slot, item in self.equipped.items():
            if item:
                lines.append(f"  {slot.title()}: {item}")
            else:
                lines.append(f"  {slot.title()}: Empty")
        
        lines.append("\nItems:")
        if self.items:
            for item in sorted(self.items, key=lambda x: (x.rarity.value, x.name)):
                lines.append(f"  {item}")
        else:
            lines.append("  (Empty)")
        
        lines.append(f"\nTotal Value: {self.get_total_value()}g")
        return "\n".join(lines)


# Predefined items for the game
ITEM_CATALOG = {
    "iron_sword": Item(
        name="Iron Sword",
        item_type=ItemType.WEAPON,
        rarity=Rarity.COMMON,
        value=50,
        description="A sturdy iron sword.",
        stats={"attack": 10, "durability": 100}
    ),
    "steel_armor": Item(
        name="Steel Armor",
        item_type=ItemType.ARMOR,
        rarity=Rarity.UNCOMMON,
        value=150,
        description="Well-crafted steel armor.",
        stats={"defense": 15, "weight": 20}
    ),
    "health_potion": Item(
        name="Health Potion",
        item_type=ItemType.POTION,
        rarity=Rarity.COMMON,
        value=25,
        description="Restores 50 HP.",
        stats={"healing": 50},
        stackable=True
    ),
    "mana_potion": Item(
        name="Mana Potion",
        item_type=ItemType.POTION,
        rarity=Rarity.COMMON,
        value=30,
        description="Restores 30 MP.",
        stats={"mana_restore": 30},
        stackable=True
    ),
    "legendary_axe": Item(
        name="Axe of the Ancients",
        item_type=ItemType.WEAPON,
        rarity=Rarity.LEGENDARY,
        value=1000,
        description="A legendary weapon of immense power.",
        stats={"attack": 50, "critical": 25, "durability": 500}
    )
}


def main():
    """Demonstrate inventory system."""
    print("=== DungeonForge Inventory System Demo ===\n")
    
    # Create an inventory
    inv = Inventory(max_slots=10)
    inv.gold = 250
    
    # Add some items
    print("Adding items to inventory...")
    inv.add_item(ITEM_CATALOG["iron_sword"])
    inv.add_item(ITEM_CATALOG["steel_armor"])
    
    # Add stackable items
    health_pot = Item(**ITEM_CATALOG["health_potion"].__dict__)
    health_pot.quantity = 3
    inv.add_item(health_pot)
    
    inv.add_item(ITEM_CATALOG["mana_potion"])
    inv.add_item(ITEM_CATALOG["legendary_axe"])
    
    # Display inventory
    print(inv.display_inventory())
    
    # Equip an item
    print("\n\nEquipping Iron Sword...")
    inv.equip_item("Iron Sword")
    print(inv.display_inventory())
    
    # Show item details
    print("\n\n=== Item Details ===")
    legendary = inv.get_item("Axe of the Ancients")
    if legendary:
        print(legendary.get_details())


if __name__ == "__main__":
    main()

