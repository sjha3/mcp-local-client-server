from utils.file_reader import read_csv_summary, read_parquet_summary
from localmcpserver.server import mcp, logger


@mcp.tool()
def summarize_csv(filename: str) -> str:
    """
    Summarize the contents of a CSV file.
    
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
    
    Returns:
        A string summarizing the file's contents.
    """
    return read_csv_summary(filename)

@mcp.tool()
def summarize_parquet(filename: str) -> str:
    """
    Summarize the contents of a Parquet file.
    
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    
    Returns:
        A string summarizing the file's contents.
    """
    return read_parquet_summary(filename)