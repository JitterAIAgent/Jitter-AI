import requests
from typing import Dict, Any, Optional

from .tool_decorator import tool

@tool
def create_shuffled_deck(deck_count: int = 1) -> Dict[str, Any]:
    """Creates a new shuffled deck of cards.
    
    This tool creates a new shuffled deck using the Deck of Cards API.
    The deck will be shuffled and ready for drawing cards.
    
    Args:
        deck_count (int): Number of decks to use (default: 1). Blackjack typically uses 6.
    
    Returns:
        Dict[str, Any]: Response containing deck_id, shuffled status, and remaining cards count.
                       Example: {"success": True, "deck_id": "3p40paa87x90", "shuffled": True, "remaining": 52}
    """
    url = f"https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}"
    response = requests.get(url)
    return response.json()

@tool  
def draw_cards(deck_id: str, count: int = 1) -> Dict[str, Any]:
    """Draws a specified number of cards from a deck.
    
    This tool draws cards from an existing deck using the deck ID.
    Each card includes code, value, suit, and image URL.
    
    Args:
        deck_id (str): The unique identifier for the deck to draw from.
        count (int): Number of cards to draw (default: 1).
    
    Returns:
        Dict[str, Any]: Response containing drawn cards array and remaining count.
                       Example: {"success": True, "deck_id": "kxozasf3edqu", "cards": [...], "remaining": 50}
    """
    url = f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}"
    response = requests.get(url)
    return response.json()

@tool
def draw_random_card(deck_id: str) -> Dict[str, Any]:
    """Draws a single random card from a deck.
    
    This tool draws exactly one card from the specified deck.
    Convenient wrapper for drawing a single card.
    
    Args:
        deck_id (str): The unique identifier for the deck to draw from.
    
    Returns:
        Dict[str, Any]: Response containing single card in cards array and remaining count.
                       Example: {"success": True, "deck_id": "abc123", "cards": [{"code": "AS", "value": "ACE", "suit": "SPADES"}], "remaining": 51}
    """
    return draw_cards(deck_id, 1)

@tool
def create_deck_and_draw_cards(count: int = 1, deck_count: int = 1) -> Dict[str, Any]:
    """Creates a new shuffled deck and immediately draws cards from it.
    
    This tool combines deck creation and card drawing in a single API call.
    More efficient than creating a deck and then drawing cards separately.
    
    Args:
        count (int): Number of cards to draw immediately (default: 1).
        deck_count (int): Number of decks to use (default: 1).
    
    Returns:
        Dict[str, Any]: Response containing deck_id, drawn cards, and remaining count.
                       Example: {"success": True, "deck_id": "xyz789", "cards": [...], "remaining": 51}
    """
    url = f"https://www.deckofcardsapi.com/api/deck/new/draw/?count={count}&deck_count={deck_count}"
    response = requests.get(url)
    return response.json()

@tool
def reshuffle_deck(deck_id: str, remaining_only: bool = False) -> Dict[str, Any]:
    """Reshuffles an existing deck of cards.
    
    This tool reshuffles a deck to randomize the order of cards.
    Can shuffle all cards or only remaining cards in the main deck.
    
    Args:
        deck_id (str): The unique identifier for the deck to reshuffle.
        remaining_only (bool): If True, only shuffle remaining cards in main stack (default: False).
    
    Returns:
        Dict[str, Any]: Response confirming shuffle with deck_id and remaining count.
                       Example: {"success": True, "deck_id": "3p40paa87x90", "shuffled": True, "remaining": 52}
    """
    url = f"https://www.deckofcardsapi.com/api/deck/{deck_id}/shuffle/"
    if remaining_only:
        url += "?remaining=true"
    response = requests.get(url)
    return response.json()

@tool
def create_new_deck(shuffled: bool = False, jokers_enabled: bool = False) -> Dict[str, Any]:
    """Creates a brand new deck of cards in order.
    
    This tool creates a new deck in standard order (A-spades through K-hearts).
    Optionally can be shuffled or include jokers.
    
    Args:
        shuffled (bool): Whether to shuffle the new deck (default: False).
        jokers_enabled (bool): Whether to include two jokers in the deck (default: False).
    
    Returns:
        Dict[str, Any]: Response containing deck_id, shuffled status, and remaining cards count.
                       Example: {"success": True, "deck_id": "3p40paa87x90", "shuffled": False, "remaining": 52}
    """
    url = "https://www.deckofcardsapi.com/api/deck/new/"
    if shuffled:
        url += "shuffle/"
    
    params = []
    if jokers_enabled:
        params.append("jokers_enabled=true")
    
    if params:
        url += "?" + "&".join(params)
    
    response = requests.get(url)
    return response.json()

@tool
def create_partial_deck(card_codes: str, shuffled: bool = True) -> Dict[str, Any]:
    """Creates a partial deck with only specified cards.
    
    This tool creates a deck containing only the cards specified by their codes.
    Useful for specific games or testing scenarios.
    
    Args:
        card_codes (str): Comma-separated card codes (e.g., "AS,2S,KS,AD,2D,KD").
                         Card codes: A,2-9,0(ten),J,Q,K + S(spades),D(diamonds),C(clubs),H(hearts).
        shuffled (bool): Whether to shuffle the partial deck (default: True).
    
    Returns:
        Dict[str, Any]: Response containing deck_id and remaining cards count.
                       Example: {"success": True, "deck_id": "3p40paa87x90", "shuffled": True, "remaining": 12}
    """
    base_url = "https://www.deckofcardsapi.com/api/deck/new/"
    if shuffled:
        base_url += "shuffle/"
    
    url = f"{base_url}?cards={card_codes}"
    response = requests.get(url)
    return response.json()

@tool
def get_deck_info(deck_id: str) -> Dict[str, Any]:
    """Gets information about a deck by attempting to draw 0 cards.
    
    This tool retrieves deck information without drawing cards.
    Useful for checking remaining cards count and deck status.
    
    Args:
        deck_id (str): The unique identifier for the deck to check.
    
    Returns:
        Dict[str, Any]: Response containing deck status and remaining cards count.
                       Example: {"success": True, "deck_id": "abc123", "remaining": 45}
    """
    url = f"https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count=0"
    response = requests.get(url)
    return response.json()
