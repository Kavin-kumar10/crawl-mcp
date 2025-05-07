# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Crawl4AI")


# Add a simple crawling tool
@mcp.tool()
async def crawl_simple(url: str) -> str:
    """
    Crawl a single URL and return the content in markdown format
    
    Args:
        url: The URL to crawl
        
    Returns:
        Markdown content of the crawled page
    """
    from crawl4ai import AsyncWebCrawler
    
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except Exception as e:
        return f"Error crawling {url}: {str(e)}"


# Add a recursive crawling tool
@mcp.tool()
async def crawl_recursive(url: str, max_depth: int = 2) -> dict:
    """
    Recursively crawl a website starting from a URL
    
    Args:
        url: The URL to start crawling from
        max_depth: Maximum depth for recursive crawling (default: 2)
        
    Returns:
        Dictionary with crawled data
    """
    import os
    import json
    from urllib.parse import urljoin
    import re
    from crawl4ai import AsyncWebCrawler
    
    # Helper function to extract URLs from markdown content
    def extract_urls_from_markdown(markdown_text, base_url):
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        links = re.findall(link_pattern, markdown_text)
        
        extracted_urls = []
        
        # Ensure base_url ends with a slash for proper matching
        if not base_url.endswith('/'):
            base_url = base_url + '/'
        
        for _, url in links:
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, url)
            
            # Check if the URL starts with the exact base URL
            if absolute_url.startswith(base_url) and absolute_url != base_url:
                extracted_urls.append(absolute_url)
        
        return extracted_urls
    
    # Recursive crawling function
    async def recursive_crawl(current_url, crawler, crawled_urls, base_url, current_depth=0):
        if current_depth > max_depth or current_url in crawled_urls:
            return []
        
        crawled_urls.add(current_url)
        results = []
        
        try:
            result = await crawler.arun(url=current_url)
            
            # Create a structured entry for this URL
            page_data = {
                "url": current_url,
                "title": result.title if hasattr(result, 'title') else "",
                "content": result.markdown,
                "depth": current_depth
            }
            
            results.append(page_data)
            
            # Extract URLs from the content for further crawling
            if current_depth < max_depth:
                extracted_urls = extract_urls_from_markdown(result.markdown, base_url)
                
                for next_url in extracted_urls:
                    if next_url not in crawled_urls:
                        # Recursively crawl the extracted URLs
                        sub_results = await recursive_crawl(
                            next_url, crawler, crawled_urls, base_url, current_depth + 1
                        )
                        results.extend(sub_results)
            
        except Exception as e:
            results.append({
                "url": current_url,
                "error": str(e),
                "depth": current_depth
            })
        
        return results
    
    # Main crawling logic
    try:
        base_url = url
        
        # Remove trailing slash for consistency
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        
        crawled_urls = set()
        crawled_data = []
        
        async with AsyncWebCrawler() as crawler:
            results = await recursive_crawl(url, crawler, crawled_urls, base_url)
            crawled_data.extend(results)
        
        return {
            "status": "success",
            "crawled_urls_count": len(crawled_urls),
            "data": crawled_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")
