based on https://github.com/jdaarevalo/docker_postgres_with_data

docker-compose down

docker-compose up

# log into image
docker exec -it `docker ps | grep postgres | awk '{print $1;}'` psql -U postgres

# populate

psql -U postgres postgres < /docker-entrypoint-initdb.d/create_tables.sql

psql -U postgres postgres < /docker-entrypoint-initdb.d/fill_tables.sql 

#
psql -U postgres

\dt
SELECT * FROM city LIMIT 2;

DB structure:

![](https://user-images.githubusercontent.com/2475570/106355076-d4025700-62c3-11eb-90e6-41c3ee47c06b.png)

#

#

### EXTRA TABLES + QUESTIONS:

![](sql/5sql_questions.png)

#### Q1: Display the last 100 customers who visited any bank centre and the date of their last visit.

    SELECT Cust_Id, MAX(Visit_Date) FROM Fact_Centre_Txn GROUP BY Cust_Id;

#### Q2: For each customer, display the number of transactions in the bank over the last 60 days.

this misses customers without transactions

    SELECT Cust_Id, COUNT(*)
    FROM Fact_Centre_Txn
    WHERE Visit_Date >= CURRENT_DATE - 60
    GROUP BY Cust_Id;

How select customers with no transactions, this?

    SELECT Cust_Id, COUNT(*) FROM Fact_Centre_Txn WHERE Visit_Date >= CURRENT_DATE - 60 GROUP BY Cust_Id
    UNION
    SELECT Map_Centre_Cust.Cust_Id, 0
    FROM Map_Centre_Cust
    LEFT JOIN Fact_Centre_Txn ON Fact_Centre_Txn.Cust_Id = Map_Centre_Cust.Cust_Id
    WHERE Fact_Centre_Txn.Cust_Id IS NULL AND Fact_Centre_Txn.Visit_Date >= CURRENT_DATE - 6000;

works but is there nicer way?

#### Q3: Produce a list of members who visited the bank more than once in a specific day and show the details of all transactions done in that day.

Specific_date = '2017-01-06 00:00:00'

constants https://stackoverflow.com/questions/13316773/is-there-a-way-to-define-a-named-constant-in-a-postgresql-query

SELECT Cust_Id, Visit_Date, Transaction_Id, Closing_Balance

FROM Fact_Centre_Txn

WHERE Visit_Date >= Specific_date AND Visit_Date < DATEADD(DAY, 1, Specific_Date)

HAVING COUNT(Visit_Date)>1

SELECT TO_DATE('2017-01-06','YYYY-MM-DD');

SELECT Cust_Id, Transaction_Id, Closing_Balance
FROM Fact_Centre_Txn
WHERE Visit_Date >= TO_DATE('2017-01-06','YYYY-MM-DD') AND Visit_Date < TO_DATE('2017-01-06','YYYY-MM-DD') + INTERVAL '1 day'
GROUP BY Cust_Id
HAVING COUNT(Visit_Date)>1;

#### Q4: Display the amount of money kept at each bank centre per day for the current month.
#### Q5: List all bank centres and the number of customers assigned to the centre. In the same output, display the percentage of each centre’s customers with respect to its region.

#### Bonus: From the Q1 result, get the average number of days between the last and second-to-the-last transaction of the last 100 customers who went to the bank.



## SQL Practice Problems 57 beginning, intermediate, and advanced challenges for you to solve using a learn-by-doing approach by Vasilik, Sylvia Moestl

### Northwind init:

(download [northwind-fix.sql](https://github.com/rgerhardt/57-sql-problems))

    docker exec -it `docker ps | grep postgres | awk '{print $1;}'` /bin/bash
    createdb -U postgres northwind
    psql -U postgres northwind < /northwind/northwind.sql
    psql -U postgres northwind < /northwind/northwind-fix.sql

then run:

    ./connect.sh northwind

or run `\c northwind` after `./connect.sh`

![](sql/northwind-er-diagram.png)

## Solutions:

### Introductory Problems

1. Return all the fields from all the shippers


    SELECT * FROM shippers; -- smpl


2. Categories, only two columns, CategoryName and Description.


    SELECT categoryname, description
    FROM categories; /* \d categories */


3. FirstName, LastName, and HireDate of all the employees with the Title of Sales Representative.


    SELECT FirstName, LastName, HireDate
    FROM employees
    WHERE title = 'Sales Representative';


4. Employees that both have the title of Sales Representative, and also are in the United States.


    SELECT FirstName, LastName, HireDate
    FROM employees
    WHERE title = 'Sales Representative' AND country = 'USA';

5. All the orders placed by a specific employee.


    SELECT *
    FROM orders
    WHERE employeeid = 5;

6. In the Suppliers table, show the SupplierID, ContactName, and ContactTitle for those Suppliers whose ContactTitle is not Marketing Manager.


    SELECT SupplierID, ContactName, ContactTitle
    FROM suppliers
    WHERE contacttitle <> 'Marketing Manager';

or WHERE NOT contacttitle = 'Marketing Manager';

7. ProductID and ProductName for those products where the ProductName includes the string “queso”.


    SELECT ProductID, ProductName FROM products
    WHERE ProductName ILIKE '%queso%'; -- ILIKE is case-insensitive   % === *    _ === .


8. OrderID, CustomerID, and ShipCountry for the orders where the ShipCountry is either France or Belgium.


    SELECT OrderID, CustomerID, ShipCountry
    FROM Orders
    WHERE ShipCountry = 'Belgium' OR ShipCountry = 'France';

9. Orders shipping to any country in Latin America.


    SELECT OrderID, CustomerID, ShipCountry
    FROM Orders
    WHERE ShipCountry IN ('Brazil', 'Mexico', 'Argentin', 'Venezuela');

10. For all the employees in the Employees table, show the FirstName, LastName, Title, and BirthDate. Order the results by BirthDate.


    SELECT FirstName, LastName, Title, BirthDate
    FROM Employees
    ORDER BY BirthDate ASC;

11. Previous + show only the date portion of the BirthDate field.


    SELECT FirstName, LastName, Title, DATE(BirthDate)
    FROM Employees
    ORDER BY BirthDate ASC;

13. Employees full name.


    SELECT FirstName, LastName, CONCAT(FirstName, ' ', LastName) as FullName
    FROM Employees;

or: FirstName || ' ' || LastName as FullName

13. In the OrderDetails table, we have the fields UnitPrice and Quantity. Create a new field, TotalPrice, that multiplies these two together.


    SELECT *, UnitPrice * Quantity AS TotalPrice
    FROM Order_Details;

14. How many customers do we have in the Customers table?


    SELECT COUNT(*) FROM Customers;

15. Show the date of the first order ever made in the Orders table.


    SELECT orderdate
    FROM Orders
    WHERE orderdate IS NOT NULL
    ORDER BY orderdate ASC
    LIMIT 1;

OR

    SELECT MIN(orderdate) FROM Orders;

-

INSERT INTO Orders VALUES(11088,'RATTC',1,NULL,NULL,NULL,2,8.53,'Rattlesnake Canyon Grocery','2817 Milton Dr.','city','code','country');

DELETE FROM Orders WHERE orderid = 11088;

16. Countries where there are customers


    SELECT DISTINCT(country) FROM Customers;

or:

    SELECT country FROM Customers GROUP BY country;

17. Show a list of all the different values in the Customers table for ContactTitles. Also include a count for each ContactTitle.


    SELECT ContactTitle, COUNT(*) AS TotalContactTitle
    FROM Customers
    GROUP BY ContactTitle;

18. For each product show the associated Supplier. Show the ProductID, ProductName, and the CompanyName of the Supplier. Sort by ProductID.


    SELECT ProductID, ProductName, CompanyName
    FROM Products
    INNER JOIN Suppliers
    ON Suppliers.SupplierID = Products.SupplierID
    ORDER BY ProductID;

(just 'JOIN' == 'INNER JOIN')

19. Show a list of the Orders that were made, including the Shipper that was used.
Show the OrderID, OrderDate (date only), and CompanyName of the Shipper, and sort by OrderID.
Show only those rows with an OrderID of less than 10300.


    SELECT OrderID, DATE(OrderDate), Shippers.CompanyName
    FROM Orders
    JOIN Shippers
    ON Orders.shipvia = Shippers.shipperid
    WHERE OrderID < 10300
    ORDER BY OrderID;

### Intermediate Problems

20. Total number of products in each category.
Sort the results by the total number of products.


    SELECT categoryname, COUNT(*) AS total
    FROM Products
    JOIN Categories
    ON Products.categoryid = Categories.categoryid
    GROUP BY Categories.categoryname
    ORDER BY total DESC;

21. Show the total number of customers per Country and City.


    SELECT Country, City, COUNT(*)
    FROM Customers
    GROUP BY Country, City;

22. What products do we have in our inventory that should be reordered?
For now, just use the fields UnitsInStock and ReorderLevel, where UnitsInStock is less than the ReorderLevel, ignoring the fields UnitsOnOrder and Discontinued.
Order the results by ProductID.


    SELECT ProductId, ProductName, UnitsInStock, ReorderLevel
    FROM Products
    WHERE UnitsInStock < ReorderLevel
    ORDER BY ProductID;

23. Prev + define “products that need reordering” with the following:
UnitsInStock plus UnitsOnOrder are less than or equal to ReorderLevel
The Discontinued flag is false (0).


    SELECT ProductId, ProductName, UnitsInStock, ReorderLevel
    FROM Products
    WHERE (UnitsInStock + UnitsOnOrder) <= ReorderLevel AND Discontinued = 0
    ORDER BY ProductID;

24. A list of all customers, sorted by region, alphabetically.
Customers with no region (null in the Region field) to be at the end, instead of at the top, where you’d normally find the null values.
Within the same region, companies should be sorted by CustomerID.


    SELECT customerid, Region FROM Customers
    ORDER BY Region, CustomerID;

or reverse

    SELECT customerid, Region FROM Customers
    ORDER BY
    (CASE
        WHEN Region IS NULL THEN 0
        ELSE 1
    END), Region, CustomerID;

25. Return the three ship countries with the highest average freight overall,
 in descending order by average freight.


    SELECT ShipCountry, AVG(freight) AS AvgFreight
    FROM Orders
    GROUP BY ShipCountry
    ORDER BY AvgFreight DESC
    LIMIT 3;

26. Prev + we only want to see orders from the year 2015.


    WHERE extract(year from OrderDate) = 2015

or

    WHERE date_part('year', OrderDate) = 2015

27. High freight charges with between.

does not apply

28. High freight charges - last year.


    SELECT ShipCountry, AVG(freight) AS AvgFreight
    FROM Orders
    WHERE OrderDate > (SELECT MAX(OrderDate) - INTERVAL '1 year' FROM Orders)
    GROUP BY ShipCountry
    ORDER BY AvgFreight DESC
    LIMIT 3;


30. Inventory list.


    SELECT Employees.EmployeeID, LastName, Orders.OrderID, ProductName, Quantity
    FROM Employees
    JOIN Orders
    ON Employees.employeeid = Orders.employeeid
    JOIN order_details
    ON Orders.orderid = order_details.orderid
    JOIN Products
    ON Products.productid = order_details.productid
    ORDER BY Orders.OrderID, Products.productid;

31. Customers with no orders.


    SELECT Customers.CustomerId
    FROM Customers
    LEFT JOIN Orders
    ON Orders.CustomerId = Customers.CustomerId
    WHERE Orders.OrderId IS NULL;

32. Customers with no orders for EmployeeID 4.


    SELECT Customers.CustomerId
    FROM Customers
    LEFT JOIN (SELECT OrderId, CustomerId FROM Orders WHERE Orders.EmployeeID = 4) AS CustomersOfEmployee
    ON Customers.CustomerId = CustomersOfEmployee.CustomerId
    WHERE CustomersOfEmployee.OrderId IS NULL;

Note that with outer joins, the filters on the where clause are applied after the join.

### Advanced Problems

32. High-value customers.

We want to send all of our high-value customers a special VIP gift.
We're defining high-value customers as those who've made at least
1 order with a total value (not including the discount) equal to $10,000 or more.
We only want to consider orders made in the year 1996.


    SELECT CustomerId, OrderId, SUM(Total)
    FROM (
    SELECT DatedOrders.CustomerId, DatedOrders.OrderId, Order_Details.UnitPrice * Order_Details.Quantity AS Total
    FROM (SELECT * FROM Orders WHERE date_part('year', OrderDate) = 1996) AS DatedOrders
    JOIN Order_Details
    ON DatedOrders.OrderId = Order_Details.OrderId
    ) AS subq GROUP BY OrderId, CustomerId
    HAVING SUM(Total) > 10000;

---

    SELECT Customers.CustomerID, Orders.OrderId, SUM(Order_Details.UnitPrice * Order_Details.Quantity)
    FROM Customers
    JOIN Orders
    ON Orders.CustomerId = Customers.CustomerId
    JOIN Order_Details
    ON Orders.OrderId = Order_Details.OrderId
    WHERE date_part('year', OrderDate) = 1996
    GROUP BY Customers.CustomerID, Orders.OrderId
    HAVING SUM(Order_Details.UnitPrice * Order_Details.Quantity) > 10000
    ORDER BY SUM(Order_Details.UnitPrice * Order_Details.Quantity) DESC;

33. s
34. s
35. s
36. s
37. s
38. s
39. s
40. s
41. s
42. s
43. s
44. s
45. s
46. s
47. s
48. s
49. s
50. s
51. s
52. s
53. s
54. s
55. s
56. s
57. s

answers https://github.com/rgerhardt/57-sql-problems
https://github.com/search?q=SQL+Practice+Problems+57

? https://github.com/jonmullins/SQL_Queries