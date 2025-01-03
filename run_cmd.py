from regex import compile as re_compile, match
from utils import DiceIOError
from list_choices import run_choice_command
from roll_dices import run_dices_cmd


shadowrun_mode = set()

IGNORED_COMMANDS = frozenset(["levels", "rank"])

LIST_CHOICE_PATTERN = re_compile("\d*[ul].*")
DICES_PATTERN = re_compile("\d*[ed]")

def run_cmd(cmd: str, user_id) -> str:
    """Returns a non-markdwon-formated message to display, or None. Catches DiceIOError. Doesn't except a '!'"""

    if cmd in IGNORED_COMMANDS:
        return

    cmd = cmd.lower().replace(" ", "")

    if cmd == "sr":
        if user_id in shadowrun_mode:
            shadowrun_mode.remove(user_id)
            return "Mode shadowrun désactivé"

        shadowrun_mode.add(user_id)
        return "Mode shadowrun activé"

    try:
        if match(DICES_PATTERN, cmd): 
            return run_dices_cmd(cmd, False)
        
        if match(LIST_CHOICE_PATTERN, cmd):
            return run_choice_command(cmd)

        return "Commande inconnue"

    except DiceIOError as err:
        return f"Une erreur s'est produite.\n{err.message}"