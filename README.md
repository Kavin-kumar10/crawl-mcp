# Crawl4AI MCP Server

This project integrates the Crawl4AI web crawler with the Model Context Protocol (MCP) server, allowing AI models to crawl websites and extract structured content.

## Features

- **URL Crawling**: Recursively crawl websites starting from a URL
- **Sitemap Crawling**: Extract and crawl all URLs from a sitemap
- **Content Extraction**: Parse web content into structured JSON
- **Content Summarization**: Summarize crawled content using AWS Bedrock Claude

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd my-first-mcp-server
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file with your AWS credentials and Bedrock configuration:
   ```
   # AWS Credentials
   AWS_ACCESS_KEY_ID=your_aws_access_key_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
   AWS_REGION=us-east-1

   # Bedrock Model Configuration
   BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
   MAX_TOKENS=4000
   TEMPERATURE=0.7
   ```

2. Replace the placeholder values with your actual AWS credentials and preferred configuration.

## Running the Server

Start the MCP server:

```bash
python server.py
```

The server will be available at `http://localhost:8000`.

## Using the Crawler Tools

The MCP server provides the following tools:

### 1. crawl_url

Crawl a URL and its linked pages recursively.

**Parameters:**
- `url` (string): The URL to crawl
- `max_depth` (integer, optional): Maximum depth for recursive crawling (default: 3)

**Example:**
```json
{
  "url": "https://example.com",
  "max_depth": 2
}
```

### 2. crawl_sitemap

Crawl all URLs from a sitemap.

**Parameters:**
- `sitemap_url` (string): URL of the sitemap XML file

**Example:**
```json
{
  "sitemap_url": "https://example.com/sitemap.xml"
}
```

### 3. summarize_crawled_data

Summarize crawled data using AWS Bedrock Claude.

**Parameters:**
- `crawled_data` (array): List of crawled data entries
- `use_langchain` (boolean, optional): Whether to use LangChain (default: true)

**Example:**
```json
{
  "crawled_data": [...],
  "use_langchain": true
}
```

## Example Usage

Here's an example of how to use the MCP server with an AI model:

1. The AI model connects to the MCP server
2. The model uses the `crawl_url` tool to crawl a website
3. The model processes the crawled data
4. The model uses the `summarize_crawled_data` tool to generate a summary

## Output

The crawler tools generate output in the following format:

```json
{
  "status": "success",
  "crawled_urls": 10,
  "unique_entries": 25,
  "output_dir": "output_20240705_115200",
  "output_file": "output_20240705_115200/output.json",
  "data": [...]
}
```

The summarization tool generates output in the following format:

```json
{
  "status": "success",
  "output_dir": "output_20240705_115200",
  "output_file": "output_20240705_115200/summarized.json",
  "context": {
    "contextData": "...",
    "metadata": {
      "filepath": "input.json",
      "section": [...]
    }
  },
  "data": [...]
}
```

## License

[MIT License](LICENSE)
