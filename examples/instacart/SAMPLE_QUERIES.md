# Instacart Sample Queries 🛒

These queries are tested on the `instacart.db` schema. Use them for your demo!

## 📊 Tier 1: Sanity Checks (Basic)

**"How many products are in the database?"**
```sql
SELECT count(*) FROM products;
-- Result: 49,688
```

**"List the first 5 departments."**
```sql
SELECT * FROM departments LIMIT 5;
```

**"Show me 5 aisles in 'frozen' department"**
*(Note: Requires JOIN logic)*
```sql
SELECT a.aisle 
FROM aisles a 
JOIN products p ON a.aisle_id = p.aisle_id 
JOIN departments d ON p.department_id = d.department_id
WHERE d.department = 'frozen'
GROUP BY a.aisle_id
LIMIT 5;
```

---

## 📈 Tier 2: Business Insights (Intermediate)

**"Show me the top 10 most ordered products"**
```sql
SELECT p.product_name, COUNT(*) as frequency
FROM order_products__prior op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_id
ORDER BY frequency DESC
LIMIT 10;
-- Result: Bananas are usually #1
```

**"Which department has the most products?"**
```sql
SELECT d.department, COUNT(*) as count
FROM products p
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY count DESC
LIMIT 1;
-- Result: Personal Care or Snacks
```

---

## 🧠 Tier 3: Complex Analytics (Advanced)

**"What are the most popular shopping hours?"**
```sql
SELECT order_hour_of_day, COUNT(*) as order_count
FROM orders
GROUP BY order_hour_of_day
ORDER BY order_hour_of_day;
-- Use this to generate a Line Chart!
```

**"Which products are most likely to be reordered?"**
*(Filter for products with > 1000 orders to remove noise)*
```sql
SELECT p.product_name, 
       AVG(op.reordered) as reorder_rate,
       COUNT(*) as total_orders
FROM order_products__prior op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_id
HAVING total_orders > 1000
ORDER BY reorder_rate DESC
LIMIT 10;
-- Result: Milk, Bananas have high reorder rates
```

**"What is the average days since prior order for each department?"**
```sql
SELECT d.department, AVG(o.days_since_prior_order) as avg_days
FROM orders o
JOIN order_products__prior op ON o.order_id = op.order_id
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY avg_days ASC;
-- Result: Dairy/Produce usually lower (people buy fresh food often)
```
