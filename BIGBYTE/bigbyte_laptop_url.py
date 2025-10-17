import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_all_urls():
    brows_config = BrowserConfig(headless=False, verbose=True)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(),
        word_count_threshold=20,
        only_text=False,
        css_selector="div.wd-products-element>div>div>div.product-wrapper>div.product-element-bottom",
        excluded_tags=["header", "footer", "nav", "script", "style", "form", "aside"],
        remove_forms=True,
        parser_type="lxml",
        method="GET",
        delay_before_return_html=10.0,
        mean_delay=5.0,
        max_range=8.0,
        semaphore_count=1,
        js_code="""
            window.scroll(0, document.body.scrollHeight);
            return true;
        """,
        scan_full_page=True,
        scroll_delay=5,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        verbose=True,
    )

    all_links = set()

    async with AsyncWebCrawler(config=brows_config) as crawler:
        total_pages = 10

        for page in range(1, total_pages + 1):
            
            if page == 1:
                url = "https://bigbyte.com.np/bigbyte-it-best-laptops-store-in-nepal/"
            else:
                url = f"https://bigbyte.com.np/bigbyte-it-best-laptops-store-in-nepal/page/{page}/"

            print(f"Crawling page {page}: {url}")

            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                internal_links = []
                for link in result.links["internal"]:
                    href = link.get("href")
                    if href and href not in all_links:
                        all_links.add(href)
                        internal_links.append(href)

                print(f"Page {page} scraped successfully — found {len(internal_links)} links")
            else:
                print(f"Failed to crawl page {page}")
                internal_links = []  

  
    with open("try.txt", "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

    print(f"\nTotal unique product URLs collected: {len(all_links)}")


if __name__ == "__main__":
    asyncio.run(scrape_all_urls())
