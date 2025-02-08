# utils.py
import random

# Store persistent roll results
ROLL_RESULTS = {
    "d4": [],
    "d6": [],
    "d8": [],
    "d10": [],
    "d12": [],
    "d20": [],
    "percentile": []
}

def roll_dice(dice_type, num_dice):
    """Rolls the specified dice type and appends results to the global results."""
    results = []
    total = 0

    if dice_type == "percentile":
        for _ in range(num_dice):
            roll = (random.randint(0, 9) * 10) + random.randint(0, 9)
            results.append(roll)
            total += roll
    else:
        dice_max = int(dice_type[1:])
        for _ in range(num_dice):
            roll = random.randint(1, dice_max)
            results.append(roll)
            total += roll

    # Add to global results storage
    ROLL_RESULTS[dice_type].extend(results)

    return results, total

def get_total():
    """Returns the grand total of all rolls."""
    return sum(sum(ROLL_RESULTS[dice]) for dice in ROLL_RESULTS)

def clear_results():
    """Clears all stored roll results."""
    for dice in ROLL_RESULTS:
        ROLL_RESULTS[dice] = []
