from enum import Enum

class RankHeroi(str, Enum):
    C = "C"
    B = "B"
    A = "A"
    S = "S"

class StatusHeroi(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_MISSAO = "EM_MISSAO"
    INATIVO = "INATIVO"
    
