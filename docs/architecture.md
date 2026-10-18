# System Architecture - DataMind

## Overview
DataMind is an AI-powered data agent designed to allow non-technical users to query enterprise database systems (Snowflake) using plain English. Powered by **Google Gemma**, DataMind converts natural language user prompts into optimized, read-only SQL queries and presents structured analytical outputs back to the user with end-to-end traceability.

---

## High-Level Component Diagram
[ User (Web Browser) ]
│
▼
┌──────────────────────────────────────────────────────────┐
│ Streamlit User Interface (app.py)                     │
│ ├── Input: Plain English Question                         │
│ └── Output: SQL, Raw Data Tables, & Executed Query ID    │
└─────────┬────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ Google Gemma (GenAI SDK)                                 │
│ ├── Prompt Construction (Question + Schema Context)      │
│ └── SQL Generation Logic                                 │
└─────────┬────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────┐
│ Safety & Reliability Layer (Guardrails)                  │
│ ├── Regex & AST Keyword Validator                        │
│ └── Action: Blocks DDL/DML (DROP, DELETE, UPDATE, etc.) │
└─────────┬────────────────────────────────────────────────┘
│ (If Validated Read-Only)
▼
┌──────────────────────────────────────────────────────────┐
│ Snowflake Data Warehouse                                 │
│ ├── Connector: snowflake-connector-python             │
│ ├── Dataset: SNOWFLAKE_SAMPLE_DATA.TPCH_SF1           │
│ └── Output: Result DataFrame + Snowflake Query ID        │
└──────────────────────────────────────────────────────────┘


---

## Step-by-Step Data Flow

1. **User Request**: The user enters a natural language query (e.g., *"Show top 5 customers with highest account balance"*) into the Streamlit frontend.
2. **Context Injection & Prompt Engineering**: The system injects Snowflake schema context (`TPCH_SF1` table definitions, column names, and primary/foreign keys) alongside the user's prompt.
3. **SQL Generation (Google Gemma)**: Google Gemma evaluates the prompt and generates a syntactically correct, dialect-aware Snowflake SQL query enclosed in structured code blocks.
4. **Read-Only Safety Guardrail**: Before any execution occurs, the generated string is evaluated by a regex guardrail parser.
   - **Passed**: If the statement begins strictly with `SELECT` and contains no forbidden mutative keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`), execution proceeds.
   - **Blocked**: If a non-`SELECT` or hazardous operation is detected, execution is halted immediately and an audit warning is flagged on the UI.
5. **Snowflake Execution**: The validated SQL query is submitted to Snowflake via `snowflake-connector-python`.
6. **Results & Traceability**: Snowflake returns the queried records as a Pandas DataFrame along with the unique Snowflake Query ID (`sfqid`). Streamlit renders the generated SQL code, data table, and query execution ID for full claim-to-row auditability.

---

## Security & Reliability Design
- **Zero Credential Leakage**: Database passwords and API keys are strictly managed via local `.env` configuration and excluded from version control using `.gitignore`.
- **Deterministic Read-Only Enforcement**: Ensures zero write or drop privileges can be executed by generated model outputs.
