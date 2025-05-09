
# Crawl4AI MCP Server

A web crawler MCP server using crawl4ai that allows AI models to crawl websites and extract content in markdown format.

## Features

- **Simple URL Crawling**: Crawl a single URL and get content in markdown format
- **Recursive Crawling**: Recursively crawl websites starting from a URL
- **Configurable Depth**: Control how deep the crawler should go
- **Timeout Configuration**: Set custom timeout for long crawling operations

## Installation

### Using uv (Recommended)

The fastest way to install and use the Crawl4AI MCP server is with uv:

```bash
# Install directly from GitHub
uv pip install git+https://github.com/yourusername/crawl4ai-mcp.git

# Or create a virtual environment first
uv venv -p python3.10 .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install git+https://github.com/yourusername/crawl4ai-mcp.git
```

### Using pipx

You can also install it with pipx for an isolated environment:

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

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage with MCP

### Running the Server

Once installed, you can run the MCP server directly:

```bash
# If installed with pipx
pipx run crawl4ai-mcp

# If installed with pip or uv
python -m Crawl_mcp.main
```

The server uses stdio transport (not URL-based) for communication with MCP clients.

### Using the mcp.json Configuration

This repository includes an `mcp.json` file that you can use to configure the MCP server in MCP-compatible clients:

```bash
# Copy it to your home directory or project directory
cp mcp.json ~/.mcp.json
```

The `mcp.json` file contains:
- Server configuration with stdio transport
- Tool definitions with parameters and return types
- Descriptions for tools and parameters

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

Here's an example of how to use the MCP server with Claude after configuring it in your MCP environment:

```
I need to use the Crawl4AI MCP server to crawl a website.

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

Note: The MCP server uses stdio transport for communication, not HTTP/URL-based transport. This means it runs in the terminal and communicates through standard input/output streams.

## Development

### Requirements

- Python 3.10 or higher
- MCP CLI 1.7.1 or higher (`pip install mcp[cli]>=1.7.1`)
- crawl4ai (`pip install crawl4ai`)

### Development Setup

Set up your development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/crawl4ai-mcp.git
cd crawl4ai-mcp

# Create a virtual environment with uv
uv venv -p python3.10 .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install in development mode
uv pip install -e .

# Install development dependencies (if you have any)
uv pip install -e ".[dev]"
```

### Testing

To test the MCP server locally:

```bash
# Run the server in development mode with the MCP Inspector
mcp dev Crawl_mcp/server.py

# Or run the module directly (stdio mode)
python -m Crawl_mcp.main
```

When running in stdio mode, the server expects JSON-RPC messages on stdin and writes responses to stdout. This is how MCP clients communicate with the server.

### Dependency Management

Use uv to manage dependencies:

```bash
# Check for dependency conflicts
uv pip check

# Generate a lock file (if you have a requirements.in file)
uv pip compile requirements.in -o requirements.txt
```

## License

[MIT License](LICENSE)
