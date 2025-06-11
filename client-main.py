from localmcpclient.client import MCPClient
import asyncio,sys
#from Agents import review_agent, finance_agent

async def main():
    client = MCPClient()
    
    try: 
        print("Connecting to MCP server...")
        await client.connect_to_server("server-main.py")  # Path to your server script
        print("Start chat...")
        await client.start_chat()
    except Exception as e:
        print(f"Error connecting to server: {e}")
    #finally:
    #    await client.close()

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        print("Asyncio task was cancelled during shutdown.")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime error during asyncio shutdown: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unhandled exception during shutdown: {e}")
        sys.exit(1)