BASIC_GROUND_TRUTH_DATASET = [
  {
    "Query": "Show the total number of employees.",
    "Ground Truth": "SELECT COUNT(*) AS total_employees FROM employees;"
  },
  {
    "Query": "Find the highest salary in the Finance department.",
    "Ground Truth": "SELECT MAX(salary) FROM employees WHERE department = 'Finance';"
  },
  {
    "Query": "Get the average age of all managers.",
    "Ground Truth": "SELECT AVG(age) FROM employees WHERE position = 'Manager';"
  },
  {
    "Query": "List the names and emails of staff in the IT department.",
    "Ground Truth": "SELECT name, email FROM employees WHERE department = 'IT';"
  },
  {
    "Query": "What are the titles of the top 5 selling books?",
    "Ground Truth": "SELECT title FROM books ORDER BY sales DESC LIMIT 5;"
  },
  {
    "Query": "Which product has the least quantity in stock?",
    "Ground Truth": "SELECT product_name FROM products ORDER BY quantity_in_stock ASC LIMIT 1;"
  },
  {
    "Query": "Display the second highest salary in the organization.",
    "Ground Truth": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);"
  },
  {
    "Query": "List employees who joined after 2015 and work in the Sales department.",
    "Ground Truth": "SELECT * FROM employees WHERE year(joined_date) > 2015 AND department = 'Sales';"
  },
  {
    "Query": "Find the average order value for each customer.",
    "Ground Truth": "SELECT customer_id, AVG(order_value) FROM orders GROUP BY customer_id;"
  },
  {
    "Query": "Show departments that have more than 10 employees.",
    "Ground Truth": "SELECT department FROM employees GROUP BY department HAVING COUNT(*) > 10;"
  },
  {
    "Query": "List all products that have never been ordered.",
    "Ground Truth": "SELECT * FROM products WHERE product_id NOT IN (SELECT product_id FROM orders);"
  },
  {
    "Query": "Which customers have spent more than $1000 in total?",
    "Ground Truth": "SELECT customer_id FROM orders GROUP BY customer_id HAVING SUM(order_value) > 1000;"
  },
  {
    "Query": "Show the total number of orders placed each day last week.",
    "Ground Truth": "SELECT order_date, COUNT(*) FROM orders WHERE order_date > CURRENT_DATE - INTERVAL '7 days' GROUP BY order_date;"
  },
  {
    "Query": "List the names of employees who do not manage anyone.",
    "Ground Truth": "SELECT name FROM employees WHERE name NOT IN (SELECT manager_name FROM employees);"
  },
  {
    "Query": "Display the department that has the highest average employee salary.",
    "Ground Truth": "SELECT department FROM employees GROUP BY department ORDER BY AVG(salary) DESC LIMIT 1;"
  }
]

ZERO_SHOT_PROMPT_TEMPLATE = """
Generate a valid SQL query for the following natural language instruction:

${query}

Only generate SQL code as a plain text string with no formatting or markdown.
"""

FEW_SHOT_PROMPT_TEMPLATE = """"
You will be provided a prompt which you are then expected to generated a valid
SQL query for.

When asked for a count, use a descriptive alias.

Only generate SQL code as a plain text string on a single line with no formatting or markdown.

The SQL query should be valid for the following tables and their schemas:
- table: employees
  - name: VARCHAR
  - email: VARCHAR
  - position: VARCHAR
  - department: VARCHAR
  - salary: FLOAT
  - manager_name VARCHAR
- table: books
  - sales: FLOAT
- table: products
  - quantity_in_stock: INT
- table: orders
  - customer_id: INT
  - order_value: FLOAT
  - order_date: DATETIME

Here is the prompt:
${query}
"""