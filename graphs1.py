def plot_top_events(events):
    # Sort events by generate count in descending order
    sorted_events = sorted(events.items(), key=lambda item: item[1], reverse=True)
    
    # Select the top 10 events
    top_events = sorted_events[:10]
    
    # Extract the names and values for the top 10 events
    names = [event[0] for event in top_events]
    values = [event[1] for event in top_events]

    # Plot a pie chart
    plt.figure(figsize=(10, 8))
    wedges, texts = plt.pie(values, startangle=140, colors=plt.cm.Paired.colors)
    plt.legend(wedges, [f'{name} ({value})' for name, value in zip(names, values)], title="Events", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Top 10 Events Generated')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
