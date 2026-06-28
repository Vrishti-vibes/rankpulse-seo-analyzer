import requests
import time
import re
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
        response = requests.get(file_url, timeout=6)
        return response.status_code == 200
    except Exception:
        return False


def analyze_url_structure(url: str):
    parsed = urlparse(url)
    path = parsed.path or "/"
    issues = []

    if "_" in path:
        issues.append("URL contains underscores.")
    if len(url) > 100:
        issues.append("URL is too long.")
    if any(char.isupper() for char in path):
        issues.append("URL contains uppercase letters.")
    if path.count("/") > 4:
        issues.append("URL depth is high.")
    if "?" in url:
        issues.append("URL contains query parameters.")

    return {
        "path": path,
        "seo_friendly": len(issues) == 0,
        "issues": issues
    }


def calculate_readability(text: str):
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = [w for w in text.split() if w.strip()]

    if not sentences:
        return {
            "average_sentence_length": 0,
            "readability_level": "Not enough content"
        }

    avg_sentence_length = round(len(words) / len(sentences), 2)

    if avg_sentence_length <= 15:
        level = "Easy to read"
    elif avg_sentence_length <= 22:
        level = "Moderate"
    else:
        level = "Difficult"

    return {
        "average_sentence_length": avg_sentence_length,
        "readability_level": level
    }


def keyword_density(text: str):
    clean_text = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    words = [w for w in clean_text.split() if len(w) > 3]

    stopwords = {
        "this", "that", "with", "from", "your", "have", "will", "they",
        "them", "about", "there", "their", "which", "when", "where",
        "what", "than", "then", "into", "also", "more", "were", "been",
        "only", "very", "some", "such", "over", "under", "through"
    }

    filtered = [w for w in words if w not in stopwords]
    total = len(filtered) if filtered else 1

    freq = {}
    for word in filtered:
        freq[word] = freq.get(word, 0) + 1

    top = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:10]

    return [
        {
            "keyword": word,
            "count": count,
            "density": round((count / total) * 100, 2)
        }
        for word, count in top
    ]


def validate_heading_hierarchy(heading_levels):
    if not heading_levels:
        return False

    previous = heading_levels[0]
    for current in heading_levels[1:]:
        if current - previous > 1:
            return False
        previous = current

    return True


def detect_social_links(links):
    social_domains = {
        "facebook": "facebook.com",
        "instagram": "instagram.com",
        "linkedin": "linkedin.com",
        "twitter": "twitter.com",
        "x": "x.com",
        "youtube": "youtube.com"
    }

    found = {}

    for link in links:
        href = link.get("href", "").lower()
        for name, domain in social_domains.items():
            if domain in href:
                found[name] = href

    return found


def check_broken_internal_links(internal_links):
    checked = []
    broken = []

    for link in list(set(internal_links))[:10]:
        try:
            response = requests.head(link, timeout=5, allow_redirects=True)
            checked.append(link)
            if response.status_code >= 400:
                broken.append(link)
        except Exception:
            broken.append(link)

    return {
        "checked_internal_links": len(checked),
        "broken_internal_links": len(broken)
    }


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

    add("Heading Hierarchy", report["heading_hierarchy_valid"], "Content",
        "Heading levels should follow a logical order.")

    add("Image Alt Text", report["images_without_alt"] == 0, "Accessibility",
        f"{report['images_without_alt']} image(s) missing alt text.")

    add("SEO-Friendly URL", report["url_structure"]["seo_friendly"], "Technical SEO",
        "Checks URL length, casing, path depth and query parameters.")

    add("HTTPS Enabled", report["https_enabled"], "Technical SEO",
        "Website should use HTTPS.")

    add("Redirect Handling", report["redirect_count"] <= 2, "Technical SEO",
        f"Detected {report['redirect_count']} redirect(s).")

    add("Indexability", report["indexable"], "Technical SEO",
        "Checks robots meta noindex directive.")

    add("Robots.txt", report["robots_txt"], "Technical SEO",
        "Robots.txt helps guide crawlers.")

    add("Sitemap.xml", report["sitemap_xml"], "Technical SEO",
        "Sitemap helps search engines discover pages.")

    add("Canonical Tag", report["canonical_tag"], "Technical SEO",
        "Canonical tag helps prevent duplicate content issues.")

    add("Mobile Viewport", report["mobile_viewport"], "Responsive Design",
        "Viewport tag supports mobile responsiveness.")

    add("Open Graph Metadata", report["open_graph_tags"] > 0, "Metadata",
        f"Found {report['open_graph_tags']} Open Graph tag(s).")

    add("Twitter Metadata", report["twitter_tags"] > 0, "Metadata",
        f"Found {report['twitter_tags']} Twitter metadata tag(s).")

    add("Structured Data", report["structured_data"] > 0, "Metadata",
        f"Found {report['structured_data']} structured data block(s).")

    add("Favicon", report["favicon_found"], "Trust Signal",
        "Favicon improves branding and browser visibility.")

    add("Language Attribute", report["language_found"], "Accessibility",
        "HTML lang attribute improves accessibility and SEO.")

    add("Charset Declaration", report["charset_found"], "Technical SEO",
        "Charset declaration improves correct page rendering.")

    add("Content Depth", report["word_count"] >= 300, "Content",
        f"Detected {report['word_count']} words.")

    add("Readability", report["readability"]["readability_level"] != "Difficult", "Content",
        f"Readability level: {report['readability']['readability_level']}.")

    add("Response Time", report["response_time_ms"] <= 3000, "Performance",
        f"Response time is {report['response_time_ms']} ms.")

    add("Page Size", report["page_size_kb"] <= 1024, "Performance",
        f"Page size is {report['page_size_kb']} KB.")

    add("Compression", report["compression_enabled"], "Performance",
        "Checks whether gzip/br compression is enabled.")

    add("Cache Headers", report["cache_headers_found"], "Performance",
        "Checks browser caching headers.")

    add("Broken Internal Links", report["broken_internal_links"] == 0, "Technical SEO",
        f"{report['broken_internal_links']} broken internal link(s) found in sampled links.")

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

    if not report["heading_hierarchy_valid"]:
        suggestions.append("Improve heading hierarchy. Avoid skipping heading levels.")

    if report["images_without_alt"] > 0:
        suggestions.append("Add descriptive alt text to all images for accessibility and image SEO.")

    if not report["url_structure"]["seo_friendly"]:
        suggestions.append("Improve URL structure using lowercase words, hyphens and shorter paths.")

    if report["redirect_count"] > 2:
        suggestions.append("Reduce redirect chains to improve crawl efficiency and loading performance.")

    if not report["indexable"]:
        suggestions.append("Remove noindex directive if this page should appear in search results.")

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

    if report["twitter_tags"] == 0:
        suggestions.append("Add Twitter Card metadata for improved link previews.")

    if report["structured_data"] == 0:
        suggestions.append("Add JSON-LD structured data where applicable.")

    if not report["favicon_found"]:
        suggestions.append("Add a favicon to improve trust and brand recognition.")

    if not report["language_found"]:
        suggestions.append("Add a lang attribute to the HTML tag for accessibility and SEO.")

    if not report["charset_found"]:
        suggestions.append("Add UTF-8 charset meta tag for correct text rendering.")

    if report["word_count"] < 300:
        suggestions.append("Increase content depth. Thin content can reduce SEO quality.")

    if report["readability"]["readability_level"] == "Difficult":
        suggestions.append("Improve readability using shorter sentences and clearer paragraph structure.")

    if report["response_time_ms"] > 3000:
        suggestions.append("Improve server response time for better performance and user experience.")

    if report["page_size_kb"] > 1024:
        suggestions.append("Reduce page size by compressing assets and optimizing images.")

    if not report["compression_enabled"]:
        suggestions.append("Enable gzip or Brotli compression to reduce transferred page size.")

    if not report["cache_headers_found"]:
        suggestions.append("Add cache headers to improve repeat visit performance.")

    if report["broken_internal_links"] > 0:
        suggestions.append("Fix broken internal links to improve crawlability and user experience.")

    if not suggestions:
        suggestions.append("Great job. The website follows many important SEO best practices.")

    return suggestions


def analyze_website(url: str):
    url = normalize_url(url)

    try:
        start_time = time.time()

        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "RankPulseSEOAnalyzer/1.0"},
            allow_redirects=True
        )

        end_time = time.time()

        response_time_ms = round((end_time - start_time) * 1000)
        page_size_kb = round(len(response.content) / 1024, 2)
        final_url = response.url
        redirect_count = len(response.history)

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        meta_description_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = meta_description_tag.get("content", "").strip() if meta_description_tag else ""

        viewport = soup.find("meta", attrs={"name": "viewport"})
        canonical = soup.find("link", attrs={"rel": "canonical"})
        charset = soup.find("meta", attrs={"charset": True})
        html_tag = soup.find("html")
        language_found = bool(html_tag and html_tag.get("lang"))

        robots_meta = soup.find("meta", attrs={"name": "robots"})
        robots_content = robots_meta.get("content", "").lower() if robots_meta else ""
        noindex = "noindex" in robots_content
        nofollow = "nofollow" in robots_content
        indexable = not noindex

        heading_tags = soup.find_all(re.compile("^h[1-6]$"))
        heading_levels = [int(tag.name[1]) for tag in heading_tags]
        heading_hierarchy_valid = validate_heading_hierarchy(heading_levels)

        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        h3_tags = soup.find_all("h3")
        h4_tags = soup.find_all("h4")
        h5_tags = soup.find_all("h5")
        h6_tags = soup.find_all("h6")

        images = soup.find_all("img")
        images_without_alt = [
            img for img in images
            if not img.get("alt") or img.get("alt").strip() == ""
        ]

        links = soup.find_all("a", href=True)
        parsed_domain = urlparse(final_url).netloc

        internal_links = []
        external_links = []

        for link in links:
            href = link.get("href")
            full_url = urljoin(final_url, href)
            link_domain = urlparse(full_url).netloc

            if link_domain == parsed_domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        broken_link_result = check_broken_internal_links(internal_links)

        og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
        twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
        structured_data_json = soup.find_all("script", type="application/ld+json")
        schema_items = soup.find_all(attrs={"itemtype": True})

        favicon = soup.find("link", rel=lambda x: x and "icon" in str(x).lower())

        text = soup.get_text(separator=" ")
        clean_text = " ".join(text.split())
        words = [word for word in clean_text.split() if word.strip()]
        word_count = len(words)

        social_links = detect_social_links(links)
        email_found = bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html))
        phone_found = bool(re.search(r"(\+?\d[\d\s\-()]{8,}\d)", html))

        compression_enabled = response.headers.get("content-encoding", "").lower() in ["gzip", "br", "deflate"]
        cache_headers_found = bool(response.headers.get("cache-control") or response.headers.get("expires"))

        report = {
            "url": url,
            "final_url": final_url,
            "status": "completed",
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "page_size_kb": page_size_kb,
            "redirect_count": redirect_count,

            "title": title,
            "title_length": len(title),
            "meta_description": meta_description,
            "meta_description_length": len(meta_description),

            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "h3_count": len(h3_tags),
            "h4_count": len(h4_tags),
            "h5_count": len(h5_tags),
            "h6_count": len(h6_tags),
            "heading_hierarchy_valid": heading_hierarchy_valid,

            "total_images": len(images),
            "images_without_alt": len(images_without_alt),

            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "checked_internal_links": broken_link_result["checked_internal_links"],
            "broken_internal_links": broken_link_result["broken_internal_links"],

            "https_enabled": final_url.startswith("https://"),
            "robots_txt": check_file_exists(final_url, "robots.txt"),
            "sitemap_xml": check_file_exists(final_url, "sitemap.xml"),
            "canonical_tag": canonical is not None,
            "mobile_viewport": viewport is not None,
            "charset_found": charset is not None,
            "language_found": language_found,
            "favicon_found": favicon is not None,

            "open_graph_tags": len(og_tags),
            "twitter_tags": len(twitter_tags),
            "structured_data": len(structured_data_json) + len(schema_items),
            "json_ld_blocks": len(structured_data_json),
            "schema_items": len(schema_items),

            "robots_meta": robots_content if robots_content else "Not found",
            "noindex": noindex,
            "nofollow": nofollow,
            "indexable": indexable,

            "word_count": word_count,
            "readability": calculate_readability(clean_text),
            "top_keywords": keyword_density(clean_text),

            "url_structure": analyze_url_structure(final_url),
            "social_links": social_links,
            "social_profiles_found": len(social_links),
            "email_found": email_found,
            "phone_found": phone_found,
            "compression_enabled": compression_enabled,
            "cache_headers_found": cache_headers_found,
        }

        scores = calculate_scores(report)
        report.update(scores)
        report["checks"] = generate_check_items(report)
        report["suggestions"] = generate_suggestions(report)

        return report

    except Exception as e:
        return {
            "url": url,
            "status": "failed",
            "error": str(e),
            "overall_score": 0,
            "grade": "D",
            "verdict": "Unable to analyze this website.",
            "checks": [],
            "suggestions": [
                "Check whether the URL is correct and publicly accessible."
            ]
        }