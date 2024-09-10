#!/bin/bash

check_hsts() {
    url="$1"
    # Ensure the URL has a scheme
    if [[ ! $url =~ ^https?:// ]]; then
        url="https://$url"
    fi

    # Extract the hostname
    hostname=$(echo "$url" | awk -F[/:] '{print $4}')

    # Perform the curl request
    response=$(curl -s -D- "https://$hostname" 2>&1)

    # Check for HSTS header
    hsts_header=$(echo "$response" | grep -i "strict-transport-security:" | tr -d '\r')

    if [ -n "$hsts_header" ]; then
        echo "$url: HSTS is enabled. Header value: ${hsts_header#*: }"
    else
        echo "$url: HSTS is not enabled"
    fi
}

# Check if a file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <file_path>"
    exit 1
fi

file_path="$1"

# Check if the file exists
if [ ! -f "$file_path" ]; then
    echo "Error: File '$file_path' not found."
    exit 1
fi

# Read URLs from the file and check HSTS for each
while IFS= read -r url || [[ -n "$url" ]]; do
    check_hsts "$url"
done < "$file_path"
