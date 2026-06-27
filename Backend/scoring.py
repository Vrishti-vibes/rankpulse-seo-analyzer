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
        return "Excellent SEO foundation with minor optimization opportunities."
    if score >= 70:
        return "Good SEO structure, but some improvements are recommended."
    if score >= 50:
        return "Average SEO health. Several important fixes are required."
    return "Poor SEO health. The page needs major technical and content improvements."


def calculate_scores(report):
    on_page_score = 0
    technical_score = 0
    content_score = 0
    metadata_score = 0
    performance_score = 0

    if 30 <= report["title_length"] <= 60:
        on_page_score += 8
    elif report["title_length"] > 0:
        on_page_score += 4

    if 120 <= report["meta_description_length"] <= 160:
        on_page_score += 8
    elif report["meta_description_length"] > 0:
        on_page_score += 4

    if report["h1_count"] == 1:
        on_page_score += 6
    elif report["h1_count"] > 1:
        on_page_score += 3

    if report["h2_count"] > 0:
        on_page_score += 4

    if report["images_without_alt"] == 0:
        on_page_score += 4

    if report["https_enabled"]:
        technical_score += 5
    if report["robots_txt"]:
        technical_score += 5
    if report["sitemap_xml"]:
        technical_score += 5
    if report["canonical_tag"]:
        technical_score += 5
    if report["mobile_viewport"]:
        technical_score += 5

    if report["word_count"] >= 800:
        content_score += 8
    elif report["word_count"] >= 300:
        content_score += 5
    elif report["word_count"] > 0:
        content_score += 2

    if report["h2_count"] + report["h3_count"] >= 3:
        content_score += 4

    if report["internal_links"] > 0:
        content_score += 3

    if report["open_graph_tags"] > 0:
        metadata_score += 4
    if report["twitter_tags"] > 0:
        metadata_score += 3
    if report["structured_data"] > 0:
        metadata_score += 3

    if report["status_code"] == 200:
        performance_score += 8
    if report["total_images"] <= 20:
        performance_score += 4
    if report["mobile_viewport"]:
        performance_score += 4
    if report["word_count"] < 5000:
        performance_score += 4

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