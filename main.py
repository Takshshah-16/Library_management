import psycopg2
import os
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="/tmp/postgresql",
            database="library_db",
            user=os.getenv("USER", "runner"),
            password=""
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            cur.close()
            conn.close()
            return columns, results
        else:
            conn.commit()
            cur.close()
            conn.close()
            return "Query executed successfully"
    except Exception as e:
        conn.close()
        return f"Error: {e}"

def display_menu():
    print("\n" + "="*70)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("="*70)
    print("\n1.  View all books")
    print("2.  View all members")
    print("3.  View all employees")
    print("4.  View all branches")
    print("5.  View issued books")
    print("6.  View returned books")
    print("7.  View available books")
    print("8.  View overdue books (>30 days)")
    print("9.  View branch performance report")
    print("10. View active members (last 6 months)")
    print("11. Issue a book")
    print("12. Return a book")
    print("13. Search books by title")
    print("14. Search books by author")
    print("15. Search books by category")
    print("0.  Exit")
    print("="*70)

def view_all_books():
    query = "SELECT * FROM books ORDER BY book_title"
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No books found")

def view_all_members():
    query = "SELECT * FROM members ORDER BY member_name"
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No members found")

def view_all_employees():
    query = "SELECT * FROM employees ORDER BY emp_name"
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No employees found")

def view_all_branches():
    query = "SELECT * FROM branch"
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No branches found")

def view_issued_books():
    query = """
        SELECT ist.issued_id, m.member_name, b.book_title, ist.issued_date, e.emp_name
        FROM issued_status ist
        JOIN members m ON ist.issued_member_id = m.member_id
        JOIN books b ON ist.issued_book_isbn = b.isbn
        JOIN employees e ON ist.issued_emp_id = e.emp_id
        ORDER BY ist.issued_date DESC
    """
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No issued books found")

def view_returned_books():
    query = """
        SELECT rs.return_id, rs.return_book_name, rs.return_date, rs.book_quality
        FROM return_status rs
        ORDER BY rs.return_date DESC
    """
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No returned books found")

def view_available_books():
    query = "SELECT * FROM books WHERE status = 'yes' ORDER BY book_title"
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No available books found")

def view_overdue_books():
    query = """
        SELECT ist.issued_member_id, m.member_name, b.book_title, ist.issued_date,
               CURRENT_DATE - ist.issued_date as days_overdue
        FROM issued_status ist
        JOIN members m ON ist.issued_member_id = m.member_id
        JOIN books b ON b.isbn = ist.issued_book_isbn
        LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
        WHERE rs.return_id IS NULL
        AND (CURRENT_DATE - ist.issued_date) > 30
        ORDER BY days_overdue DESC
    """
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No overdue books found")

def view_branch_performance():
    query = """
        SELECT b.branch_id, b.manager_id, b.branch_address,
               COUNT(ist.issued_id) as books_issued,
               COUNT(rs.return_id) as books_returned,
               SUM(bk.rental_price) as total_revenue
        FROM branch b
        LEFT JOIN employees e ON b.branch_id = e.branch_id
        LEFT JOIN issued_status ist ON ist.issued_emp_id = e.emp_id
        LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
        LEFT JOIN books bk ON ist.issued_book_isbn = bk.isbn
        GROUP BY b.branch_id, b.manager_id, b.branch_address
    """
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No data found")

def view_active_members():
    query = """
        SELECT DISTINCT m.member_id, m.member_name, m.member_address, m.reg_date
        FROM members m
        JOIN issued_status ist ON m.member_id = ist.issued_member_id
        WHERE ist.issued_date > CURRENT_DATE - INTERVAL '6 months'
        ORDER BY m.member_name
    """
    columns, results = execute_query(query)
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No active members found")

def issue_book():
    print("\n--- Issue a Book ---")
    issued_id = input("Enter issued ID (e.g., IS160): ")
    member_id = input("Enter member ID: ")
    book_isbn = input("Enter book ISBN: ")
    emp_id = input("Enter employee ID: ")
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("CALL book_issue(%s, %s, %s, %s)", 
                   (issued_id, member_id, book_isbn, emp_id))
        conn.commit()
        print("Book issue processed successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        conn.close()

def return_book():
    print("\n--- Return a Book ---")
    return_id = input("Enter return ID (e.g., RS160): ")
    issued_id = input("Enter issued ID: ")
    book_quality = input("Enter book quality (Good/Damaged): ")
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("CALL add_return_records(%s, %s, %s)", 
                   (return_id, issued_id, book_quality))
        conn.commit()
        print("Book return processed successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        conn.close()

def search_books_by_title():
    title = input("Enter book title to search: ")
    query = "SELECT * FROM books WHERE book_title ILIKE %s"
    columns, results = execute_query(query, (f"%{title}%",))
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No books found")

def search_books_by_author():
    author = input("Enter author name to search: ")
    query = "SELECT * FROM books WHERE author ILIKE %s"
    columns, results = execute_query(query, (f"%{author}%",))
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No books found")

def search_books_by_category():
    category = input("Enter category to search: ")
    query = "SELECT * FROM books WHERE category ILIKE %s"
    columns, results = execute_query(query, (f"%{category}%",))
    if results:
        print("\n" + tabulate(results, headers=columns, tablefmt="grid"))
    else:
        print("No books found")

def main():
    print("\nWelcome to Library Management System!")
    print("Initializing...")
    
    conn = get_db_connection()
    if not conn:
        print("\nDatabase not initialized. Please run 'python setup_database.py' first.")
        return
    conn.close()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            view_all_books()
        elif choice == '2':
            view_all_members()
        elif choice == '3':
            view_all_employees()
        elif choice == '4':
            view_all_branches()
        elif choice == '5':
            view_issued_books()
        elif choice == '6':
            view_returned_books()
        elif choice == '7':
            view_available_books()
        elif choice == '8':
            view_overdue_books()
        elif choice == '9':
            view_branch_performance()
        elif choice == '10':
            view_active_members()
        elif choice == '11':
            issue_book()
        elif choice == '12':
            return_book()
        elif choice == '13':
            search_books_by_title()
        elif choice == '14':
            search_books_by_author()
        elif choice == '15':
            search_books_by_category()
        elif choice == '0':
            print("\nThank you for using Library Management System!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
