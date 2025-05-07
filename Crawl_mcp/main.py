#!/usr/bin/env python3
"""
Command-line entry point for Crawl4AI MCP Server
"""

import sys
import argparse
from Crawl_mcp.server import mcp


def main():
    """Main entry point for the Crawl4AI MCP Server"""
    parser = argparse.ArgumentParser(description="Crawl4AI MCP Server")
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout in seconds for MCP requests (default: 600)",
    )
    
    args = parser.parse_args()
    
    # Set timeout
    mcp.timeout = args.timeout
    
    # Run with stdio transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    sys.exit(main())
