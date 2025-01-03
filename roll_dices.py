from random import randint, shuffle
from regex import split, compile as re_compile
from parse_dices import DiceType, DiceParser
from utils import DiceIOError, fail_if


ARTIMETHIC_OPERATOR = re_compile("(\+|(?<!k)\-)")

def run_dices_cmd(cmd: str, user_in_sr_mode: bool) -> str:
    cmd = cmd.lower().replace(" ", "")

    tokens = ["+"] + split(ARTIMETHIC_OPERATOR, cmd)

    # Somehow there are sometimes empty tokens, instead of fixing it we just remove them 
    tokens = list(filter(bool, tokens))

    # Shadowrun mode
    if user_in_sr_mode and len(tokens) == 2:
        parsed = DiceParser(token)

        if parsed.dice_side == 6 \
                and parsed.keep == None \
                and parsed.sort == False \
                and parsed.dice_type == DiceType.classic:

            dices = [randint(1, 6) for _ in range(parsed.dice_number)]
            
            return f"""Nombre de 6 : {dices.count(6)}
Nombre de 5/6 : {dices.count(6) + dices.count(5)}
Nombre de 1 : {dices.count(1)}
"""

    sum_ = 0
    dices = []

    fail_if(len(tokens) % 2 != 0, "Il y'a trop d'opérateurs")
    
    for operator, token in zip(tokens[::2], tokens[1::2]):
        if token.isdigit():
            token_sum = int(token)

        else:
            token_dices = roll_dices(DiceParser(token))
            dices.extend(token_dices)
            token_sum  = sum(token_dices)

        if operator == "+":
            sum_ += token_sum

        elif operator == "-":
            sum_ -= token_sum

        else:
            raise DiceIOError(f"Operateur inconnu, '+' ou '-' étaient attendus mais '{operator}' a été trouvé")

    return format_result(sum_, dices)

def format_result(sum_: int, result: list[int]) -> str:
    return f"""# {sum_}
{", ".join(map(str, result))}
    """

def roll_dices(parsed: DiceParser) -> list[int]:
    """Returns a non-markdwon-formated message to display"""
    
    result = []
    remaining_dices = parsed.dice_number
    
    while True:
        if parsed.dice_type == DiceType.explode and result != []:
            if result[-1] == parsed.dice_side:
                result.append(randint(1, parsed.dice_side))
                continue

        if remaining_dices < 1:
            break
        
        result.append(randint(1, parsed.dice_side))
        remaining_dices -= 1
        
    if parsed.keep:
        result = sorted(result)[:abs(parsed.keep)] if parsed.keep < 0 else sorted(result)[-parsed.keep:]
        shuffle(result)

    if parsed.filter:
        result = list(filter(parsed.filter, result))

    if parsed.sort:
        result.sort()

    return result