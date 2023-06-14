import feedparser

# URL of the RSS feed you want to parse
rss_url = "http://azure.microsoft.com/en-us/updates/feed/"

# Parse the feed
print("Parsing feed...")
feed = feedparser.parse(rss_url)
print("Feed parsed successfully!")

# Print the contents of the feed
print("Feed entries:")
for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Updated: {entry.updated}")
    print("---")
