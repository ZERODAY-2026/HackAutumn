# Test suite for SQL generation safety guardrails

def is_safe_query(sql: str) -> bool:
    """Validates that a generated query is strictly a SELECT statement."""
    clean_sql = sql.strip().upper()
    if not clean_sql.startswith("SELECT"):
        return False
    forbidden_words = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE"]
    for word in forbidden_words:
        if word in clean_sql:
            return False
    return True

def run_tests():
    test_cases = [
        ("SELECT * FROM CUSTOMER LIMIT 10;", True),
        ("SELECT C_NAME, C_ACCTBAL FROM CUSTOMER ORDER BY C_ACCTBAL DESC LIMIT 5;", True),
        ("DROP TABLE CUSTOMER;", False),
        ("UPDATE CUSTOMER SET C_ACCTBAL = 0;", False),
        ("DELETE FROM ORDERS WHERE O_ORDERDATE < '1995-01-01';", False)
    ]

    print("--- Running Read-Only Safety Guardrail Tests ---")
    all_passed = True
    for query, expected in test_cases:
        result = is_safe_query(query)
        status = "PASSED" if result == expected else "FAILED"
        if result != expected:
            all_passed = False
        print(f"[{status}] Query: '{query}' | Expected Safe: {expected} | Got: {result}")
    
    if all_passed:
        print("\nAll guardrail test cases passed successfully!")

if __name__ == "__main__":
    run_tests()
