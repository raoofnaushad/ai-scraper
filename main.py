
import os

from src import scraper as SC
from src import utils as U
from src import normalization as N
from src import config as C



def scrape(url):
    
    ## Step 1: Getting all the links from the given url which has the same domain
    same_domain_urls = U.find_links_same_domain(url)
    # Order URLs by length
    ordered_urls = U.sort_urls_by_length(same_domain_urls)

    ## Step 2: Retrieving content (as formatted text) from all these websites as a list.
    contents_in_md = SC.extract_content_to_markdown(ordered_urls)

    # Step 3: Use the extracted content from all the sites to merge to the final content which will be used for scraping.
    merged_content = N.merge_contents(contents_in_md)
    
    # Check if the debug folder exists, if not create it
    debug_folder_path = './debug'
    if not os.path.exists(debug_folder_path):
        os.makedirs(debug_folder_path)

    # Writing merged contents to a Markdown file
    file_path = os.path.join(debug_folder_path, 'scraped_md.md')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(merged_content)
    
    return None


def scrape_and_extract(url, company_name):
    # Placeholder for the scraping logic
    contents = scrape(url)
    token_count = U.count_tokens(contents)
    print(f"Token Count: {token_count}")
    segmented_content = U.split_content_by_token_limit(contents)
    print(f"Segmented Content Size: {len(segmented_content)}")


if __name__ == "__main__":
    url = "https://www.farpointhq.com/"
    company_name = "Farpoint"
    # url = "https://www.evbex.com/"

    scrape_and_extract(url, company_name)

