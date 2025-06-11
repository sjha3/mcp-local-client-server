#Import tools so they get registered via decorators
import tools.file_tools
import tools.finance_tools
import tools.personal_reviews
from localmcpserver.server import mcp, logger


if __name__ == "__main__":
    logger.info("Starting MCP server using logger...")
    mcp.run()

