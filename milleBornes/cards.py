from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntFlag, auto, IntEnum
from typing import Any, Self

class Rule(IntEnum):
    WINNING_DISTANCE: int = 1000
    SPEED_LIMIT = 50
    MAX_USE_200 = 2

class State(IntFlag):
    RED_LIGHT = auto()
    SPEED_LIMIT = auto()
    OUT_OF_FUEL = auto()
    FLAT_TIRE = auto()
    ACCIDENT = auto()

@dataclass(frozen=True, slots=True)
class Card(ABC):
    value: Any
    
    @classmethod
    @abstractmethod
    def get_content(cls) -> dict[Any, int]:
        """Renvoie un dictionnaire de cartes de la classe courante et leur nombre dans le jeu."""
        pass

    @classmethod
    def generate_all(cls) -> list[Self]:
        cards: list[Self] = []
        return sum((v * [cls(k)] for k, v in cls.get_content().items()), cards)

class Distance(Card):
    @classmethod
    def get_content(cls) -> dict[int, int]:
        return {
        25: 10,
        50: 10,
        75: 10,
        100: 12,
        200: 4,
    }

    def __str__(self) -> str:
        return f"{self.value} bornes"
        
class Hazard(Card):
    value: State

    @classmethod
    def get_content(cls) -> dict[State, int]:
        return {
            State.RED_LIGHT: 5,
            State.SPEED_LIMIT: 4,
            State.OUT_OF_FUEL: 3,
            State.FLAT_TIRE: 3,
            State.ACCIDENT: 3,
        }

    def __str__(self) -> str:
        match self.value:
            case State.RED_LIGHT: return "Feu rouge"
            case State.SPEED_LIMIT: return "Limite de vitesse (50 bornes/tour)"
            case State.OUT_OF_FUEL: return "Panne d'essence"
            case State.FLAT_TIRE: return "Crevaison"
            case State.ACCIDENT: return "Accident"

        raise ValueError(f"Carte Corrompue ! Valeur reçue : {self.value!r}")
    
class Remedy(Card):
    value: State

    @classmethod
    def get_content(cls) -> dict[State, int]:
        return {
            State.RED_LIGHT: 14,
            State.SPEED_LIMIT: 6,
            State.OUT_OF_FUEL: 6,
            State.FLAT_TIRE: 6,
            State.ACCIDENT: 6,
        }       

    def __str__(self) -> str:
        match self.value:
            case State.RED_LIGHT: return "Feu vert"
            case State.SPEED_LIMIT: return "Fin de limite de vitesse"
            case State.OUT_OF_FUEL: return "Essence"
            case State.FLAT_TIRE: return "Roue de Secours"
            case State.ACCIDENT: return "Réparations"

        raise ValueError(f"Carte Corrompue ! Valeur reçue : {self.value!r}")

class Safety(Card):
    value: State

    @classmethod
    def get_content(cls) -> dict[State, int]:
        return {
            State.RED_LIGHT | State.SPEED_LIMIT: 1,
            State.OUT_OF_FUEL: 1,
            State.FLAT_TIRE: 1,
            State.ACCIDENT: 1,
        }       

    def __str__(self) -> str:
        match self.value:
            case State.RED_LIGHT | State.SPEED_LIMIT: return "Véhicule prioritaire"
            case State.OUT_OF_FUEL: return "Citerne d'essence"
            case State.FLAT_TIRE: return "Increvable"
            case State.ACCIDENT: return "As du volant"

        if self.value is State.RED_LIGHT | State.SPEED_LIMIT:
            return "Véhicule prioritaire"
