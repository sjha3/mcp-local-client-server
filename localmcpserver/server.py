from mcp.server.fastmcp import FastMCP
import yfinance as yf
import logging

#print("Starting MCP server...")

# This is the shared MCP server instance
mcp = FastMCP("local-mcp-server")

# Setup logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("mcp-server")
logger.info("Initializing MCP server...")


