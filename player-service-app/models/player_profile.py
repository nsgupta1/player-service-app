from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class PlayerProfile:
    playerId: str
    nameFirst: str
    nameLast: str
    nameGiven: Optional[str] = None
    birthYear: Optional[int] = None
    birthMonth: Optional[int] = None
    birthDay: Optional[int] = None
    birthCountry: Optional[str] = None
    birthState: Optional[str] = None
    birthCity: Optional[str] = None
    deathYear: Optional[int] = None
    deathMonth: Optional[int] = None
    deathDay: Optional[int] = None
    deathCountry: Optional[str] = None
    deathState: Optional[str] = None
    deathCity: Optional[str] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    bats: Optional[str] = None
    throws: Optional[str] = None
    debut: Optional[str] = None
    finalGame: Optional[str] = None
    retroID: Optional[str] = None
    bbrefID: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProfile':
        return cls(**{
            k: v for k, v in data.items() 
            if k in cls.__annotations__
        })

    @property
    def full_name(self) -> str:
        return f"{self.nameFirst} {self.nameLast}"

    @property
    def birth_date(self) -> Optional[date]:
        if all(v is not None for v in [self.birthYear, self.birthMonth, self.birthDay]):
            return date(self.birthYear, self.birthMonth, self.birthDay)
        return None

    @property
    def death_date(self) -> Optional[date]:
        if all(v is not None for v in [self.deathYear, self.deathMonth, self.deathDay]):
            return date(self.deathYear, self.deathMonth, self.deathDay)
        return None