import time
import threading
import winsound

def convert_to_24hr(time_str):
    return time.strftime("%H:%M", time.strptime(time_str, "%I:%M %p"))


def start_alarm(task_time, task_name):
    def run_alarm():
        # Convert input (12-hour → 24-hour)
        converted_time = convert_to_24hr(task_time)

        print(f"⏳ Waiting for {task_name} at {task_time}")

        while True:
            current_time = time.strftime("%H:%M")

            if current_time == converted_time:
                print(f"🔔 Reminder: {task_name} - Start now!")

                # 🔊 Sound
                for _ in range(3):
                    winsound.Beep(1000, 500)
                    time.sleep(5)

                break

            time.sleep(30)

    threading.Thread(target=run_alarm).start()


