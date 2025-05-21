from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Crawl4AI")

@mcp.tool()
async def crawl_recursive(
    url: str,
    max_depth: int = 2,
    max_pages: int = 500
) -> dict:
    """
    Recursively crawl a website starting from a URL.

    Args:
        url: The URL to start crawling from.
        max_depth: Maximum depth for recursive crawling (default: 2).
        max_pages: Maximum number of pages to crawl (default: 500).

    Returns:
        Dictionary with crawled data.
    """
    import re
    import io
    import hashlib
    from contextlib import redirect_stdout
    from urllib.parse import urljoin, urlparse

    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

    def extract_urls_from_markdown(markdown_text, base_url):
        if not markdown_text or isinstance(markdown_text, dict):
            return []
        # Ensure base_url ends with a slash for proper matching
        if not base_url.endswith('/'):
            base_url = base_url + '/'
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        links = re.findall(link_pattern, markdown_text)
        extracted_urls = []
        for _, link_url in links:
            absolute_url = urljoin(base_url, link_url)
            if absolute_url.startswith(base_url) and absolute_url != base_url:
                extracted_urls.append(absolute_url)
        return extracted_urls
    
    def remove_links_from_markdown(markdown_text):
        """
        Remove markdown links from text while preserving the link text.
        For example, [Link Text](https://example.com) becomes Link Text.
        
        Args:
            markdown_text: The markdown text to process.
            
        Returns:
            Markdown text with links removed but link text preserved.
        """
        if not markdown_text or isinstance(markdown_text, dict):
            return markdown_text
        
        # Replace markdown links with just the link text
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        return re.sub(link_pattern, r'\1', markdown_text)

    def get_content_hash(content: str) -> str:
        if not content:
            return "empty"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if not base_url.endswith('/'):
            base_url += '/'

        crawled_urls = set()
        content_hashes = set()
        results = []
        page_count = 0
        main_content = ""

        async def recursive_crawl(current_url, crawler, current_depth=0):
            nonlocal page_count, main_content

            if current_depth > max_depth or current_url in crawled_urls or page_count >= max_pages:
                return

            crawled_urls.add(current_url)
            page_count += 1

            try:
                config = CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    verbose=False,
                )
                f_inner = io.StringIO()
                with redirect_stdout(f_inner):
                    result = await crawler.arun(url=current_url, config=config)
                markdown_content = ""
                if hasattr(result, "markdown") and hasattr(result.markdown, "raw_markdown"):
                    markdown_content = result.markdown.raw_markdown or ""
                # Duplicate content check
                content_hash = get_content_hash(markdown_content)
                if content_hash in content_hashes and content_hash != "empty":
                    return  # Skip duplicate content
                content_hashes.add(content_hash)
                if current_url == url and not main_content:
                    main_content = remove_links_from_markdown(markdown_content)
                
                # Remove links from markdown content before adding to results
                clean_markdown = remove_links_from_markdown(markdown_content)
                results.append({
                    "url": current_url,
                    "depth": current_depth,
                    "title": getattr(result, "title", "") or result.metadata.get("title", ""),
                    "markdown": clean_markdown
                })

                if current_depth < max_depth and page_count < max_pages:
                    extracted_urls = extract_urls_from_markdown(markdown_content, base_url)
                    for next_url in extracted_urls:
                        if next_url not in crawled_urls and page_count < max_pages:
                            await recursive_crawl(next_url, crawler, current_depth + 1)
            except Exception as e:
                results.append({
                    "url": current_url,
                    "depth": current_depth,
                    "error": str(e)
                })

        f = io.StringIO()
        with redirect_stdout(f):
            async with AsyncWebCrawler() as crawler:
                await recursive_crawl(url, crawler)

        return {
            "status": "success",
            "crawled_urls_count": len(crawled_urls),
            "main_content": main_content,
            "data": results
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }
