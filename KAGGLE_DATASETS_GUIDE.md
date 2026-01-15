# Kaggle Datasets Guide 📚

This project is compatible with multiple datasets. This guide explains the schema and business value of the recommended datasets.

---

## 🥇 Instacart Market Basket Analysis (Recommended)

**Source:** [Instacart via Kaggle](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis)
**Scale:** 3M+ orders, 50k products.

### The Schema
This is a standard Star Schema structure tailored for retail analytics.

1.  **`aisles`**: (`aisle_id`, `aisle`) - e.g., "baking ingredients".
2.  **`departments`**: (`department_id`, `department`) - e.g., "produce".
3.  **`products`**: (`product_id`, `product_name`, `aisle_id`, `department_id`).
4.  **`orders`**: (`order_id`, `user_id`, `order_number`, `order_dow`, `order_hour_of_day`, `days_since_prior_order`).
5.  **`order_products__prior`**: Mapping table detailing what was in past orders.
6.  **`order_products__train`**: Mapping table for the most recent order (split for ML purposes).

### Why use this for a Portfolio?
*   **Volume**: 3 million rows in `orders` table forces you to think about performance/indexing.
*   **Complexity**: Questions often require joining 4-5 tables (Order -> OrderProduct -> Product -> Aisle -> Dept).
*   **Relatability**: Everyone understands "Top selling organic fruit".

---

## 🥈 Online Retail Dataset (Alternative)

**Source:** [UCI ML Repo via Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)
**Scale:** 500k transactions.

### The Schema
A simple, single-table transaction log.
*   **`online_retail`**: (`InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`)

### Why use this?
*   **Simplicity**: Very easy to set up (no complex joins).
*   **Time Series**: Great for "Sales over time" queries.

---

## 🥉 E-Commerce Sales Data (Backup)

**Source:** Synthetic Sales Data.

If you just need *something* to verify the code works, use a small synthetic dataset. But for a portfolio, **Instacart** is the clear winner.
