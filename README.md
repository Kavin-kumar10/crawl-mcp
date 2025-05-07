# Crawl4AI MCP Server

A web crawler MCP server using crawl4ai that allows AI models to crawl websites and extract content in markdown format.

## Features

- **Simple URL Crawling**: Crawl a single URL and get content in markdown format
- **Recursive Crawling**: Recursively crawl websites starting from a URL
- **Configurable Depth**: Control how deep the crawler should go
- **Timeout Configuration**: Set custom timeout for long crawling operations

## Installation

### Using pipx (Recommended)

The easiest way to install and use the Crawl4AI MCP server is with pipx:

```bash
pipx install git+https://github.com/yourusername/crawl4ai-mcp.git
```

This will install the package in an isolated environment and make the `crawl4ai-mcp` command available globally.

### Using pip

You can also install it with pip:

```bash
pip install git+https://github.com/yourusername/crawl4ai-mcp.git
```

### From Source

To install from source:

```bash
git clone https://github.com/yourusername/crawl4ai-mcp.git
cd crawl4ai-mcp
pip install -e .
```

## Usage with MCP

### Running the Server

Once installed, you can use the MCP server with any MCP-compatible client:

```bash
# Using pipx installation
mcp connect crawl4ai-mcp

# Or directly with the MCP CLI
mcp connect "pipx run crawl4ai-mcp"
```

### Available Tools

The MCP server provides the following tools:

#### 1. crawl_simple

Crawl a single URL and return the content in markdown format.

**Parameters:**
- `url` (string): The URL to crawl

**Example:**
```json
{
  "url": "https://example.com"
}
```

#### 2. crawl_recursive

Recursively crawl a website starting from a URL.

**Parameters:**
- `url` (string): The URL to start crawling from
- `max_depth` (integer, optional): Maximum depth for recursive crawling (default: 2)

**Example:**
```json
{
  "url": "https://example.com",
  "max_depth": 3
}
```

### Example Usage with Claude

Here's an example of how to use the MCP server with Claude:

```
I need to connect to the Crawl4AI MCP server to crawl a website.

First, let me crawl a single page:
<use_mcp_tool>
<server_name>crawl4ai-mcp</server_name>
<tool_name>crawl_simple</tool_name>
<arguments>
{
  "url": "https://example.com"
}
</arguments>
</use_mcp_tool>

Now, let me recursively crawl the website:
<use_mcp_tool>
<server_name>crawl4ai-mcp</server_name>
<tool_name>crawl_recursive</tool_name>
<arguments>
{
  "url": "https://example.com",
  "max_depth": 2
}
</arguments>
</use_mcp_tool>
```

## Development

### Requirements

- Python 3.8 or higher
- MCP CLI (`pip install mcp[cli]`)
- crawl4ai (`pip install crawl4ai`)

### Testing

To test the MCP server locally:

```bash
# Run the server in development mode
mcp dev Crawl_mcp/server.py
```

## License

[MIT License](LICENSE)
