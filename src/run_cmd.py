from regex import compile as re_compile, match
from utils import DiceIOError
from list_choices import run_choice_command
from roll_dices import run_dices_cmd


shadowrun_mode = set()

IGNORED_COMMANDS = frozenset(["levels", "rank", ""])

DICES_CMD_PATTERN = re_compile("^\d*[de].*")
CHOICES_CMD_PATTERN = re_compile("^\d*[lu].*")

def run_cmd(cmd: str, user_id) -> str:
    """Returns a non-markdwon-formated message to display, or None. Catches DiceIOError. Doesn't except a '!'"""

    if cmd in IGNORED_COMMANDS:
        return

    cmd = cmd.lower()

    if cmd == "sr":
        if user_id in shadowrun_mode:
            shadowrun_mode.remove(user_id)
            return "Mode shadowrun désactivé"

        shadowrun_mode.add(user_id)
        return "Mode shadowrun activé"

    try:
        if match(DICES_CMD_PATTERN, cmd):
            return run_dices_cmd(cmd.replace(" ", ""), user_id in shadowrun_mode)
        
        if match(CHOICES_CMD_PATTERN, cmd):
            return run_choice_command(cmd)

        return "Commande inconnue"

    except DiceIOError as err:
        return f"Erreur : \n{err.message}"

    except Exception as err:
        return f"Une erreur inconnue s'est produite. Merci de contactez le propriétaire pour corriger cela :\n{err}"


while True:
    print(run_cmd(input("> "), 1))