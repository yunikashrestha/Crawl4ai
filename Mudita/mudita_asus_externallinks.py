import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig,CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_all_asus_laptops():
    brow_config = BrowserConfig(headless=False)  # Change to True for headless mode

    config_run = CrawlerRunConfig(
        word_count_threshold=50,
        markdown_generator=DefaultMarkdownGenerator(),
        excluded_tags=["header", "nav", "footer", "aside", "form", "script", "style"],
        only_text=False,
        remove_forms=True,
        parser_type="lxml",
        cache_mode=CacheMode.DISABLED,
        method="GET",
        check_robots_txt=False,
        delay_before_return_html=5.0,
        mean_delay=2.0,
        max_range=6.0,
        semaphore_count=3,

        # JavaScript: keep clicking "Show 20 more products" until it disappears
        js_code="""
        async function clickShowMore() {
            for (let i = 0; i < 10; i++) {  // Try up to 10 times
                let btn = document.querySelector('button.action.primary.mst-scroll__button._next');
                if (!btn) {
                    console.log("No more 'Show more' button found after " + i + " clicks.");
                    break;
                }
                btn.click();
                console.log("Clicked 'Show 20 more products' button #" + (i + 1));
                await new Promise(r => setTimeout(r, 4000));  // wait 4s for new products to load
            }
            window.scrollTo(0, document.body.scrollHeight);
            return true;
        }
        clickShowMore();
        """,

        scan_full_page=True,
        scroll_delay=2,
        max_scroll_steps=5,
        process_iframes=False,
        remove_overlay_elements=True,
        simulate_user=True,

        exclude_social_media_domains=[],
        exclude_external_links=True,
        exclude_social_media_links=True,
        exclude_domains=[],
        css_selector="li.item.product.product-item",  # Product container

        verbose=True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    target_url = "https://mudita.com.np/laptops-nepal/by-brand/asus.html?laptop_series=698,697,699,695,696,727"

    async with AsyncWebCrawler(config=brow_config) as crawler:
        print(f"Starting crawl for: {target_url}")
        results = await crawler.arun(url=target_url, config=config_run)

        if results.success:
            print("Page fetched successfully. Extracting product URLs...")

            product_urls = set()
            for result in results:
                for link in result.links["internal"]:
                    href = link.get("href")
                    if href and "/asus-" in href:  # filter to keep only Asus product pages
                        product_urls.add(href)

            # Save results
            output_file = "links.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                for url in sorted(product_urls):
                    f.write(url + "\n")

            print(f"Saved {len(product_urls)} product URLs to '{output_file}'")
        else:
            print("Crawl failed. Check configuration or JS execution timing.")

async def main():
    await scrape_all_asus_laptops()

if __name__ == "__main__":
    asyncio.run(main())
