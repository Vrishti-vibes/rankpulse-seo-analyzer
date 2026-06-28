def get_grade(score):
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B+"
    if score >= 60:
        return "B"
    if score >= 45:
        return "C"
    return "D"


def get_verdict(score):
    if score >= 85:
        return "Excellent SEO foundation with strong technical and content signals."
    if score >= 70:
        return "Good SEO structure with some improvement opportunities."
    if score >= 50:
        return "Average SEO health. Several important fixes are required."
    return "Poor SEO health. Major technical, content and metadata improvements are needed."


def calculate_scores(report):
    on_page_score = 0
    technical_score = 0
    content_score = 0
    metadata_score = 0
    performance_score = 0

    # On-Page SEO: 30
    if 30 <= report["title_length"] <= 60:
        on_page_score += 6
    elif report["title_length"] > 0:
        on_page_score += 3

    if 120 <= report["meta_description_length"] <= 160:
        on_page_score += 6
    elif report["meta_description_length"] > 0:
        on_page_score += 3

    if report["h1_count"] == 1:
        on_page_score += 5
    elif report["h1_count"] > 1:
        on_page_score += 2

    if report["h2_count"] > 0:
        on_page_score += 3

    if report["heading_hierarchy_valid"]:
        on_page_score += 4

    if report["images_without_alt"] == 0:
        on_page_score += 4

    if on_page_score > 30:
        on_page_score = 30

    # Technical SEO: 25
    if report["https_enabled"]:
        technical_score += 3
    if report["robots_txt"]:
        technical_score += 3
    if report["sitemap_xml"]:
        technical_score += 3
    if report["canonical_tag"]:
        technical_score += 3
    if report["mobile_viewport"]:
        technical_score += 3
    if report["url_structure"]["seo_friendly"]:
        technical_score += 3
    if report["indexable"]:
        technical_score += 3
    if report["charset_found"]:
        technical_score += 2
    if report["language_found"]:
        technical_score += 2

    if technical_score > 25:
        technical_score = 25

    # Content Quality: 15
    if report["word_count"] >= 800:
        content_score += 5
    elif report["word_count"] >= 300:
        content_score += 3
    elif report["word_count"] > 0:
        content_score += 1

    if report["h2_count"] + report["h3_count"] >= 3:
        content_score += 3

    if report["internal_links"] > 0:
        content_score += 2

    if report["readability"]["readability_level"] in ["Easy to read", "Moderate"]:
        content_score += 3

    if len(report["top_keywords"]) > 0:
        content_score += 2

    if content_score > 15:
        content_score = 15

    # Metadata: 10
    if report["open_graph_tags"] > 0:
        metadata_score += 3
    if report["twitter_tags"] > 0:
        metadata_score += 2
    if report["structured_data"] > 0:
        metadata_score += 3
    if report["favicon_found"]:
        metadata_score += 2

    if metadata_score > 10:
        metadata_score = 10

    # Performance Basics: 20
    if report["status_code"] == 200:
        performance_score += 4

    if report["response_time_ms"] <= 1500:
        performance_score += 4
    elif report["response_time_ms"] <= 3000:
        performance_score += 2

    if report["page_size_kb"] <= 512:
        performance_score += 4
    elif report["page_size_kb"] <= 1024:
        performance_score += 2

    if report["redirect_count"] <= 1:
        performance_score += 3
    elif report["redirect_count"] <= 2:
        performance_score += 1

    if report["compression_enabled"]:
        performance_score += 3

    if report["cache_headers_found"]:
        performance_score += 2

    if performance_score > 20:
        performance_score = 20

    overall_score = (
        on_page_score +
        technical_score +
        content_score +
        metadata_score +
        performance_score
    )

    return {
        "on_page_score": on_page_score,
        "technical_score": technical_score,
        "content_score": content_score,
        "metadata_score": metadata_score,
        "performance_score": performance_score,
        "overall_score": overall_score,
        "grade": get_grade(overall_score),
        "verdict": get_verdict(overall_score)
    }