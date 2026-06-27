import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from scoring import calculate_scores


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url


def check_file_exists(base_url: str, filename: str) -> bool:
    try:
        parsed = urlparse(base_url)
        file_url = f"{parsed.scheme}://{parsed.netloc}/{filename}"
        response = requests.get(file_url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def generate_check_items(report):
    checks = []

    def add(name, passed, category, detail):
        checks.append({
            "name": name,
            "passed": passed,
            "category": category,
            "detail": detail
        })

    add("SEO Title", 30 <= report["title_length"] <= 60, "On-Page SEO",
        f"Title length is {report['title_length']} characters.")
    add("Meta Description", 120 <= report["meta_description_length"] <= 160, "On-Page SEO",
        f"Meta description length is {report['meta_description_length']} characters.")
    add("Single H1 Tag", report["h1_count"] == 1, "On-Page SEO",
        f"Found {report['h1_count']} H1 tag(s).")
    add("Image Alt Text", report["images_without_alt"] == 0, "Accessibility",
        f"{report['images_without_alt']} image(s) missing alt text.")
    add("HTTPS Enabled", report["https_enabled"], "Technical SEO",
        "Website should use HTTPS.")
    add("Robots.txt", report["robots_txt"], "Technical SEO",
        "Robots.txt helps search engines understand crawling rules.")
    add("Sitemap.xml", report["sitemap_xml"], "Technical SEO",
        "Sitemap helps search engines discover pages.")
    add("Canonical Tag", report["canonical_tag"], "Technical SEO",
        "Canonical tag helps avoid duplicate content issues.")
    add("Mobile Viewport", report["mobile_viewport"], "Responsive Design",
        "Viewport tag is required for mobile responsiveness.")
    add("Open Graph Metadata", report["open_graph_tags"] > 0, "Metadata",
        f"Found {report['open_graph_tags']} Open Graph tag(s).")
    add("Structured Data", report["structured_data"] > 0, "Metadata",
        f"Found {report['structured_data']} structured data block(s).")
    add("Content Depth", report["word_count"] >= 300, "Content",
        f"Detected {report['word_count']} words.")

    return checks


def generate_suggestions(report):
    suggestions = []

    if not report["title"]:
        suggestions.append("Add a clear SEO title tag for the page.")
    elif report["title_length"] < 30:
        suggestions.append("Increase the title length to make it more descriptive.")
    elif report["title_length"] > 60:
        suggestions.append("Shorten the title tag to keep it under 60 characters.")

    if not report["meta_description"]:
        suggestions.append("Add a meta description between 140 and 160 characters.")
    elif report["meta_description_length"] < 120:
        suggestions.append("Make the meta description more detailed.")
    elif report["meta_description_length"] > 160:
        suggestions.append("Shorten the meta description to avoid truncation in search results.")

    if report["h1_count"] == 0:
        suggestions.append("Add one H1 tag that clearly describes the page topic.")
    elif report["h1_count"] > 1:
        suggestions.append("Use only one primary H1 tag for better heading structure.")

    if report["images_without_alt"] > 0:
        suggestions.append("Add descriptive alt text to all images for accessibility and image SEO.")

    if not report["robots_txt"]:
        suggestions.append("Add a robots.txt file to guide search engine crawlers.")

    if not report["sitemap_xml"]:
        suggestions.append("Add a sitemap.xml file to help search engines discover pages.")

    if not report["canonical_tag"]:
        suggestions.append("Add a canonical tag to avoid duplicate content issues.")

    if not report["mobile_viewport"]:
        suggestions.append("Add a mobile viewport meta tag for responsive design.")

    if report["open_graph_tags"] == 0:
        suggestions.append("Add Open Graph metadata for better social media sharing.")

    if report["structured_data"] == 0:
        suggestions.append("Add JSON-LD structured data where applicable.")

    if not suggestions:
        suggestions.append("Great job. The website follows many important SEO best practices.")

    return suggestions


def analyze_website(url: str):
    url = normalize_url(url)

    try:
        response = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "RankPulseSEOAnalyzer/1.0"}
        )

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        meta_description_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = meta_description_tag.get("content", "").strip() if meta_description_tag else ""

        viewport = soup.find("meta", attrs={"name": "viewport"})
        canonical = soup.find("link", attrs={"rel": "canonical"})

        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")

        images = soup.find_all("img")
        images_without_alt = [
            img for img in images
            if not img.get("alt") or img.get("alt").strip() == ""
        ]

        links = soup.find_all("a", href=True)
        parsed_domain = urlparse(url).netloc

        internal_links = []
        external_links = []

        for link in links:
            href = link.get("href")
            full_url = urljoin(url, href)
            link_domain = urlparse(full_url).netloc

            if link_domain == parsed_domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
        twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
        structured_data = soup.find_all("script", type="application/ld+json")

        text = soup.get_text(separator=" ")
        words = [word for word in text.split() if word.strip()]
        word_count = len(words)

        report = {
            "url": url,
            "title": title,
            "title_length": len(title),
            "meta_description": meta_description,
            "meta_description_length": len(meta_description),
            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "h3_count": len(h3_tags),
            "total_images": len(images),
            "images_without_alt": len(images_without_alt),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "https_enabled": url.startswith("https://"),
            "robots_txt": check_file_exists(url, "robots.txt"),
            "sitemap_xml": check_file_exists(url, "sitemap.xml"),
            "canonical_tag": canonical is not None,
            "mobile_viewport": viewport is not None,
            "open_graph_tags": len(og_tags),
            "twitter_tags": len(twitter_tags),
            "structured_data": len(structured_data),
            "word_count": word_count,
            "status_code": response.status_code,
        }

        scores = calculate_scores(report)
        report.update(scores)
        report["suggestions"] = generate_suggestions(report)
        report["checks"] = generate_check_items(report)

        return report

    except Exception as e:
        return {
            "url": url,
            "status": "failed",
            "error": str(e),
            "overall_score": 0,
            "grade": "D",
            "verdict": "Unable to analyze this website.",
            "suggestions": [
                "Check whether the URL is correct and publicly accessible."
            ],
            "checks": []
        }