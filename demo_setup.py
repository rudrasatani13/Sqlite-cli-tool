#!/usr/bin/env python3
"""
Demo setup script to create sample database and data for testing the SQLite CLI tool
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_database():
    """Create a sample database with test data"""
    
    # Connect to database
    conn = sqlite3.connect('sample_data.sqlite')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER,
            city VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_name VARCHAR(100) NOT NULL,
            quantity INTEGER DEFAULT 1,
            price DECIMAL(10,2),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            price DECIMAL(10,2),
            stock_quantity INTEGER DEFAULT 0,
            description TEXT
        )
    ''')
    
    # Sample data for users
    users_data = [
        ('john_doe', 'john@example.com', 28, 'New York'),
        ('jane_smith', 'jane@example.com', 34, 'Los Angeles'),
        ('bob_wilson', 'bob@example.com', 22, 'Chicago'),
        ('alice_brown', 'alice@example.com', 29, 'Houston'),
        ('charlie_davis', 'charlie@example.com', 31, 'Phoenix'),
        ('diana_miller', 'diana@example.com', 26, 'Philadelphia'),
        ('frank_garcia', 'frank@example.com', 35, 'San Antonio'),
        ('grace_rodriguez', 'grace@example.com', 27, 'San Diego'),
        ('henry_martinez', 'henry@example.com', 33, 'Dallas'),
        ('ivy_anderson', 'ivy@example.com', 24, 'San Jose')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, email, age, city) VALUES (?, ?, ?, ?)',
        users_data
    )
    
    # Sample data for products
    products_data = [
        ('Laptop Pro', 'Electronics', 1299.99, 50, 'High-performance laptop for professionals'),
        ('Wireless Mouse', 'Electronics', 29.99, 200, 'Ergonomic wireless mouse'),
        ('Coffee Mug', 'Kitchen', 12.99, 100, 'Ceramic coffee mug with handle'),
        ('Desk Chair', 'Furniture', 199.99, 25, 'Comfortable office chair'),
        ('Notebook Set', 'Stationery', 15.99, 150, 'Set of 3 lined notebooks'),
        ('Water Bottle', 'Sports', 24.99, 75, 'Insulated stainless steel water bottle'),
        ('Bluetooth Speaker', 'Electronics', 79.99, 60, 'Portable Bluetooth speaker'),
        ('Plant Pot', 'Garden', 18.99, 40, 'Ceramic plant pot with drainage'),
        ('Desk Lamp', 'Furniture', 45.99, 30, 'LED desk lamp with adjustable brightness'),
        ('Phone Case', 'Electronics', 19.99, 120, 'Protective phone case')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO products (name, category, price, stock_quantity, description) VALUES (?, ?, ?, ?, ?)',
        products_data
    )
    
    # Generate sample orders
    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT id, name, price FROM products')
    products = cursor.fetchall()
    
    orders_data = []
    for _ in range(50):  # Generate 50 random orders
        user_id = random.choice(user_ids)
        product = random.choice(products)
        product_id, product_name, price = product
        quantity = random.randint(1, 5)
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        order_date = datetime.now() - timedelta(days=days_ago)
        
        orders_data.append((user_id, product_name, quantity, price, order_date))
    
    cursor.executemany(
        'INSERT INTO orders (user_id, product_name, quantity, price, order_date) VALUES (?, ?, ?, ?, ?)',
        orders_data
    )
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print("✅ Sample database 'sample_data.sqlite' created successfully!")
    print("📊 Sample data includes:")
    print("  • 10 users")
    print("  • 10 products")
    print("  • 50 random orders")
    print("\n🚀 You can now test the CLI with:")
    print("  python sqlcli.py")
    print("  sqlcli> connect sample_data.sqlite")

if __name__ == '__main__':
    create_sample_database()
