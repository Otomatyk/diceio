from enum import StrEnum
from regex import compile as re_compile
from random import sample, choices
from utils import fail_if
from parser import Parser


def format(choices_: list[str]) -> str:
    return ", ".join(choices_)

def run_choice_command(cmd: str) -> str:
    return format(
        ChoiceCommandRunner(cmd).pick()
    )

CHOICE_NUMBER_PATTERN = re_compile("^\d+")
CHOICE_TYPE_PATTERN = re_compile("^[ul]")

class ChoiceType(StrEnum):
    unique = "unique"
    classic = "classic"
    
class ChoiceCommandRunner(Parser):
    def __init__(self, cmd: str) -> str:
        super().__init__(cmd)

        # Cmd's cleaned in run_cmd

        self.parse_choice_number()
        self.parse_choice_type()

        self.cmd = self.cmd.lstrip()
        fail_if(self.cmd == "", "Une liste de choix était attendue, mais rien n'a été trouvé")

        self.parse_choices()

        print(self.choice_number, self.choice_type, self.choices)

    def parse_choice_number(self):
        choice_number = self.consume_or_none(CHOICE_NUMBER_PATTERN)

        if not choice_number:
            self.choice_number = 1 
            return

        fail_if(choice_number == "0", "Tirer zéro choix n'est pas autorisé")

        self.choice_number = int(choice_number)

    def parse_choice_type(self):
        choice_type = self.consume_or_fail(
            CHOICE_TYPE_PATTERN,
            f"'u' ou 'l' étaient attendus, mais '{self.cmd[0]}' a été trouvé"
        )

        self.choice_type = ChoiceType.unique if choice_type == "u" else ChoiceType.classic 

    def parse_choices(self):
        self.choices = list(map(str.strip, self.cmd.split(",")))

        fail_if(
            self.choice_number > len(self.choices) and self.choice_type == ChoiceType.unique,
            "Impossible de choisir plus de choix qu'il n'y en a quand les choix sont uniques"
        )

    def pick(self) -> list[str]:
        if self.choice_type == ChoiceType.unique:
            return sample(self.choices, k=self.choice_number)

        if self.choice_type == ChoiceType.classic:
            return choices(self.choices, k=self.choice_number)