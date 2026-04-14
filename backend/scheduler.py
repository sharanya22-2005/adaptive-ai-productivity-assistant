# scheduler.py
PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

def generate_schedule(tasks):
    # sort by priority (then simple order)
    tasks_sorted = sorted(tasks, key=lambda x: PRIORITY_ORDER.get(x["priority"], 3))

    schedule = []
    current_time = 9  # start 9 AM

    for t in tasks_sorted:
        duration = int(t.get("duration", 1))

        schedule.append({
            "task": t["name"],
            "start_time": f"{current_time}:00",
            "end_time": f"{current_time + duration}:00"
        })

        current_time += duration

    return schedule