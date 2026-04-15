import time
import threading
import time

def start_alarm(task_time, task_name):
    def run_alarm():
        print(f"⏳ Waiting for {task_name} at {task_time}")

        while True:
            current_time = time.strftime("%H:%M")

            if current_time == task_time:
                print(f"🔔 Reminder: {task_name} - Start now!")
                break

    threading.Thread(target=run_alarm).start()

time.sleep(30)
