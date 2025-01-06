from enum import StrEnum
from regex import compile as re_compile, search
from random import randint, shuffle
from utils import DiceIOError, fail_if
from parser import Parser


DICE_NUMBER_PATTERN = re_compile("^\d+")
DICE_TYPE_PATTERN = re_compile("^(d|e)")
DICE_SIDE_PATTERN = re_compile("^\d+")
KEEP_PATTERN = re_compile("(?<=^k)((-)?\d+)")
FILTER_PATTERN = re_compile("^\[.(\-)?\d+\]")

class DiceType(StrEnum):
    explode = "explode"
    classic = "classic"

class DiceParser(Parser):
    def __init__(self, cmd: str):
        super().__init__(cmd)

        # Cmd's cleaned in run_cmd
        
        self.dice_number = self.parse_dice_number()
        self.dice_type = self.parse_dice_type()
        self.dice_side = self.parse_dice_side()
        self.sort = self.parse_sort()
        self.filter = self.parse_filter()
        self.keep = self.parse_keep()

        fail_if(self.cmd != "", f"Instructions inconnues : '{self.cmd}'")
        
    def condition_to_func(self, condition: str):
        """Create a filter-function from a condition such as `>5` or `=1`"""
        target_number = int(condition[1:])
        operator = condition[0]

        fail_if(target_number < 1, "Le nombre cible du filtre doit être supérieur ou égal à 1")

        match operator:
            case "!":
                return lambda i: i != target_number

            case "=":
                return lambda i: i == target_number

            case ">":
                return lambda i: i > target_number

            case "<":
                return lambda i: i < target_number

        raise DiceIOError(f"Opérateur inconnu pour le filtre : '{operator}'")
    
    def parse_dice_number(self) -> int:
        dice_number = self.consume_or_none(DICE_NUMBER_PATTERN)
        
        if not dice_number:
            return 1
            
        dice_number = int(dice_number)

        fail_if(dice_number == 0, "Lancer zéro dès n'est pas autorisé")
            
        return dice_number

    def parse_dice_type(self) -> DiceType:
        dice_type = self.consume_or_fail(
            DICE_TYPE_PATTERN,
            f"'e' ou 'd' étaient attendus mais '{self.cmd[0]}' a été trouvé"
        )

        return DiceType.explode if dice_type == "e" else DiceType.classic

    def parse_dice_side(self) -> int:
        dice_side = self.consume_or_fail(
            DICE_SIDE_PATTERN,
            f"Un nombre était attendu en tant que nombre de cotés, mais '{self.cmd}' a été trouvé"
        )

        dice_side = int(dice_side)

        fail_if(dice_side == 0, "Bien essayé mais on ne peut pas lancer des dès à zéro face")
        fail_if(self.dice_type == DiceType.explode and dice_side == 1, "Un dès explode ne peut pas avoir une seule face")
   
        return dice_side

    def parse_sort(self) -> bool:
        sort_ = "s" in self.cmd
        self.cmd = self.cmd.replace("s", "")
        
        return sort_

    @Parser.if_consume_succesed(KEEP_PATTERN)
    def parse_keep(self, keep) -> int | None:
        self.cmd = self.cmd[1:] # KEEP_PATTERN doesn't catch the `k`, so it's removed here
        fail_if(keep == "0", "Garder zéro dès avec 'k' est interdit  ; ça sert a rien en plus") 

        return int(keep)

    @Parser.if_consume_succesed(FILTER_PATTERN)
    def parse_filter(self, filter_):
        return self.condition_to_func(filter_[1:-1])


