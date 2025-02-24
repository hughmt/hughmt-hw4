#!/usr/bin/env python3
import sqlite3
import csv
import sys

def csv_to_sqlite(db_name, csv_file):
    # Connect to SQLite database (create if not exists)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Read CSV file
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        
        # Get headers from first row
        headers = next(csv_reader)
        
        # Create table name from CSV filename (remove path and extension)
        table_name = csv_file.split('/')[-1].rsplit('.', 1)[0]
        
        # Create SQL create table statement
        create_table_sql = f"CREATE TABLE {table_name} ({', '.join(f'{header} TEXT' for header in headers)})"
        
        # Create table
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(create_table_sql)
        
        # Insert data
        placeholders = ','.join(['?' for _ in headers])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        # Insert rows
        cursor.executemany(insert_sql, csv_reader)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 csv_to_sqlite.py <database_name> <csv_file>")
        sys.exit(1)
        
    db_name = sys.argv[1]
    csv_file = sys.argv[2]
    
    try:
        csv_to_sqlite(db_name, csv_file)
        print(f"Successfully imported {csv_file} into {db_name}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
