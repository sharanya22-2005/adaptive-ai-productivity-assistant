import time

def start_alarm(task_time, task_name):
    print(f"⏳ Waiting for {task_name} at {task_time}")

    while True:
        current_time = time.strftime("%H:%M")

        if current_time == task_time:
            print(f"🔔 Reminder: {task_name} - Start now!")
            break