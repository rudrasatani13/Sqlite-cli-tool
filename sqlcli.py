#!/usr/bin/env python3
"""
SQLite CLI Tool - A comprehensive command-line interface for SQLite database interaction
"""

import sqlite3
import csv
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import cmd
import shlex
import textwrap

class SQLiteCLI(cmd.Cmd):
    """Interactive SQLite CLI tool"""
    
    intro = """
╔══════════════════════════════════════════════════════════════╗
║                    SQLite CLI Tool v1.0                      ║
║              Professional Database Interaction               ║
╚══════════════════════════════════════════════════════════════╝

Type 'help' or '?' to list commands.
Type 'connect <database>' to start working with a database.
    """
    
    prompt = 'sqlcli> '
    
    def __init__(self):
        super().__init__()
        self.connection: Optional[sqlite3.Connection] = None
        self.database_path: Optional[str] = None
        self.query_history: List[Dict[str, Any]] = []
        self.last_results: List[Dict[str, Any]] = []
        self.page_size = 20
        
    def do_connect(self, args):
        """Connect to a SQLite database
        Usage: connect <database_path>
        Example: connect mydata.sqlite
        """
        if not args:
            print("❌ Error: Please specify a database path")
            print("Usage: connect <database_path>")
            return
            
        database_path = args.strip()
        
        try:
            # Close existing connection if any
            if self.connection:
                self.connection.close()
                
            # Create directory if it doesn't exist
            db_dir = os.path.dirname(database_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            # Connect to database
            self.connection = sqlite3.connect(database_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            self.database_path = database_path
            
            # Test connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            
            print(f"✅ Connected to: {database_path}")
            print(f"📊 SQLite version: {version}")
            
            # Show available tables
            self._show_tables()
            
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def do_query(self, args):
        """Execute a SQL query
        Usage: query <SQL_STATEMENT>
        Example: query SELECT * FROM users WHERE age > 25
        """
        if not self.connection:
            print("❌ Error: No database connection. Use 'connect <database>' first.")
            return
            
        if not args:
            print("❌ Error: Please provide a SQL query")
            print("Usage: query <SQL_STATEMENT>")
            return
            
        sql_query = args.strip()
        
        try:
            cursor = self.connection.cursor()
            start_time = datetime.now()
            
            cursor.execute(sql_query)
            
            # Handle different query types
            if sql_query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Convert to list of dictionaries for easier handling
                self.last_results = [dict(row) for row in results]
                
                # Add to history
                self.query_history.append({
                    'query': sql_query,
                    'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'execution_time': execution_time,
                    'row_count': len(results)
                })
                
                # Display results
                self._display_results(self.last_results, execution_time)
                
            else:
                # For INSERT, UPDATE, DELETE operations
                self.connection.commit()
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                rows_affected = cursor.rowcount
                
                # Add to history
                self.query_history.append({
                    'query': sql_query,
                    'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'execution_time': execution_time,
                    'rows_affected': rows_affected
                })
                
                print(f"✅ Query executed successfully")
                print(f"📊 Rows affected: {rows_affected}")
                print(f"⏱️  Execution time: {execution_time:.3f}s")
                
        except sqlite3.Error as e:
            print(f"❌ SQL Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def do_save(self, args):
        """Save last query results to file
        Usage: save <filename> [format]
        Formats: csv, json, txt (default: csv)
        Example: save results.csv
        Example: save data.json json
        """
        if not self.last_results:
            print("❌ Error: No results to save. Execute a SELECT query first.")
            return
            
        if not args:
            print("❌ Error: Please specify a filename")
            print("Usage: save <filename> [format]")
            return
            
        parts = args.strip().split()
        filename = parts[0]
        format_type = parts[1].lower() if len(parts) > 1 else 'csv'
        
        if format_type not in ['csv', 'json', 'txt']:
            print("❌ Error: Unsupported format. Use: csv, json, or txt")
            return
            
        try:
            if format_type == 'csv':
                self._save_csv(filename)
            elif format_type == 'json':
                self._save_json(filename)
            elif format_type == 'txt':
                self._save_txt(filename)
                
            print(f"✅ Results saved to: {filename}")
            print(f"📊 Records saved: {len(self.last_results)}")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def do_history(self, args):
        """Show query history
        Usage: history [limit]
        Example: history 10
        """
        if not self.query_history:
            print("📝 No query history available")
            return
            
        limit = None
        if args:
            try:
                limit = int(args.strip())
            except ValueError:
                print("❌ Error: Invalid limit number")
                return
                
        history_to_show = self.query_history[-limit:] if limit else self.query_history
        
        print("\n📝 Query History:")
        print("=" * 80)
        
        for i, entry in enumerate(history_to_show, 1):
            print(f"\n{i}. [{entry['timestamp']}]")
            print(f"   Query: {entry['query'][:60]}{'...' if len(entry['query']) > 60 else ''}")
            print(f"   Time: {entry['execution_time']:.3f}s", end="")
            
            if 'row_count' in entry:
                print(f" | Rows: {entry['row_count']}")
            elif 'rows_affected' in entry:
                print(f" | Affected: {entry['rows_affected']}")
            else:
                print()
    
    def do_tables(self, args):
        """Show all tables in the database
        Usage: tables
        """
        if not self.connection:
            print("❌ Error: No database connection. Use 'connect <database>' first.")
            return
            
        self._show_tables()
    
    def do_describe(self, args):
        """Describe table structure
        Usage: describe <table_name>
        Example: describe users
        """
        if not self.connection:
            print("❌ Error: No database connection. Use 'connect <database>' first.")
            return
            
        if not args:
            print("❌ Error: Please specify a table name")
            print("Usage: describe <table_name>")
            return
            
        table_name = args.strip()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            if not columns:
                print(f"❌ Table '{table_name}' not found")
                return
                
            print(f"\n📋 Table: {table_name}")
            print("=" * 60)
            print(f"{'Column':<20} {'Type':<15} {'Null':<8} {'Default':<15} {'PK'}")
            print("-" * 60)
            
            for col in columns:
                cid, name, col_type, not_null, default_val, pk = col
                null_str = "NO" if not_null else "YES"
                default_str = str(default_val) if default_val is not None else ""
                pk_str = "YES" if pk else ""
                
                print(f"{name:<20} {col_type:<15} {null_str:<8} {default_str:<15} {pk_str}")
                
        except sqlite3.Error as e:
            print(f"❌ SQL Error: {e}")
    
    def do_pagesize(self, args):
        """Set page size for result display
        Usage: pagesize <number>
        Example: pagesize 50
        """
        if not args:
            print(f"📄 Current page size: {self.page_size}")
            return
            
        try:
            new_size = int(args.strip())
            if new_size < 1:
                print("❌ Error: Page size must be greater than 0")
                return
                
            self.page_size = new_size
            print(f"✅ Page size set to: {new_size}")
            
        except ValueError:
            print("❌ Error: Invalid page size number")
    
    def do_clear(self, args):
        """Clear the screen
        Usage: clear
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def do_status(self, args):
        """Show connection status and statistics
        Usage: status
        """
        print("\n📊 Connection Status:")
        print("=" * 40)
        
        if self.connection:
            print(f"✅ Connected to: {self.database_path}")
            print(f"📝 Queries executed: {len(self.query_history)}")
            print(f"📄 Page size: {self.page_size}")
            
            if self.last_results:
                print(f"📋 Last result count: {len(self.last_results)}")
        else:
            print("❌ No database connection")
    
    def do_exit(self, args):
        """Exit the CLI tool
        Usage: exit
        """
        return self.do_quit(args)
    
    def do_quit(self, args):
        """Quit the CLI tool
        Usage: quit
        """
        if self.connection:
            self.connection.close()
            print("👋 Database connection closed.")
        print("Goodbye!")
        return True
    
    def _show_tables(self):
        """Display all tables in the database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n📋 Available tables ({len(tables)}):")
                for table in tables:
                    print(f"  • {table[0]}")
            else:
                print("📋 No tables found in database")
                
        except sqlite3.Error as e:
            print(f"❌ Error retrieving tables: {e}")
    
    def _display_results(self, results: List[Dict[str, Any]], execution_time: float):
        """Display query results with pagination"""
        if not results:
            print("📊 No results found")
            print(f"⏱️  Execution time: {execution_time:.3f}s")
            return
            
        print(f"\n📊 Query Results ({len(results)} rows)")
        print(f"⏱️  Execution time: {execution_time:.3f}s")
        print("=" * 80)
        
        # Get column names
        columns = list(results[0].keys())
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = max(
                len(str(col)),
                max(len(str(row.get(col, ''))) for row in results[:self.page_size])
            )
            # Limit column width to 30 characters
            col_widths[col] = min(col_widths[col], 30)
        
        # Display results in pages
        for page_start in range(0, len(results), self.page_size):
            page_end = min(page_start + self.page_size, len(results))
            page_results = results[page_start:page_end]
            
            # Print header
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            print(header)
            print("-" * len(header))
            
            # Print rows
            for row in page_results:
                row_str = " | ".join(
                    str(row.get(col, ''))[:col_widths[col]].ljust(col_widths[col])
                    for col in columns
                )
                print(row_str)
            
            # Show pagination info
            if len(results) > self.page_size:
                print(f"\nShowing rows {page_start + 1}-{page_end} of {len(results)}")
                
                if page_end < len(results):
                    response = input("Press Enter for next page, 'q' to quit viewing: ")
                    if response.lower() == 'q':
                        break
                    print()
    
    def _save_csv(self, filename: str):
        """Save results to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if self.last_results:
                fieldnames = self.last_results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.last_results)
    
    def _save_json(self, filename: str):
        """Save results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.last_results, jsonfile, indent=2, default=str)
    
    def _save_txt(self, filename: str):
        """Save results to text file"""
        with open(filename, 'w', encoding='utf-8') as txtfile:
            if not self.last_results:
                txtfile.write("No results to save\n")
                return
                
            # Write header
            columns = list(self.last_results[0].keys())
            col_widths = {col: max(len(str(col)), 
                                 max(len(str(row.get(col, ''))) for row in self.last_results))
                         for col in columns}
            
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            txtfile.write(header + "\n")
            txtfile.write("-" * len(header) + "\n")
            
            # Write rows
            for row in self.last_results:
                row_str = " | ".join(
                    str(row.get(col, '')).ljust(col_widths[col])
                    for col in columns
                )
                txtfile.write(row_str + "\n")
    
    def emptyline(self):
        """Handle empty line input"""
        pass
    
    def default(self, line):
        """Handle unknown commands"""
        print(f"❌ Unknown command: {line}")
        print("Type 'help' for available commands")

def main():
    """Main entry point"""
    try:
        cli = SQLiteCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
