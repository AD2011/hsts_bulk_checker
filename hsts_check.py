import sys
import subprocess
import urllib.parse
import re

def check_hsts(url):
    # Ensure the URL has a scheme
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    # Parse the URL to get the hostname
    hostname = urllib.parse.urlparse(url).hostname

    try:
        # Run the curl command and capture the output
        result = subprocess.run(['curl', '-s', '-D-', f'https://{hostname}'],
                                capture_output=True, text=True, timeout=10)

        # Check if the Strict-Transport-Security header is present
        hsts_header = re.search(r'strict-transport-security:\s*(.+)', result.stdout, re.IGNORECASE)
        if hsts_header:
            header_value = hsts_header.group(1).strip()
            return f"{url}: HSTS is enabled. Header value: {header_value}"
        else:
            return f"{url}: HSTS is not enabled"
    except subprocess.TimeoutExpired:
        return f"{url}: Connection timed out"
    except Exception as e:
        return f"{url}: Error occurred - {str(e)}"

def main(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.read().splitlines()

        for url in urls:
            print(check_hsts(url))

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        main(sys.argv[1])
