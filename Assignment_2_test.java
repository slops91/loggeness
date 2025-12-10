package com.assignments;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class Assignment_2_test {

    private List<SalesRecord> mockData;

    @BeforeEach
    void setUp() {
        mockData = new ArrayList<>();

        // MOCK DATA CREATION
        // Create 4 distinct records to cover various scenarios (Years, Countries, Statuses, Deal Sizes) and all 16 Analytical Queries

        // Record 1: Normal Sale (USA, 2021, Small Deal)
        // Sales: 100.0, Qty: 10, Price: 10.0, MSRP: 10.0 (No Discount)
        mockData.add(new SalesRecord(
            1, 10, 10.0, 1, 100.0, "1/1/2021", "Shipped", 1, 1, 2021, 
            "Cars", 10.0, "S10_1", "Customer A", "555-0101", "Ad1", "Ad2", "NYC", "NY", "10001", "USA", "NA", 
            "Doe", "John", "Small"
        ));

        // Record 2: High Value Sale (UK, 2021, Medium Deal)
        // Sales: 500.0, Qty: 20, Price: 25.0, MSRP: 30.0 (Discounted: Lost 5.0 per item)
        mockData.add(new SalesRecord(
            2, 20, 25.0, 1, 500.0, "5/5/2021", "Shipped", 2, 5, 2021, 
            "Planes", 30.0, "S10_2", "Customer B", "555-0102", "Ad1", "Ad2", "London", "N/A", "SW1", "UK", "EMEA", 
            "Smith", "Jane", "Medium"
        ));

        // Record 3: Top Value Sale (USA, 2022, Large Deal, Disputed)
        // Sales: 1000.0, Qty: 10, Price: 100.0, MSRP: 100.0
        mockData.add(new SalesRecord(
            3, 10, 100.0, 1, 1000.0, "10/10/2022", "Disputed", 4, 10, 2022, 
            "Cars", 100.0, "S10_1", "Customer A", "555-0101", "Ad1", "Ad2", "NYC", "NY", "10001", "USA", "NA", 
            "Doe", "John", "Large"
        ));
        
        // Record 4: Another Rep (France, 2022, Q4)
        // Sales: 400.0, Qty: 4, Price: 100.0, MSRP: 100.0
        mockData.add(new SalesRecord(
            4, 4, 100.0, 1, 400.0, "12/12/2022", "Shipped", 4, 12, 2022, 
            "Ships", 100.0, "S10_3", "Customer C", "555-0103", "Ad1", "Ad2", "Paris", "N/A", "75000", "France", "EMEA", 
            "Bond", "James", "Small"
        ));
    }

    // BASIC METRICS TESTS

    @Test
    void testCalculateTotalSales() {
        // 100 + 500 + 1000 + 400 = 2000
        double result = Assignment_2.calculateTotalSales(mockData);
        assertEquals(2000.0, result, 0.001);
    }

    @Test
    void testGetTotalOrderCount() {
        long result = Assignment_2.getTotalOrderCount(mockData);
        assertEquals(4, result);
    }

    // GROUPING TESTS

    @Test
    void testGetSalesByYear() {
        Map<Integer, Double> result = Assignment_2.getSalesByYear(mockData);
        // 2021: 100 + 500 = 600
        // 2022: 1000 + 400 = 1400
        assertEquals(600.0, result.get(2021), 0.001);
        assertEquals(1400.0, result.get(2022), 0.001);
    }

    @Test
    void testGetSalesByProductLine() {
        Map<String, Double> result = Assignment_2.getSalesByProductLine(mockData);
        // Cars: 100 + 1000 = 1100
        // Planes: 500
        assertEquals(1100.0, result.get("Cars"), 0.001);
        assertEquals(500.0, result.get("Planes"), 0.001);
    }

    @Test
    void testGetSalesByTerritory() {
        Map<String, Double> result = Assignment_2.getSalesByTerritory(mockData);
        // NA: 100 + 1000 = 1100 (Customer A is in NA)
        // EMEA: 500 + 400 = 900
        assertEquals(1100.0, result.get("NA"), 0.001);
        assertEquals(900.0, result.get("EMEA"), 0.001);
    }

    // ORDERING & LIMITING TESTS

    @Test
    void testGetTopNCustomers() {
        // Customer A: 100 + 1000 = 1100
        // Customer B: 500
        // Customer C: 400
        List<Map.Entry<String, Double>> result = Assignment_2.getTopNCustomers(mockData, 2);

        assertEquals(2, result.size());
        assertEquals("Customer A", result.get(0).getKey());
        assertEquals(1100.0, result.get(0).getValue(), 0.001);
        assertEquals("Customer B", result.get(1).getKey());
    }

    @Test
    void testGetTopSalesPeople() {
        // John Doe: 100 + 1000 = 1100
        // Jane Smith: 500
        // James Bond: 400
        List<Map.Entry<String, Double>> result = Assignment_2.getTopSalesPeople(mockData, 1);
        
        assertEquals("John Doe", result.get(0).getKey()); // Tests composite key generation
        assertEquals(1100.0, result.get(0).getValue(), 0.001);
    }

    // FILTERING & SEARCHING TESTS

    @Test
    void testGetSalesByCountry() {
        List<SalesRecord> usaRecords = Assignment_2.getSalesByCountry(mockData, "USA");
        assertEquals(2, usaRecords.size()); // Record 1 and 3
    }

    @Test
    void testHasDisputedOrders() {
        assertTrue(Assignment_2.hasDisputedOrders(mockData)); // Record 3 is Disputed
    }

    @Test
    void testFindFirstHighValueDeal() {
        // Find first deal > 800. Record 3 is 1000.
        Optional<SalesRecord> result = Assignment_2.findFirstHighValueDeal(mockData, 800.0);
        
        assertTrue(result.isPresent());
        assertEquals(1000.0, result.get().getSales(), 0.001);
        assertEquals(3, result.get().getOrderNumber());
    }

    @Test
    void testGetHighestValueSale() {
        Optional<SalesRecord> max = Assignment_2.getHighestValueSale(mockData);
        assertTrue(max.isPresent());
        assertEquals(1000.0, max.get().getSales(), 0.001);
    }

    // COMPLEX CALCULATION TESTS

    @Test
    void testCalculateTotalLostRevenue() {
        // Only Record 2 has a discount.
        // MSRP: 30, Price: 25, Qty: 20
        // Loss = (30 - 25) * 20 = 5 * 20 = 100
        double loss = Assignment_2.calculateTotalLostRevenue(mockData);
        assertEquals(100.0, loss, 0.001);
    }

    @Test
    void testGetBusiestQuarter() {
        // Record 1: Q1
        // Record 2: Q2
        // Record 3: Q4
        // Record 4: Q4
        // Q4 has 2 records, others have 1.
        int busiestQtr = Assignment_2.getBusiestQuarter(mockData);
        assertEquals(4, busiestQtr);
    }

    @Test // Test to get averages sales grouped by deal size
    void testGetAvgSalesByDealSize() {
        Map<String, Double> result = Assignment_2.getAvgSalesByDealSize(mockData);
        
        // Small Deals: Record 1 (100) and Record 4 (400). Avg = 250.
        assertEquals(250.0, result.get("Small"), 0.001);
        
        // Large Deals: Record 3 (1000). Avg = 1000.
        assertEquals(1000.0, result.get("Large"), 0.001);
    }
    
    @Test // Unique Cities present in the Mock Data
    void testGetUniqueCities() {
        List<String> cities = Assignment_2.getUniqueCities(mockData);
        // London, NYC, Paris (Sorted)
        assertEquals(3, cities.size());
        assertEquals("London", cities.get(0));
        assertEquals("NYC", cities.get(1));
        assertEquals("Paris", cities.get(2));
    }
    @Test // Average quantity by status 
    void testGetAvgQuantityByStatus() {
        Map<String, Double> result = Assignment_2.getAvgQuantityByStatus(mockData);

        // Shipped records: qty 10 (rec1), 20 (rec2), 4 (rec4) → (10 + 20 + 4) / 3 = 34/3 ≈ 11.3333
        assertEquals(34.0 / 3.0, result.get("Shipped"), 0.001);

        // Disputed record: qty 10 (rec3) → average = 10
        assertEquals(10.0, result.get("Disputed"), 0.001);

        assertEquals(2, result.size());
    }
    
    @Test // Ensure that it returns optional empty
    void testFindFirstHighValueDeal_NoMatch() {
        // Threshold above any sale in mockData (max is 1000.0)
        Optional<SalesRecord> result = Assignment_2.findFirstHighValueDeal(mockData, 2000.0);

        assertTrue(result.isEmpty(), "Expected no deal to be found above the threshold");
    }
    
    @Test // Case where User inputs N greater than number of records
    void testGetTopNCustomers_NGreaterThanUniqueCustomers() {
        // There are 3 unique customers, but we request top 10
        List<Map.Entry<String, Double>> result = Assignment_2.getTopNCustomers(mockData, 10);

        // Should only return the 3 that actually exist
        assertEquals(3, result.size());

        // Still sorted by revenue descending
        assertEquals("Customer A", result.get(0).getKey());
        assertEquals(1100.0, result.get(0).getValue(), 0.001);
        assertEquals("Customer B", result.get(1).getKey());
        assertEquals("Customer C", result.get(2).getKey());
    }

}