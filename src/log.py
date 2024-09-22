from datetime import datetime

LOG_FILE = "events.log"


def get_timestamp(time=None):

    # Use current time, if not provided
    if time == None:
        time = datetime.now()

    # Generate and return the timestamp
    return time.strftime("%Y-%m-%d")


def write_log(message, time=None):

    # Get the timestamp
    ts = get_timestamp(time)

    # Create the formatted string
    content = f"[{ts}] {message}"

    # Write the content to the log file
    with open(LOG_FILE, "a") as f:
        f.write(f"{content}\n")

    # Print the content
    print(message)
