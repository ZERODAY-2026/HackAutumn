# HackAutumn
# DataMind - Talk to Your Data

## Project Overview
DataMind is an AI-powered open-source data agent that lets users ask questions in natural language and receive grounded answers calculated directly from Snowflake sample datasets using Google Gemma.

## Features
- **Natural Language Querying:** Ask questions in plain English.
- **Deterministic Computation:** Answers are computed in real time using SQL executed against Snowflake.
- **Traceable Evidence:** Displays the exact SQL executed and raw result rows returned by Snowflake.
- **Read-Only Safeguards:** Blocks non-SELECT queries to prevent unauthorized database modifications.

## Architecture & Workflow
1. User enters a question in the Streamlit UI.
2. Google Gemma converts the user's question into a Snowflake SQL query based on database schema.
3. The SQL statement is validated by a read-only safeguard layer.
4. The validated query is executed on Snowflake (`SNOWFLAKE_SAMPLE_DATA`).
5. Results, raw data rows, and an explanation are displayed to the user.

## Setup and Installation

### Prerequisites
- Python 3.9+
- A Snowflake account with access to `SNOWFLAKE_SAMPLE_DATA`
- Google Gemma API key (Google AI Studio / Hugging Face)

### Local Deployment
1. Clone the repository:
   ```bash
   git clone [https://github.com/ubrahmmani/datamind.git](https://github.com/ubrahmmani/datamind.git)
   cd datamind
