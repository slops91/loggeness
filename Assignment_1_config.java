// Class is used to configure the values for Main Class
package com.assignments;

public class Assignment_1_config {
	private final int bufferCapacity; // To make these parameters immutable once assigned
    private final int numProducers;
    private final int numConsumers;
    private final int itemsPerProducer;

    public Assignment_1_config(int bufferCapacity,
                               int numProducers,
                               int numConsumers,
                               int itemsPerProducer) {

        if (bufferCapacity <= 0) // Dealing with edge cases
            throw new IllegalArgumentException("Buffer capacity must be > 0.");
        if (numProducers <= 0) // Dealing with edge cases
            throw new IllegalArgumentException("Number of producers must be > 0.");
        if (numConsumers <= 0) // Dealing with edge cases
            throw new IllegalArgumentException("Number of consumers must be > 0.");
        if (itemsPerProducer <= 0) // Dealing with edge cases
            throw new IllegalArgumentException("Items per producer must be > 0.");

        long totalItems = (long) numProducers * itemsPerProducer; // Ensuring that the values assumed don't exceed the value of Integer causing overflow
        if (totalItems > Integer.MAX_VALUE) {
            throw new IllegalArgumentException(
                    "Total items produced exceeds int max value."
            );
        }

        this.bufferCapacity = bufferCapacity;
        this.numProducers = numProducers;
        this.numConsumers = numConsumers;
        this.itemsPerProducer = itemsPerProducer;
    }
    // Getter Methods for the parameters called in the Main Assignment_1 Class
    public int getBufferCapacity() {
        return bufferCapacity;
    }

    public int getNumProducers() {
        return numProducers;
    }

    public int getNumConsumers() {
        return numConsumers;
    }

    public int getItemsPerProducer() {
        return itemsPerProducer;
    }

    @Override
    public String toString() { // Displaying config info
        return String.format(
            "Config{bufferCap=%d, producers=%d, consumers=%d, itemsPerProducer=%d}",
            bufferCapacity, numProducers, numConsumers, itemsPerProducer
        );
    }
}
