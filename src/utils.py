from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import tiktoken


from src import config as C

def get_domain(url):
    """
    Extracts the domain from a given URL.
    """
    parsed_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
    return domain

def find_links_same_domain(url):
    """
    Fetches a URL, parses its HTML to find all <a> tags, and filters links that belong to the same domain.
    """
    domain = get_domain(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    same_domain_links = []
    for link in links:
        href = link['href']
        # Check if the link is absolute and belongs to the same domain or is relative
        if href.startswith(domain) or href.startswith('/'):
            # Normalize relative links to absolute
            absolute_link = href if href.startswith('http') else domain + href
            same_domain_links.append(absolute_link)
    
    # Remove duplicates by converting the list to a set, then back to a list
    return list(set(same_domain_links))



def count_tokens(content):
    encoding = tiktoken.encoding_for_model(C.OPENAI_MODEL)
    token_count = len(encoding.encode(content))
    return token_count



def sort_urls_by_length(urls):
    """Sort URLs by their length, from shortest to longest."""
    return sorted(urls, key=len)

def split_content_by_token_limit(content, limit=C.TOKEN_LIMIT):
    """
    Split content into segments, each having up to `limit` tokens, 
    while preserving the original structure (e.g., new lines, paragraphs).
    """
    # Split the content by lines to preserve structure
    lines = content.splitlines()
    segments = []
    current_segment = []
    current_token_count = 0
    
    for line in lines:
        # Count tokens in the current line
        line_tokens = line.split()
        line_token_count = len(line_tokens)
        
        # Check if adding this line would exceed the limit
        if current_token_count + line_token_count > limit:
            # If so, start a new segment
            segments.append("\n".join(current_segment))
            current_segment = [line]  # Start new segment with current line
            current_token_count = line_token_count
        else:
            # Otherwise, add the line to the current segment
            current_segment.append(line)
            current_token_count += line_token_count
            
    # Don't forget to add the last segment
    if current_segment:
        segments.append("\n".join(current_segment))
    
    return segments




def read_debug_file(filepath):
    """Read and return the content of a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file {filepath} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None