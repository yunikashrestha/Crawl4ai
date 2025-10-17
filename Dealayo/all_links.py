import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_links():
    brows_config = BrowserConfig(headless=True, verbose=True)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=20,
        markdown_generator=DefaultMarkdownGenerator(),
        excluded_tags=["header", "nav", "footer", "style", "script", "aside"],
        only_text=False,
        remove_forms=True,
        parser_type="lxml",
        method="GET",
        check_robots_txt=False,
        delay_before_return_html=20.0,
        mean_delay=3.0,
        max_range=6.0,
        semaphore_count=5,
        js_code="""
            window.scrollTo(0, document.body.scrollHeight);
            return true;
        """,
        scan_full_page=True,
        scroll_delay=2.5,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        simulate_user=True,
        css_selector="div.product-item-info",
        target_elements=['div'],
        verbose=True,
    )

    all_links = set()

    async with AsyncWebCrawler(config=brows_config) as crawler:
        for page_num in range(1, 6):
            url = f"https://dealayo.com/mobile.html?p={page_num}"
            print(f"\n Crawling page {page_num}: {url}")

            results = await crawler.arun(url=url, config=run_config)

            if results.success:
                internal_links = []
                for link in results.links["internal"]:
                    product_url = link.get("href")  # FIXED here
                    if product_url and product_url not in all_links:
                        all_links.add(product_url)
                        internal_links.append(product_url)

                print(f"Found {len(internal_links)} product URLs on page {page_num}")

                # Append to file instead of overwriting
                with open("dealayo_mobile_links.txt", "a", encoding="utf-8") as f:
                    for link in internal_links:
                        f.write(link + "\n")

            else:
                print(f"Failed to crawl page {page_num}")

    print(f"\nTotal unique product URLs collected: {len(all_links)}")

if __name__ == "__main__":
    asyncio.run(scrape_links())
