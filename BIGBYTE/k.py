import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode,BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def crawl_for_information(internal_links):

    """
    js_selector = div#tab-id>div:nth-child(1)>button
    """
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(verbose = True, headless = True)
    run_conf_one = CrawlerRunConfig(
    session_id=session_id,   
    css_selector="div.elementor-widget-container>h1, p.price, span.meta-label, span.sku, div.woocommerce-product-details__short-description>p, div.woocommerce-product-details__short-description>ul>li:nth-of-type(1), section[data-id='7c5ae2c']>div>div>div>div>div>table ",
    word_count_threshold=10,      
    excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
    markdown_generator=DefaultMarkdownGenerator(),
    cache_mode=CacheMode.DISABLED,
    delay_before_return_html=20.0,
    js_code="""
            window.scrollTo(0,document.body.scrollHeight);
            const moreInfoButton = document.querySelector("span.wd-btn-text");
            if (moreInfoButton) {
                moreInfoButton.click();
            }
            return true;

            
        """,
        scan_full_page=True,
        remove_overlay_elements=True,
        simulate_user=True,
        verbose=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        
    )
    

    async with AsyncWebCrawler(config = browser_config) as crawler:
            for internal_link in internal_links:
                results_one = await crawler.arun(url =internal_link , config = run_conf_one)
                if results_one.success:
                    print(results_one.markdown)

                    with open("laptop-info.md","a",encoding="utf-8") as f:
                        f.write(f'{results_one.markdown}\n URL = {internal_link}\n\n\n====================\n\n\n')