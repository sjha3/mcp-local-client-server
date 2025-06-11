# MCP Client-Server Project

This project provides a local implementation of an MCP (Model Context Protocol) server and client, enabling AI agents to interact with local tools and data sources.

## Features

### 1. MCP Server
The MCP server exposes tools to perform the following operations:

- **Operations in local files**: Read and process data from local CSV and Parquet files.
- **Get financial data**: Retrieve financial data using the Yahoo Finance API.
- **Manage lifecycle of an object in Kusto database**: Create, update, and manage objects in an Azure Data Explorer (Kusto) database.

### 2. MCP Client
The MCP client provides the following capabilities:

- **Connects to the MCP server** created above.
- **Creates AI agents using Autogen**: Utilizes the Autogen framework to instantiate multiple AI agents.
- **Assigns tools from the MCP server to these agents**: Each agent is equipped with the appropriate tools for its tasks.

## How to Run

1. **Install Python dependencies** using pip:
   ```
   pip install -r requirements.txt
   ```
2. **Create .env file and add these environment variables**:
   ```
   azure_endpoint
   azure_deployment
   api_version
   api_key
   azure_model_name
   ```
2. **Run the MCP server**:
   ```
   python server-main.py
   ```
3. **Run the MCP client**:
   ```
   python client-main.py
   ```

This will bring up a prompt where you can chat with the AI agents.

Based on your question, the appropriate agent will be invoked and the requested operation will be performed automatically.
