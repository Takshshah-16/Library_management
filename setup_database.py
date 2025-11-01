import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="library_db",
        user=os.getenv("USER", "postgres"),
        password=""
    )
    return conn

def create_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user=os.getenv("USER", "postgres"),
            password=""
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'library_db'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute("CREATE DATABASE library_db")
            print("Database 'library_db' created successfully")
        else:
            print("Database 'library_db' already exists")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS return_status CASCADE")
    cur.execute("DROP TABLE IF EXISTS issued_status CASCADE")
    cur.execute("DROP TABLE IF EXISTS books CASCADE")
    cur.execute("DROP TABLE IF EXISTS members CASCADE")
    cur.execute("DROP TABLE IF EXISTS employees CASCADE")
    cur.execute("DROP TABLE IF EXISTS branch CASCADE")
    
    cur.execute("""
        CREATE TABLE branch (
            branch_id VARCHAR(10) PRIMARY KEY,
            manager_id VARCHAR(10),
            branch_address VARCHAR(30),
            contact_no VARCHAR(15)
        )
    """)
    
    cur.execute("""
        CREATE TABLE employees (
            emp_id VARCHAR(10) PRIMARY KEY,
            emp_name VARCHAR(30),
            position VARCHAR(30),
            salary DECIMAL(10,2),
            branch_id VARCHAR(10),
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
        )
    """)
    
    cur.execute("""
        CREATE TABLE members (
            member_id VARCHAR(10) PRIMARY KEY,
            member_name VARCHAR(30),
            member_address VARCHAR(30),
            reg_date DATE
        )
    """)
    
    cur.execute("""
        CREATE TABLE books (
            isbn VARCHAR(50) PRIMARY KEY,
            book_title VARCHAR(80),
            category VARCHAR(30),
            rental_price DECIMAL(10,2),
            status VARCHAR(10),
            author VARCHAR(30),
            publisher VARCHAR(30)
        )
    """)
    
    cur.execute("""
        CREATE TABLE issued_status (
            issued_id VARCHAR(10) PRIMARY KEY,
            issued_member_id VARCHAR(30),
            issued_book_name VARCHAR(80),
            issued_date DATE,
            issued_book_isbn VARCHAR(50),
            issued_emp_id VARCHAR(10),
            FOREIGN KEY (issued_member_id) REFERENCES members(member_id),
            FOREIGN KEY (issued_emp_id) REFERENCES employees(emp_id),
            FOREIGN KEY (issued_book_isbn) REFERENCES books(isbn)
        )
    """)
    
    cur.execute("""
        CREATE TABLE return_status (
            return_id VARCHAR(10) PRIMARY KEY,
            issued_id VARCHAR(30),
            return_book_name VARCHAR(80),
            return_date DATE,
            return_book_isbn VARCHAR(50),
            book_quality VARCHAR(15) DEFAULT 'Good',
            FOREIGN KEY (return_book_isbn) REFERENCES books(isbn)
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("All tables created successfully")

def load_csv_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    csv_files = {
        'branch': 'branch.csv',
        'employees': 'employees.csv',
        'members': 'members.csv',
        'books': 'books.csv',
        'issued_status': 'issued_status.csv',
        'return_status': 'return_status.csv'
    }
    
    for table, csv_file in csv_files.items():
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                for row in reader:
                    placeholders = ','.join(['%s'] * len(row))
                    columns = ','.join(headers)
                    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                    try:
                        cur.execute(query, row)
                    except Exception as e:
                        print(f"Error inserting into {table}: {e}")
                        print(f"Row: {row}")
                
                print(f"Loaded data from {csv_file}")
    
    conn.commit()
    cur.close()
    conn.close()

def create_procedures():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE OR REPLACE PROCEDURE book_issue(
            p_issued_id VARCHAR(10),
            p_issued_member_id VARCHAR(30),
            p_issued_book_isbn VARCHAR(30),
            p_issued_emp_id VARCHAR(30)
        )
        LANGUAGE plpgsql 
        AS $$
        DECLARE
            v_status VARCHAR(10);
        BEGIN
            SELECT status INTO v_status FROM books WHERE isbn = p_issued_book_isbn;
            
            IF v_status = 'yes' THEN
                INSERT INTO issued_status(issued_id, issued_member_id, issued_date, issued_book_isbn, issued_emp_id)
                VALUES (p_issued_id, p_issued_member_id, CURRENT_DATE, p_issued_book_isbn, p_issued_emp_id);
                
                UPDATE books SET status = 'no' WHERE isbn = p_issued_book_isbn;
                
                RAISE NOTICE 'Book issued successfully for ISBN: %', p_issued_book_isbn;
            ELSE
                RAISE NOTICE 'Book not available for ISBN: %', p_issued_book_isbn;
            END IF;
        END;
        $$
    """)
    
    cur.execute("""
        CREATE OR REPLACE PROCEDURE add_return_records(
            p_return_id VARCHAR(10),
            p_issued_id VARCHAR(10),
            p_book_quality VARCHAR(10)
        )
        LANGUAGE plpgsql
        AS $$
        DECLARE
            v_isbn VARCHAR(50);
            v_book_name VARCHAR(80);
        BEGIN
            INSERT INTO return_status(return_id, issued_id, return_date, book_quality)
            VALUES (p_return_id, p_issued_id, CURRENT_DATE, p_book_quality);
            
            SELECT issued_book_isbn, issued_book_name
            INTO v_isbn, v_book_name
            FROM issued_status
            WHERE issued_id = p_issued_id;
            
            UPDATE books SET status = 'yes' WHERE isbn = v_isbn;
            
            RAISE NOTICE 'Thank you for returning the book: %', v_book_name;
        END;
        $$
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Stored procedures created successfully")

if __name__ == "__main__":
    print("Setting up Library Management System Database...")
    create_database()
    create_tables()
    load_csv_data()
    create_procedures()
    print("\nDatabase setup completed successfully!")
