from flask import session

def init_roll_results():
    if "roll_results" not in session:
        session["roll_results"] = {
            dice: {"rolls": [], "total": 0}
            for dice in ["d4", "d6", "d8", "d10", "d12", "d20", "percentile"]
        }

def roll_dice(dice_type, num_dice):
    import random
    init_roll_results()
    results = []
    roll_total = 0

    if dice_type == "percentile":
        for _ in range(num_dice):
            roll = (random.randint(0, 9) * 10) + random.randint(0, 9)
            if roll == 0:
                roll = 100
            results.append(roll)
            roll_total += roll
    else:
        dice_max = int(dice_type[1:])
        for _ in range(num_dice):
            roll = random.randint(1, dice_max)
            results.append(roll)
            roll_total += roll

    session["roll_results"][dice_type]["rolls"].extend(results)
    session["roll_results"][dice_type]["total"] += roll_total
    session.modified = True

    return results, roll_total

def get_results():
    init_roll_results()
    return session["roll_results"]

def get_grand_total():
    return sum(get_results()[dice]["total"] for dice in get_results())

def clear_dice_results(dice_type):
    init_roll_results()
    session["roll_results"][dice_type] = {"rolls": [], "total": 0}
    session.modified = True

def clear_all_results():
    session.pop("roll_results", None)
