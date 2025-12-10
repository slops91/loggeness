package com.assignments;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Assignment_2 {

    private static final String CSV_PATH = "src/sales_data_sample.csv"; // Specifying path of csv file
    public static void main(String[] args) {
        try { // put in a try and catch block to deal with file reading errors
            System.out.println("--- Loading Data ---");
            List<SalesRecord> records = loadSalesData(CSV_PATH);
            
            if (records.isEmpty()) {
                System.out.println("No records found. Check CSV path.");
                return;
            }
            System.out.println("Loaded " + records.size() + " records successfully.\n");

            // EXECUTING ANALYTICAL QUERIES

            // 1. Total Sales
            System.out.println("1. Total Sales: $" + String.format("%.2f", calculateTotalSales(records)));

            // 2. Total Order Count
            System.out.println("2. Total Orders: " + getTotalOrderCount(records));

            // 3. Sales By Year
            System.out.println("3. Sales by Year: " + getSalesByYear(records));

            // 4. Sales By Product Line (Top 3 shown)
            System.out.println("4. Sales by Product Line: " + getSalesByProductLine(records));

            // 5. Avg Quantity by Status
            System.out.println("5. Avg Qty per Status: " + getAvgQuantityByStatus(records));

            // 6. Top 3 Customers (Complex Grouping + Sorting)
            System.out.println("6. Top 3 Customers by Revenue:");
            getTopNCustomers(records, 3)
                .forEach(e -> System.out.println("   - " + e.getKey() + ": $" + String.format("%.2f", e.getValue())));

            // 7. Highest Value Single Sale (Max)
            System.out.println("7. Highest Value Sale: " + 
                getHighestValueSale(records)
                    .map(r -> "$" + r.getSales() + " (Order #" + r.getOrderNumber() + ")")
                    .orElse("N/A"));

            // 8. Filter by Country (e.g., 'USA')
            long usaCount = getSalesByCountry(records, "USA").size();
            System.out.println("8. Count of Sales in USA: " + usaCount);

            // 9. Unique Cities (Distinct)
            List<String> cities = getUniqueCities(records);
            System.out.println("9. Unique Cities (First 5): " + cities.subList(0, Math.min(cities.size(), 5)));

            // 10. Check for Disputed Orders (AnyMatch)
            System.out.println("10. Any Disputed Orders? " + hasDisputedOrders(records));

            // 11. Find FIRST High Value Deal (findFirst)
            System.out.println("11. First Deal > $5000: " + 
                findFirstHighValueDeal(records, 5000)
                    .map(r -> "Order #" + r.getOrderNumber() + " ($" + r.getSales() + ")")
                    .orElse("None found"));
            System.out.println("\n12. Sales by Territory:");
            getSalesByTerritory(records).forEach((k, v) -> System.out.println("   - " + k + ": " + String.format("%.2f", v)));

            // 13. Avg Sales by Deal Size (Uses 'dealSize')
            System.out.println("\n13. Avg Sales by Deal Size: " + getAvgSalesByDealSize(records));

            // 14. Top Sales Reps (Uses Composite 'getContactFullName')
            System.out.println("\n14. Top 3 Sales Reps (Contact Person):");
            getTopSalesPeople(records, 3).forEach(e -> System.out.println("   - " + e.getKey() + ": " + String.format("%.2f", e.getValue())));

            // 15. Total Discount Given (Uses 'msrp', 'priceEach', 'quantity')
            // Insight: How much money did we 'lose' by selling below MSRP?
            System.out.println("\n15. Total Discount Given vs MSRP: $" + String.format("%.2f", calculateTotalLostRevenue(records)));

            // 16. Busiest Quarter (Uses 'qtrId')
            System.out.println("\n16. Busiest Quarter (by Volume): Q" + getBusiestQuarter(records));

        } catch (IOException e) {
            System.err.println("Error reading CSV: " + e.getMessage());
        }
    }

    // ANALYTICAL STATIC METHODS, Actual Implementation of the static methods used for the static queries

    // 1. Calculate Total Sales (Sum)
    public static double calculateTotalSales(List<SalesRecord> records) {
        return records.stream() // gets the Sales value from each record and returns the total sum
                .mapToDouble(SalesRecord::getSales)
                .sum();
    }

    // 2. Count Total Orders
    public static long getTotalOrderCount(List<SalesRecord> records) {
        return records.stream().count(); // Converts into stream of elements and gets the total count of orders
    }

    // 3. Get Sales Grouped by Year
    public static Map<Integer, Double> getSalesByYear(List<SalesRecord> records) {
        return records.stream() // Gets Total Sales grouped by Year
                .collect(Collectors.groupingBy(
                        SalesRecord::getYearId,
                        Collectors.summingDouble(SalesRecord::getSales)
                ));
    }

    // 4. Get Sales Grouped by Product Line
    public static Map<String, Double> getSalesByProductLine(List<SalesRecord> records) {
        return records.stream() // Gets Total Sales grouped by Product Line
                .collect(Collectors.groupingBy(
                        SalesRecord::getProductLine,
                        Collectors.summingDouble(SalesRecord::getSales)
                ));
    }

    // 5. Average Quantity Ordered by Status
    public static Map<String, Double> getAvgQuantityByStatus(List<SalesRecord> records) {
        return records.stream() // Gets Quantity ordered by Status
                .collect(Collectors.groupingBy(
                        SalesRecord::getStatus,
                        Collectors.averagingInt(SalesRecord::getQuantityOrdered)
                ));
    }

    // 6. Get Top N Customers by Revenue
    public static List<Map.Entry<String, Double>> getTopNCustomers(List<SalesRecord> records, int n) {
        return records.stream() // Gets Top N Customers by Revenue, N is given by User
                .collect(Collectors.groupingBy(
                        SalesRecord::getCustomerName,
                        Collectors.summingDouble(SalesRecord::getSales)
                ))
                .entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(n)
                .collect(Collectors.toList());
    }

    // 7. Find Highest Value Sale Record, uses Optional to deal with the edge case there is no maximum
    public static Optional<SalesRecord> getHighestValueSale(List<SalesRecord> records) {
        return records.stream() // Gets Highest Sales Value
                .max(Comparator.comparingDouble(SalesRecord::getSales));
    }

    // 8. Find All Sales from a Specific Country
    public static List<SalesRecord> getSalesByCountry(List<SalesRecord> records, String country) {
        return records.stream() // Gets Sales from a Specific Country
                .filter(r -> r.getCountry().equalsIgnoreCase(country))
                .collect(Collectors.toList());
    }

    // 9. Get Unique Cities List
    public static List<String> getUniqueCities(List<SalesRecord> records) {
        return records.stream() // Gets all the cities that are unique in the CSV File
                .map(SalesRecord::getCity)
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }

    // 10. Check if any order exists with 'Disputed' status
    public static boolean hasDisputedOrders(List<SalesRecord> records) {
        return records.stream() // Checks if there is any order with status as disputed
                .anyMatch(r -> "Disputed".equalsIgnoreCase(r.getStatus()));
    }

    // 11. Find First deal over a certain amount (findFirst)
    public static Optional<SalesRecord> findFirstHighValueDeal(List<SalesRecord> records, double threshold) {
        return records.stream() // Find the first deal over a specific threshold
                .filter(r -> r.getSales() > threshold)
                .findFirst(); 
    }

    // 12. Sales by Territory
    public static Map<String, Double> getSalesByTerritory(List<SalesRecord> records) {
        return records.stream() // Gets the sales grouped by territory
                .collect(Collectors.groupingBy(
                        SalesRecord::getTerritory,
                        Collectors.summingDouble(SalesRecord::getSales)
                ));
    }

    // 13. Average Sales by Deal Size
    public static Map<String, Double> getAvgSalesByDealSize(List<SalesRecord> records) {
        return records.stream() // Gets the sales grouped by deal size according to CSV File
                .collect(Collectors.groupingBy(
                        SalesRecord::getDealSize,
                        Collectors.averagingDouble(SalesRecord::getSales)
                ));
    }

    // 14. Top Sales People
    public static List<Map.Entry<String, Double>> getTopSalesPeople(List<SalesRecord> records, int n) {
        return records.stream() // Gets the Top Sales People limited upto n value
                .collect(Collectors.groupingBy(
                        SalesRecord::getContactFullName,
                        Collectors.summingDouble(SalesRecord::getSales)
                ))
                .entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(n)
                .collect(Collectors.toList());
    }

    // 15. Calculate "Lost Revenue" (Discounts)
    public static double calculateTotalLostRevenue(List<SalesRecord> records) {
        return records.stream() // Gets the total amount lost by discounts using the formula: (MSRP - PriceEach) * Quantity
                .mapToDouble(r -> (r.getMsrp() - r.getPriceEach()) * r.getQuantityOrdered())
                .sum();
    }

    // 16. Find Busiest Quarter (returns the QTR_ID)
    public static int getBusiestQuarter(List<SalesRecord> records) {
        return records.stream() // Gets the quarter where usually sales are the most over years
                .collect(Collectors.groupingBy(SalesRecord::getQtrId, Collectors.counting()))
                .entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(0);
    }

    // Method to deal with Loading Sales Data from CSV File
    private static List<SalesRecord> loadSalesData(String path) throws IOException {
        // Uses ISO_8859_1 to handle special characters
        try (Stream<String> lines = Files.lines(Paths.get(path), StandardCharsets.ISO_8859_1)) {
            return lines
                    .skip(1) // skip header
                    .map(Assignment_2::parseLineSafely)
                    .flatMap(Optional::stream)
                    .collect(Collectors.toList());
        }
    }
    // Uses Optional to prevent Null Pointer Exception, deals with missing values
    private static Optional<SalesRecord> parseLineSafely(String line) {
        if (line == null || line.trim().isEmpty()) return Optional.empty();
        String[] parts = line.split(",", -1);
        if (parts.length < 25) return Optional.empty();

        try {
            int orderNumber        = Integer.parseInt(parts[0].trim());
            int quantityOrdered    = Integer.parseInt(parts[1].trim());
            double priceEach       = Double.parseDouble(parts[2].trim());
            int orderLineNumber    = Integer.parseInt(parts[3].trim());
            double sales           = Double.parseDouble(parts[4].trim());
            String orderDate       = parts[5].trim();
            String status          = parts[6].trim();
            int qtrId              = Integer.parseInt(parts[7].trim());
            int monthId            = Integer.parseInt(parts[8].trim());
            int yearId             = Integer.parseInt(parts[9].trim());
            String productLine     = parts[10].trim();
            double msrp            = Double.parseDouble(parts[11].trim());
            String productCode     = parts[12].trim();
            String customerName    = parts[13].trim();
            String phone           = parts[14].trim();
            String addressLine1    = parts[15].trim();
            String addressLine2    = parts[16].trim();
            String city            = parts[17].trim();
            String state           = parts[18].trim();
            String postalCode      = parts[19].trim();
            String country         = parts[20].trim();
            String territory       = parts[21].trim();
            String contactLastName = parts[22].trim();
            String contactFirstName= parts[23].trim();
            String dealSize        = parts[24].trim();

            return Optional.of(new SalesRecord(
                    orderNumber, quantityOrdered, priceEach, orderLineNumber, sales,
                    orderDate, status, qtrId, monthId, yearId, productLine, msrp,
                    productCode, customerName, phone, addressLine1, addressLine2,
                    city, state, postalCode, country, territory,
                    contactLastName, contactFirstName, dealSize
            ));
        } catch (NumberFormatException ex) { // To deal with incorrect input in CSV File, Text where Number should be 
            return Optional.empty();
        }
    }
}

// DATA MODEL CLASS, Class is a blueprint holding the data of one row

class SalesRecord {
    private final int orderNumber; // Ensure that the data is immutable, cannot be changed after creation
    private final int quantityOrdered;
    private final double priceEach;
    private final int orderLineNumber;
    private final double sales;
    private final String orderDate;
    private final String status;
    private final int qtrId;
    private final int monthId;
    private final int yearId;
    private final String productLine;
    private final double msrp;
    private final String productCode;
    private final String customerName;
    private final String phone;
    private final String addressLine1;
    private final String addressLine2;
    private final String city;
    private final String state;
    private final String postalCode;
    private final String country;
    private final String territory;
    private final String contactLastName;
    private final String contactFirstName;
    private final String dealSize;

    public SalesRecord(int orderNumber, int quantityOrdered, double priceEach,
                       int orderLineNumber, double sales, String orderDate,
                       String status, int qtrId, int monthId, int yearId,
                       String productLine, double msrp, String productCode,
                       String customerName, String phone, String addressLine1,
                       String addressLine2, String city, String state,
                       String postalCode, String country, String territory,
                       String contactLastName, String contactFirstName,
                       String dealSize) {
        this.orderNumber = orderNumber;
        this.quantityOrdered = quantityOrdered;
        this.priceEach = priceEach;
        this.orderLineNumber = orderLineNumber;
        this.sales = sales;
        this.orderDate = orderDate;
        this.status = status;
        this.qtrId = qtrId;
        this.monthId = monthId;
        this.yearId = yearId;
        this.productLine = productLine;
        this.msrp = msrp;
        this.productCode = productCode;
        this.customerName = customerName;
        this.phone = phone;
        this.addressLine1 = addressLine1;
        this.addressLine2 = addressLine2;
        this.city = city;
        this.state = state;
        this.postalCode = postalCode;
        this.country = country;
        this.territory = territory;
        this.contactLastName = contactLastName;
        this.contactFirstName = contactFirstName;
        this.dealSize = dealSize;
    }

    // Getters needed for Analytical Methods
    public int getOrderNumber() { return orderNumber; }
    public int getQuantityOrdered() { return quantityOrdered; }
    public double getPriceEach() { return priceEach; }
    public int getOrderLineNumber() { return orderLineNumber; }
    public double getSales() { return sales; }
    public String getOrderDate() { return orderDate; }
    public String getStatus() { return status; }
    public int getQtrId() { return qtrId; }
    public int getMonthId() { return monthId; }
    public int getYearId() { return yearId; }
    public String getProductLine() { return productLine; }
    public double getMsrp() { return msrp; }
    public String getProductCode() { return productCode; }
    public String getCustomerName() { return customerName; }
    public String getPhone() { return phone; }
    public String getAddressLine1() { return addressLine1; }
    public String getAddressLine2() { return addressLine2; }
    public String getCity() { return city; }
    public String getState() { return state; }
    public String getPostalCode() { return postalCode; }
    public String getCountry() { return country; }
    public String getTerritory() { return territory; }
    public String getContactLastName() { return contactLastName; }
    public String getContactFirstName() { return contactFirstName; }
    public String getDealSize() { return dealSize; }

    //Getter Functions for Composite Attributes

    // Combines First + Last Name for easier reporting
    public String getContactFullName() {
        return contactFirstName + " " + contactLastName;
    }

    // Combines City + Country for Geographic grouping
    public String getGeoLocation() {
        return city + ", " + country;
    }

    // Returns a readable Quarter string (e.g., "2003-Q4")
    public String getQuarterLabel() {
        return yearId + "-Q" + qtrId;
    }
}


