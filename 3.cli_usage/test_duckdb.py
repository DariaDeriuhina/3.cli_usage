import duckdb
import pytest

def connect_to_db():
    con = duckdb.connect('chinook.db')
    return con

def test_customers_from_usa():
    con = connect_to_db()
    query = "SELECT COUNT(*) FROM customers WHERE Country = 'USA';"
    result = con.execute(query).fetchone()
    assert result[0] == 13

def test_customets_columns():
    con = connect_to_db()
    query = "PRAGMA table_info(customers)"
    result = con.execute(query).fetchall()
    column_names = [row[1] for row in result]
    expected_columns = {'CustomerId', 'FirstName', 'LastName', 'Company', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email', 'SupportRepId'}
    assert expected_columns.issubset(column_names), "Missing columns in customers"

def test_customer_email_format():
    con = connect_to_db()
    query = "SELECT Email FROM customers WHERE Country = 'USA';"
    results = con.execute(query).fetchall()
    for email, in results:
        assert '@' in email, "Incorrect format"

def test_unique_customer_ids():
    con = connect_to_db()
    query = "SELECT COUNT(DISTINCT CustomerId) FROM customers;"
    distinct_count = con.execute(query).fetchone()[0]
    query = "SELECT COUNT(CustomerId) FROM customers;"
    total_count = con.execute(query).fetchone()[0]
    assert distinct_count == total_count, "There duplicates"

def test_invalid_query():
    con = connect_to_db()
    with pytest.raises(Exception):
        con.execute("FROM non_exist_table")