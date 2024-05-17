import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect('your_database.db')

# Pure SQL approach
def query_data_with_sql(conn):
    query = """
    SELECT
        c.customer_id,
        c.age,
        i.item_name,
        SUM(COALESCE(o.quantity, 0)) as total_quantity
    FROM
        Customer c
    JOIN
        Sales s ON c.customer_id = s.customer_id
    JOIN
        Orders o ON s.sales_id = o.sales_id
    JOIN
        Items i ON o.item_id = i.item_id
    WHERE
        c.age BETWEEN 18 AND 35
    GROUP BY
        c.customer_id, c.age, i.item_name
    HAVING
        total_quantity > 0
    ORDER BY
        c.customer_id
    """
    result = conn.execute(query)
    rows = result.fetchall()
    result.close()
    return rows


# Store results to CSV file
def store_to_csv(data, filename):
    data.to_csv(filename, sep=';', index=False)

# Main execution
def main():
    # Query using SQL
    sql_results = query_data_with_sql(conn)
    sql_df = pd.DataFrame(sql_results, columns=['Customer', 'Age', 'Item', 'Quantity'])
    store_to_csv(sql_df, 'output_sql.csv')


    print("Data has been written to output_sql.csv and output_pandas.csv")

if __name__ == "__main__":
    main()
