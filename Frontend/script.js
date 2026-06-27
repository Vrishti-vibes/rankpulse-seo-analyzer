const API_BASE_URL = "http://127.0.0.1:8000";

async function startAnalysis() {
    const url = document.getElementById("urlInput").value.trim();
    const loading = document.getElementById("loading");
    const resultSection = document.getElementById("resultSection");

    if (!url) {
        alert("Please enter a website URL");
        return;
    }

    loading.classList.remove("d-none");
    resultSection.classList.add("d-none");

    try {
        const analyzeResponse = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        });

        const analyzeData = await analyzeResponse.json();

        const resultResponse = await fetch(`${API_BASE_URL}/api/results/${analyzeData.job_id}`);
        const result = await resultResponse.json();

        displayResults(result);

    } catch (error) {
        alert("Backend server is not running. Start FastAPI from backend folder.");
        console.error(error);
    } finally {
        loading.classList.add("d-none");
    }
}

function setProgress(id, value, total) {
    const percent = Math.min((value / total) * 100, 100);
    document.getElementById(id).style.width = `${percent}%`;
}

function displayResults(data) {
    document.getElementById("resultSection").classList.remove("d-none");

    document.getElementById("overallScore").innerText = data.overall_score || 0;
    document.getElementById("onPageScore").innerText = `${data.on_page_score || 0}/30`;
    document.getElementById("technicalScore").innerText = `${data.technical_score || 0}/25`;
    document.getElementById("performanceScore").innerText = `${data.performance_score || 0}/20`;
    document.getElementById("contentScore").innerText = `${data.content_score || 0}/15`;

    document.getElementById("scoreLabel").innerText = `SEO Grade ${data.grade || "D"}`;
    document.getElementById("verdictText").innerText = data.verdict || "SEO analysis completed.";

    const scoreStatus = document.getElementById("scoreStatus");
    scoreStatus.innerText = `Grade ${data.grade || "D"}`;

    setProgress("onPageBar", data.on_page_score || 0, 30);
    setProgress("technicalBar", data.technical_score || 0, 25);
    setProgress("performanceBar", data.performance_score || 0, 20);
    setProgress("contentBar", data.content_score || 0, 15);

    const details = [
        ["Analyzed URL", data.url],
        ["Page Title", data.title || "Not found"],
        ["Title Length", data.title_length],
        ["Meta Description Length", data.meta_description_length],
        ["H1 Tags", data.h1_count],
        ["H2 Tags", data.h2_count],
        ["H3 Tags", data.h3_count],
        ["Images Missing Alt", data.images_without_alt],
        ["Internal Links", data.internal_links],
        ["External Links", data.external_links],
        ["HTTPS", data.https_enabled ? "Enabled" : "Missing"],
        ["Robots.txt", data.robots_txt ? "Found" : "Missing"],
        ["Sitemap.xml", data.sitemap_xml ? "Found" : "Missing"],
        ["Canonical Tag", data.canonical_tag ? "Found" : "Missing"],
        ["Mobile Viewport", data.mobile_viewport ? "Found" : "Missing"],
        ["Open Graph Tags", data.open_graph_tags],
        ["Twitter Tags", data.twitter_tags],
        ["Structured Data", data.structured_data],
        ["Word Count", data.word_count]
    ];

    const websiteDetails = document.getElementById("websiteDetails");
    websiteDetails.innerHTML = details.map(item => `
        <div class="detail-item">
            <strong>${item[0]}</strong>
            <span>${item[1]}</span>
        </div>
    `).join("");

    const checkMatrix = document.getElementById("checkMatrix");
    checkMatrix.innerHTML = "";

    if (data.checks && data.checks.length > 0) {
        data.checks.forEach(check => {
            const div = document.createElement("div");
            div.className = "check-item";

            div.innerHTML = `
                <div class="check-icon ${check.passed ? "pass" : "fail"}">
                    ${check.passed ? "✓" : "!"}
                </div>
                <div>
                    <h4>${check.name}</h4>
                    <p><strong>${check.category}</strong> — ${check.detail}</p>
                </div>
            `;

            checkMatrix.appendChild(div);
        });
    }

    const suggestionsList = document.getElementById("suggestionsList");
    suggestionsList.innerHTML = "";

    data.suggestions.forEach(suggestion => {
        const li = document.createElement("li");
        li.innerText = suggestion;
        suggestionsList.appendChild(li);
    });

    window.scrollTo({
        top: document.getElementById("resultSection").offsetTop - 20,
        behavior: "smooth"
    });
}