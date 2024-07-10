import matplotlib.pyplot as plt

# Function to parse the log file
def parse_log_file(file_path):
    events = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("[") and not line.startswith("-"):
                parts = line.split()
                if len(parts) > 2:
                    event_name = parts[0]
                    generate_count = int(parts[1])
                    events[event_name] = generate_count
    return events

# Function to plot the graph
def plot_events(events):
    names = list(events.keys())
    values = list(events.values())

    plt.figure(figsize=(10, 8))
    plt.barh(names, values, color='skyblue')
    plt.xlabel('Number of Events Generated')
    plt.title('Event Generation Count')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()

# Main execution
file_path = '/mnt/data/sample.bt.log'  # Replace with your log file path
events = parse_log_file(file_path)
plot_events(events)
