# engine/simulator.py

from copy import deepcopy
from engine.scoring import calculate_business_health


def apply_changes(base_data: dict, changes: dict):
    """
    Apply scenario changes to the base data.
    Supports both absolute overrides and incremental changes.
    """

    new_data = deepcopy(base_data)

    for key, value in changes.items():
        if key.endswith("_delta"):
            # Incremental change (e.g. expenses +500)
            field = key.replace("_delta", "")
            new_data[field] = new_data.get(field, 0) + value
        else:
            # Absolute override (e.g. revenue = 20000)
            new_data[key] = value

    return new_data


def simulate_scenario(data: dict, changes: dict):
    """
    Simulate a business scenario by applying changes
    and recalculating business health scores.
    """

    # Step 1: Apply changes
    new_data = apply_changes(data, changes)

    # Step 2: Recalculate scores
    new_scores = calculate_business_health(new_data)

    # Step 3: Return results
    return {
        "new_data": new_data,
        "new_scores": new_scores
    }
