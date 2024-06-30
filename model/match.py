from dataclasses import dataclass

@dataclass
class Match:
    id:int
    home:int
    away:int
    homeName:str
    awayName:str

    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        return f"[{self.id}] {self.homeName} vs {self.awayName}"