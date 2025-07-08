# SQLite CLI Tool

A comprehensive command-line interface for SQLite database interaction, designed for developers and data analysts who need robust, user-friendly database querying capabilities.

## Features

### Core Functionality
- **Secure Database Connections**: Connect to SQLite databases with error handling
- **Interactive SQL Execution**: Execute SELECT, INSERT, UPDATE, DELETE queries
- **Multiple Output Formats**: Save results as CSV, JSON, or plain text
- **Query History**: Track and review previously executed queries
- **Result Pagination**: Handle large result sets with configurable page sizes
- **Table Management**: List tables and describe table structures

### User Experience
- **Intuitive Commands**: Simple, memorable command syntax
- **Rich Feedback**: Clear success/error messages with emojis
- **Professional Interface**: Clean, organized output formatting
- **Error Handling**: Graceful handling of connection and query errors

## Installation

1. Ensure you have Python 3.6+ installed
2. No additional dependencies required (uses built-in libraries)
3. Download the CLI tool files

## Quick Start

### 1. Create Sample Database (Optional)
\`\`\`bash
python demo_setup.py
\`\`\`

### 2. Launch the CLI
\`\`\`bash
python run_cli.py
\`\`\`

### 3. Connect to Database
\`\`\`
sqlcli> connect sample_data.sqlite
\`\`\`

### 4. Execute Queries
\`\`\`
sqlcli> query SELECT * FROM users WHERE age > 25
sqlcli> query INSERT INTO users (username, email, age) VALUES ('newuser', 'new@example.com', 30)
\`\`\`

## Available Commands

### Database Operations
- `connect <database_path>` - Connect to SQLite database
- `query <SQL_STATEMENT>` - Execute SQL query
- `tables` - Show all tables in database
- `describe <table_name>` - Show table structure

### Result Management
- `save <filename> [format]` - Save last results (csv/json/txt)
- `pagesize <number>` - Set result pagination size
- `history [limit]` - Show query history

### Utility Commands
- `status` - Show connection status and statistics
- `clear` - Clear screen
- `help` - Show available commands
- `exit` / `quit` - Exit the CLI

## Usage Examples

### Basic Queries
\`\`\`sql
-- Select data with filtering
sqlcli> query SELECT username, email, age FROM users WHERE city = 'New York'

-- Join tables
sqlcli> query SELECT u.username, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id

-- Update records
sqlcli> query UPDATE users SET age = 29 WHERE username = 'john_doe'

-- Insert new data
sqlcli> query INSERT INTO products (name, category, price) VALUES ('New Product', 'Electronics', 99.99)
\`\`\`

### Save Results
\`\`\`bash
# Save as CSV (default)
sqlcli> save user_report.csv

# Save as JSON
sqlcli> save data_export.json json

# Save as plain text
sqlcli> save results.txt txt
\`\`\`

### Database Exploration
\`\`\`bash
# List all tables
sqlcli> tables

# Examine table structure
sqlcli> describe users

# Check connection status
sqlcli> status
\`\`\`

## Output Formats

### CSV Format
- Standard comma-separated values
- Headers included
- UTF-8 encoding

### JSON Format
- Pretty-printed JSON array
- Each row as an object
- Proper data type handling

### Text Format
- Formatted table layout
- Column alignment
- Human-readable structure

## Error Handling

The CLI provides comprehensive error handling for:
- **Connection Errors**: Invalid database paths, permissions
- **SQL Errors**: Syntax errors, constraint violations
- **File Errors**: Save operation failures
- **Input Errors**: Invalid commands, missing parameters

## Query History

- Automatic tracking of all executed queries
- Timestamp and execution time recording
- Row count/affected rows tracking
- Configurable history display limits

## Performance Features

- **Result Pagination**: Handle large datasets efficiently
- **Optimized Display**: Smart column width calculation
- **Memory Management**: Efficient result storage
- **Fast Execution**: Direct SQLite integration

## Security Considerations

- **Local Database Access**: Only works with local SQLite files
- **No Network Exposure**: CLI runs locally only
- **Safe SQL Execution**: Uses parameterized queries where applicable
- **Error Information**: Detailed but safe error messages

## Troubleshooting

### Common Issues

1. **Database Not Found**
   \`\`\`
   ❌ Database connection error: unable to open database file
   \`\`\`
   - Check file path spelling
   - Ensure directory exists
   - Verify file permissions

2. **SQL Syntax Error**
   \`\`\`
   ❌ SQL Error: near "SELCT": syntax error
   \`\`\`
   - Review SQL syntax
   - Check table/column names
   - Use `describe` command to verify structure

3. **Permission Denied**
   \`\`\`
   ❌ Error saving file: [Errno 13] Permission denied
   \`\`\`
   - Check write permissions
   - Ensure directory exists
   - Try different output location

## Advanced Usage

### Batch Operations
\`\`\`sql
-- Create and populate table in sequence
sqlcli> query CREATE TABLE temp_data (id INTEGER, value TEXT)
sqlcli> query INSERT INTO temp_data VALUES (1, 'test'), (2, 'data')
sqlcli> query SELECT * FROM temp_data
\`\`\`

### Complex Queries
\`\`\`sql
-- Analytical queries
sqlcli> query SELECT category, AVG(price) as avg_price, COUNT(*) as product_count FROM products GROUP BY category ORDER BY avg_price DESC

-- Subqueries
sqlcli> query SELECT * FROM users WHERE id IN (SELECT DISTINCT user_id FROM orders WHERE order_date > '2024-01-01')
\`\`\`

## Contributing

This CLI tool is designed to be extensible. Key areas for enhancement:
- Additional output formats
- Query result caching
- Batch query execution
- Configuration file support
- Plugin system for custom commands

## License

Open source - feel free to modify and distribute according to your needs.
