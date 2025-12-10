package com.assignments;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.Test;



public class Assignment_1_test {
	@Test //Test to check if buffer works for size of 3
    void boundedBuffer_putAndTake_singleThread() throws InterruptedException {
        Buffer<Integer> buffer = new BoundedBuffer<>(3);

        buffer.put(1);
        buffer.put(2);
        buffer.put(3);

        assertEquals(1, buffer.take());
        assertEquals(2, buffer.take());
        assertEquals(3, buffer.take());
    }

    @Test // Test to check that bounder buffer accepts only values greater than 0
    void boundedBuffer_constructorRejectsNonPositiveCapacity() {
        assertThrows(IllegalArgumentException.class, () -> new BoundedBuffer<Integer>(0));
        assertThrows(IllegalArgumentException.class, () -> new BoundedBuffer<Integer>(-5));
    }

    @Test // Test to check for Edge Case where it is NULL and Exception is thrown
    void boundedBuffer_putRejectsNull() throws InterruptedException {
        Buffer<Integer> buffer = new BoundedBuffer<>(2);
        assertThrows(IllegalArgumentException.class, () -> buffer.put(null));
    }

    @Test // Testing Blocking Behavior when Queue is full
    void boundedBuffer_blocksProducerWhenFullAndUnblocksAfterTake() throws Exception {
        final BoundedBuffer<Integer> buffer = new BoundedBuffer<>(1);

        buffer.put(1); // now full, took small size so queue fills up quick

        Thread producerThread = new Thread(() -> {
            try {
                buffer.put(2); // will block until a take() happens
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                fail("Producer thread was interrupted unexpectedly");
            }
        });

        producerThread.start();

        // To ensure hitting the blocking call
        Thread.sleep(100);
        // It should still be alive = blocked
        assertTrue(producerThread.isAlive(), "Producer should be blocked when buffer is full");

        // Now consume one item to free space
        Integer taken = buffer.take();
        assertEquals(1, taken);

        // After space is free, producerThread should finish soon
        producerThread.join(1000);
        assertFalse(producerThread.isAlive(), "Producer should have completed after space freed");

        // And we should be able to take the second produced value
        assertEquals(2, buffer.take());
    }

    /* Producer tests (using fake buffer)
     * Inner Class to help with Tests on Producer
     */
    private static class RecordingBuffer<T> implements Buffer<T> {
        private final List<T> items = Collections.synchronizedList(new ArrayList<>()); // Ensure Thread Safety

        @Override
        public void put(T item) {
            if (item == null) {
                throw new IllegalArgumentException("Null not allowed");
            }
            items.add(item);
        }

        @Override
        public T take() {
            throw new UnsupportedOperationException("Not needed for this test");
        }

        List<T> getItems() {
            return items;
        }
    }

    @Test //Test to check if buffer produces correct number of items
    void producer_producesExpectedNumberOfItems() {
        RecordingBuffer<Integer> buffer = new RecordingBuffer<>();
        int itemsToProduce = 5;
        Producer producer = new Producer(1, buffer, itemsToProduce);

        // Run synchronously in the test thread
        producer.run();

        assertEquals(itemsToProduce, buffer.getItems().size(), "Should produce correct count");

        // Optional: check the pattern of produced values
        // Producer produces these values
        List<Integer> expected = Arrays.asList(1001, 1002, 1003, 1004, 1005);
        assertEquals(expected, buffer.getItems());
    }

    @Test // Ensures Invalid Arguments are rejected
    void producer_constructorRejectsInvalidArguments() {
        Buffer<Integer> dummyBuffer = new BoundedBuffer<>(1);

        assertThrows(IllegalArgumentException.class,
                     () -> new Producer(1, null, 5));

        assertThrows(IllegalArgumentException.class,
                     () -> new Producer(1, dummyBuffer, 0));

        assertThrows(IllegalArgumentException.class,
                     () -> new Producer(1, dummyBuffer, -3));
    }

    /*Consumer tests (using preloaded buffer)
     * Helper class with Consumer Tests
     */

    private static class PreloadedBuffer implements Buffer<Integer> {
        private final List<Integer> source;
        private int index = 0;
        private final List<Integer> consumed = new ArrayList<>();

        private final int poisonPill;

        PreloadedBuffer(List<Integer> values, int poisonPill) {
            this.source = new ArrayList<>(values);
            this.poisonPill = poisonPill;
        }

        @Override
        public synchronized void put(Integer item) {
            throw new UnsupportedOperationException("Not needed for this test");
        }

        @Override
        public synchronized Integer take() {
            if (index >= source.size()) {
                throw new IllegalStateException("No more items to take");
            }
            Integer value = source.get(index++);
            if (!value.equals(poisonPill)) {
                consumed.add(value);
            }
            return value;
        }

        List<Integer> getConsumed() {
            return consumed;
        }
    }

    @Test // Test to check it consumes all items and shutdowns on poison pill
    void consumer_processesAllItemsAndStopsOnPoisonPill() {
        int poison = Assignment_1.POISON_PILL;
        // 3 normal items followed by poison pill
        PreloadedBuffer buffer =
                new PreloadedBuffer(Arrays.asList(10, 20, 30, poison), poison);

        Consumer consumer = new Consumer(1, buffer, poison);

        // run() loops until poison pill; we just call it directly
        consumer.run();

        assertEquals(Arrays.asList(10, 20, 30), buffer.getConsumed(),
                     "Consumer should process all non-poison items exactly once");
    }

    @Test // Test to check it rejects NULL Buffer
    void consumer_constructorRejectsNullBuffer() {
        int poison = Assignment_1.POISON_PILL;
        assertThrows(IllegalArgumentException.class,
                     () -> new Consumer(1, null, poison));
    }
    
 // Assignment_1_config tests

    @Test // Ensure that correct values are stored as expected
    void config_validValuesAreStoredCorrectly() {
        Assignment_1_config config =
                new Assignment_1_config(5, 2, 3, 10);

        assertEquals(5, config.getBufferCapacity());
        assertEquals(2, config.getNumProducers());
        assertEquals(3, config.getNumConsumers());
        assertEquals(10, config.getItemsPerProducer());
    }

    @Test //Ensure Illegal Argument Exception is thrown when invalid values are considered
    void config_invalidValuesThrowException() {
        assertThrows(IllegalArgumentException.class,
                () -> new Assignment_1_config(0, 2, 2, 5));
        assertThrows(IllegalArgumentException.class,
                () -> new Assignment_1_config(5, 0, 2, 5));
        assertThrows(IllegalArgumentException.class,
                () -> new Assignment_1_config(5, 2, 0, 5));
        assertThrows(IllegalArgumentException.class,
                () -> new Assignment_1_config(5, 2, 2, 0));
    }

    @Test // To check if it works for large values
    void config_allowsLargeButValidValues() {
        // large but safe values within int range
        int largeBufferCapacity   = 100000;
        int largeNumProducers     = 1000;
        int largeNumConsumers     = 1000;
        int largeItemsPerProducer = 1000000;

        Assignment_1_config config = new Assignment_1_config(
                largeBufferCapacity,
                largeNumProducers,
                largeNumConsumers,
                largeItemsPerProducer
        );

        assertEquals(largeBufferCapacity,   config.getBufferCapacity());
        assertEquals(largeNumProducers,     config.getNumProducers());
        assertEquals(largeNumConsumers,     config.getNumConsumers());
        assertEquals(largeItemsPerProducer, config.getItemsPerProducer());
    }

   @Test // To check if Illegal Argument Exception is throw when Integer Max Value is exceeded 
    void config_throwsExceptionIfTotalItemsExceedsIntMax() {
        // This should exceed Integer.MAX_VALUE → must throw
        int tooManyProducers = 50000;
        int tooManyItems = 50000;
        
        assertThrows(IllegalArgumentException.class,
                () -> new Assignment_1_config(10, tooManyProducers, 1, tooManyItems),
                "Configuration should reject total items > Integer.MAX_VALUE");
    }
}
