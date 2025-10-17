import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_multiple_urls():
    brows_config = BrowserConfig(headless=False, verbose=True)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(),
        word_count_threshold=20,
        only_text=False,
        css_selector="span.base, span.price, div#description.data.item.content ul, div.additional-attributes-wrapper.table-wrapper",
        excluded_tags=["header","nav","footer","form","style","script"],
        scan_full_page=True,
        js_code="""
            window.scrollTo(0,document.body.scrollHeight);
            const moreInfoButton = document.querySelector("#tab-label-additional-title");
            if (moreInfoButton) {
                moreInfoButton.click();
            }
            return true;

            
        """,
        scroll_delay=1.5,
        delay_before_return_html=10.0,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    # List of URLs obtained previously
    with open("dealayo_mobile_links.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with AsyncWebCrawler(config=brows_config) as crawler:
        for idx, url in enumerate(urls, start=1):
            print(f"\nScraping URL {idx}/{len(urls)}: {url}")
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                print("*******Crawled Successfully*******")
                print(result.markdown)

                # Save each product description in a single Markdown file (appending)
                with open("all_laptop_feature.md", "a", encoding="utf-8") as f:
                    f.write(f"# Product {idx}\n")
                    f.write(f"URL: {url}\n\n")
                    f.write(result.markdown + "\n")
                    f.write("="*80 + "\n")  # separator
                print(f"******Saved product {idx} description******")
            else:
                print(f"*******Failed to fetch URL {url}*******")

async def main():
    await scrape_multiple_urls()

if __name__ == "__main__":
    asyncio.run(main())