from datetime import datetime, timedelta

def calculate_stop_time(remaining_time):
    # Parse the remaining time input (h:mm)
    try:
        hours, minutes = map(int, remaining_time.split('.'))
        current_time = datetime.now().time()
        half_past_12 = datetime.strptime('12:30', '%H:%M').time()

        if current_time < half_past_12:
            choice = input("Do you want to calculate the lunch break? (y/n): ").lower()
            if choice == 'y':
                lunch = int(input("How long do you plan to take your lunch break? (in minutes): ").lower())
                if (0 <= lunch <= 60):
                    minutes += lunch
                    if minutes >= 60:
                        hours += 1
                        minutes -= 60
            elif choice == 'n':
                print("Okay, lunch break calculation skipped.")
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
                exit()

        remaining_delta = timedelta(hours=hours, minutes=minutes)

    except ValueError:
        print("Invalid time format. Please use 'h.mm'.")
        return None

    # Get the current local time
    now = datetime.now()
    stop_time = now + remaining_delta
    print(f"\n\nYou can stop working at: {stop_time.strftime('%H:%M')}")
    return stop_time

def calculate_remaining_intervals(stop_time):
    # Define the target intervals (4:00 PM, 4:30 PM, ..., 6:30 PM)
    intervals = [
        datetime(stop_time.year, stop_time.month, stop_time.day, 16, 0),
        datetime(stop_time.year, stop_time.month, stop_time.day, 16, 30),
        datetime(stop_time.year, stop_time.month, stop_time.day, 17, 0),
        datetime(stop_time.year, stop_time.month, stop_time.day, 17, 30),
        datetime(stop_time.year, stop_time.month, stop_time.day, 18, 0),
        datetime(stop_time.year, stop_time.month, stop_time.day, 18, 30)
    ]

    # Get the current local time
    now = datetime.now()

    # Calculate remaining time for each interval
    for interval in intervals:
        if now < interval:  # Display intervals that aren't past due
            remaining_time = interval - stop_time  # Reversed the subtraction
            hours, remainder = divmod(abs(remaining_time.seconds), 3600)  # Get absolute value of remaining time
            minutes, _ = divmod(remainder, 60)
            if remaining_time.days < 0:
                hours = 24 - abs(hours + 1)
                minutes = 60 - abs(minutes)
                print(f"{interval.strftime('%H:%M')}:   -{hours:02}:{minutes:02}")
            else:
                print(f"{interval.strftime('%H:%M')}:    {hours:02}:{minutes:02} (Overtime)")

# Example usage
if __name__ == "__main__":
    while True:
        remaining_time_input = input("Enter the remaining work time (h.mm): ")
        stop_time = calculate_stop_time(remaining_time_input)
        if stop_time:
            calculate_remaining_intervals(stop_time)
        print("\n\n\n")
