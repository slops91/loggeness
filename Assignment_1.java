package com.assignments;
import java.util.ArrayDeque;
import java.util.Queue;

public class Assignment_1 {

    // Special value to signal consumers to stop.
    public static final int POISON_PILL = Integer.MIN_VALUE;

    public static void main(String[] args) {
        // Configuration
    	Assignment_1_config config;
        try {
            // tweak these values freely using the config class
            config = new Assignment_1_config(
                    3,   // bufferCapacity
                    3,   // numProducers
                    3,   // numConsumers
                    3   // itemsPerProducer
            );
        } catch (IllegalArgumentException ex) { // catches any invalid configuration
            System.err.println("Invalid configuration: " + ex.getMessage());
            return;
        }

        // Create buffer using config values
        Buffer<Integer> buffer;
        try {
            buffer = new BoundedBuffer<>(config.getBufferCapacity());
        } catch (IllegalArgumentException ex) {
            System.err.println("Failed to create buffer: " + ex.getMessage());
            return;
        }
        // Move values into local variables for convenience
        int numProducers     = config.getNumProducers();
        int numConsumers     = config.getNumConsumers();
        int itemsPerProducer = config.getItemsPerProducer();
        // Consideration for multiple producers and consumers
        Thread[] producers = new Thread[numProducers];
        Thread[] consumers = new Thread[numConsumers];

        // Start consumers first (they will wait for data)
        for (int i = 0; i < numConsumers; i++) {
            consumers[i] = new Thread(
                    new Consumer(i + 1, buffer, POISON_PILL), // Thread id starting from 1
                    "Consumer-" + (i + 1) 
            );
            consumers[i].start(); // will call buffer.take()(shared queue) and block if empty
        }

        // Start producers next
        for (int i = 0; i < numProducers; i++) {
            producers[i] = new Thread(
                    new Producer(i + 1, buffer, itemsPerProducer),
                    "Producer-" + (i + 1)
            );
            producers[i].start(); // will  start putting data into shared queue
        }

        // Wait for producers to finish
        for (Thread producer : producers) {
            try {
                producer.join();
            } catch (InterruptedException e) { // Main thread is interrupted while waiting
                Thread.currentThread().interrupt();
                System.err.println("Main thread interrupted while waiting for producers.");
                return;
            }
        }

        // Send shutdown signal to each consumer 
        System.out.println("All producers finished. Sending poison pills...");
        for (int i = 0; i < numConsumers; i++) {
            try {
                buffer.put(POISON_PILL); // Used poison pills to notify consumers that no more data will be produced 
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.err.println("Main thread interrupted while sending poison pills.");
                return;
            }
        }

        // Wait for consumers to finish
        for (Thread consumer : consumers) {
            try {
                consumer.join();
            } catch (InterruptedException e) { // Main thread is interrupted while waiting
                Thread.currentThread().interrupt();
                System.err.println("Main thread interrupted while waiting for consumers.");
                return;
            }
        }

        System.out.println("All consumers finished. Program exiting normally.");
    }

}

/**
 * Generic buffer interface.
 */
interface Buffer<T> {
    void put(T item) throws InterruptedException;
    T take() throws InterruptedException;
}

/**
 * Thread-safe bounded buffer using wait/notify .
 */
class BoundedBuffer<T> implements Buffer<T> { //Concrete implementation of generic buffer interface(Strategy Pattern)

    private final Queue<T> queue = new ArrayDeque<>();
    private final int capacity;

    public BoundedBuffer(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be positive.");
        }
        this.capacity = capacity;
    }

    @Override
    public void put(T item) throws InterruptedException {
        if (item == null) {
            throw new IllegalArgumentException("Null values are not allowed in the buffer.");
        }

        synchronized (this) { // Only one thread inside this synchronized block for the same buffer object
            while (queue.size() == capacity) {
                wait(); // buffer full, wait for a consumer, releases lock waiting for notify/notfiyAll
            }
            queue.add(item);
            notifyAll(); // wake up any waiting consumers
        }
    }

    @Override
    public T take() throws InterruptedException {
        synchronized (this) { //Mutual Exclusion similar to put() method
            while (queue.isEmpty()) {
                wait(); // buffer empty, wait for a producer, releases lock waiting for notify/notifyAll
            }
            T item = queue.remove(); //FIFO Queue removes item from front of queue
            notifyAll(); // wake up any waiting producers
            return item;
        }
    }
}

/**
 * Producer: generates integers and puts them in the buffer.
 */
class Producer implements Runnable {

    private final int id;
    private final Buffer<Integer> buffer;
    private final int itemsToProduce;

    public Producer(int id, Buffer<Integer> buffer, int itemsToProduce) {
        if (buffer == null) { //Checking for edge cases
            throw new IllegalArgumentException("Buffer cannot be null for Producer.");
        }
        if (itemsToProduce <= 0) { //Checking for edge cases
            throw new IllegalArgumentException("itemsToProduce must be > 0 for Producer.");
        }
        this.id = id;
        this.buffer = buffer;
        this.itemsToProduce = itemsToProduce;
    }

    @Override
    public void run() {
        try {
            for (int i = 1; i <= itemsToProduce; i++) {
                int value = (id * 1000) + i; // Simulating producer thread producing some value
                buffer.put(value);
                System.out.println("Producer " + id + " produced: " + value);

                // Optional: Just to see the thread interleaving seen better in the output
                Thread.sleep(50);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Producer " + id + " interrupted.");
        } catch (IllegalArgumentException e) {
            System.err.println("Producer " + id + " error: " + e.getMessage());
        }
    }
}

/**
 * Consumer: takes integers from the buffer and processes them.
 */
class Consumer implements Runnable {

    private final int id;
    private final Buffer<Integer> buffer;
    private final int poisonPill; // sentinel value for consumer threads signaling them to shut down

    public Consumer(int id, Buffer<Integer> buffer, int poisonPill) {
        if (buffer == null) { //checking for edge cases
            throw new IllegalArgumentException("Buffer cannot be null for Consumer.");
        }
        this.id = id;
        this.buffer = buffer;
        this.poisonPill = poisonPill;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Integer value = buffer.take();

                if (value == poisonPill) { // Keeps consuming until it gets the poison pill signaling shut down
                    System.out.println("Consumer " + id + " received poison pill. Shutting down.");
                    break;
                }

                System.out.println("Consumer " + id + " consumed: " + value);

                // Optional: simulate time taken for consumer to consume
                Thread.sleep(80);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Consumer " + id + " interrupted.");
        } catch (IllegalArgumentException e) {
            System.err.println("Consumer " + id + " error: " + e.getMessage());
        }
    }
}
