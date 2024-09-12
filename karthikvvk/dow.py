import os
import requests

# Your Google Custom Search API key
api_key = 'AIzaSyBsutZgpB-cgJltJ2W1qfHOnOMjTcBZArc'

# Your Custom Search Engine (CSE) ID
cse_id = '55aafcdef841a4a20'

def fetch_image_urls(query, num_images):
    """
    Fetches image URLs using the Google Custom Search API.
    :param query: Search query for fetching images.
    :param num_images: Number of image URLs to fetch.
    :return: A list of image URLs.
    """
    start_index = 0
    search_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&searchType=image&num={num_images}&start={start_index}"
    image_urls = []

    while len(image_urls) < num_images:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        search_results = response.json()

        if "items" not in search_results:
            break

        items = search_results["items"]
        for item in items:
            if len(image_urls) >= num_images:
                break
            image_urls.append(item["link"])

        # Pagination: Set next page
        start_index += len(items)

    return image_urls

def download_images(image_urls, download_dir, query):
    """
    Downloads images from the provided URLs.
    :param image_urls: List of image URLs to download.
    :param download_dir: Directory where images will be saved.
    :param query: Search query used for naming files.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            file_path = os.path.join(download_dir, f"{query}_{i + 1}.jpg")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Example usage
if __name__ == "__main__":
    search_term = input("enter term to search: ")  # Search term (class name)
    num_images_to_download = 1
    download_directory = fr'C:\Users\vkart\My Drive\mine\codes\python\learning\AI\dataset\{search_term}'
    if os.path.exists(download_directory):
        pass
    else:
        os.mkdir(download_directory)

    # Fetch image URLs
    image_urls = fetch_image_urls(query=search_term, num_images=num_images_to_download)
    
    # Download images
    download_images(image_urls=image_urls, download_dir=download_directory, query=search_term)

    print("Download completed!")
