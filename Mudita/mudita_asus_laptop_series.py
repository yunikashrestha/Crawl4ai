import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_product_urls():
    brow_config = BrowserConfig(headless=False)

    config_run = CrawlerRunConfig(
        word_count_threshold=50,
        markdown_generator=DefaultMarkdownGenerator(),
        excluded_tags=["header", "nav", "footer", "aside", "form", "script", "style"],
        only_text=False,
        remove_forms=True,
        parser_type="lxml",

        disable_cache=False,
        no_cache_read=False,
        no_cache_write=False,
        method="GET",
        check_robots_txt=False,
        delay_before_return_html=10.0,
        mean_delay=2.0,
        max_range=6.0,
        semaphore_count=5,
        js_code="""
        async function clickShowMore() {
            for (let i = 0; i < 50; i++) {  // Try up to 10 times
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
        scroll_delay=1.5,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        simulate_user=True,

        exclude_social_media_domains=[],
        exclude_external_links=True,
        exclude_social_media_links=True,
        exclude_domains=[],
        css_selector="li.item.product.product-item",
        target_elements=['li'], 
        verbose=True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    async with AsyncWebCrawler(config=brow_config) as crawler:
        all_links = set()  
        product_array=[698,697,699,696,695,727]# to avoid duplicates

        # LOOP through multiple pages
        for page_num in range(0, 6):  
            url = f"https://mudita.com.np/laptops-nepal/by-brand/asus.html?laptop_series={product_array[page_num]}"
            print(f"\n[CRAWLING PAGE {page_num}] {url}")

            results = await crawler.arun(url=url, config=config_run)

            if results.success:
                internal_links = []
                for result in results:
                    for link in result.links["internal"]:
                        product_url = link.get("href")
                        if product_url and product_url not in all_links:
                            all_links.add(product_url)
                            internal_links.append(product_url)

                print(f"Found {len(internal_links)} product URLs on page {page_num}")
                
                # Save
                with open(f"mudita_asus_laptop{product_array[page_num]}.txt", "a", encoding="utf-8") as f:
                    for link in internal_links:
                        f.write(link + "\n")
            else:
                print(f"Failed to crawl page {page_num}")

        print(f"\nTotal unique product URLs collected: {len(all_links)}")

async def main():
    await scrape_product_urls()

if __name__ == "__main__":
    asyncio.run(main())
