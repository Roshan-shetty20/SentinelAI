/* ============================================================
   SENTINEL AI
   MAIN JAVASCRIPT

   Robot Effects
   Robot Family
   Custom Cursor
   Radar
   URL Analyzer
   FastAPI Integration
   Navigation
   Scroll Animations
============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ========================================================
       ELEMENTS
    ======================================================== */

    const robot = document.getElementById("robot");

    const robotMessage =
        document.getElementById("robotMessage");

    const robotMessageText =
        document.getElementById("robotMessageText");

    const robotStatus =
        document.querySelector(".robot-status");

    const scannerStatusText =
        document.getElementById("scannerStatusText");

    const analyzeButton =
        document.getElementById("analyzeButton");

    const urlInput =
        document.getElementById("urlInput");

    const analysisResult =
        document.getElementById("analysisResult");

    const resultTitle =
        document.getElementById("resultTitle");

    const resultUrl =
        document.getElementById("resultUrl");

    const resultRisk =
        document.getElementById("resultRisk");

    const resultConfidence =
        document.getElementById("resultConfidence");

    const featureCards =
        document.querySelectorAll(".feature-card");

    const glow =
        document.querySelector(".glow-1");


    /* ========================================================
       CUSTOM CYBER CURSOR
    ======================================================== */

    const cursor =
        document.createElement("div");

    cursor.className = "cyber-cursor";


    const cursorRing =
        document.createElement("div");

    cursorRing.className = "cursor-ring";


    const cursorCrosshair =
        document.createElement("div");

    cursorCrosshair.className =
        "cursor-crosshair";


    document.body.appendChild(cursorRing);
    document.body.appendChild(cursorCrosshair);
    document.body.appendChild(cursor);


    let mouseX = 0;
    let mouseY = 0;

    let ringX = 0;
    let ringY = 0;


    /* ========================================================
       CURSOR MOVEMENT
    ======================================================== */

    document.addEventListener(
        "mousemove",
        (event) => {

            mouseX = event.clientX;
            mouseY = event.clientY;


            cursor.style.left =
                `${mouseX}px`;

            cursor.style.top =
                `${mouseY}px`;


            cursorCrosshair.style.left =
                `${mouseX}px`;

            cursorCrosshair.style.top =
                `${mouseY}px`;


            if (glow) {

                glow.style.transform =
                    `translate(
                        ${mouseX * 0.015}px,
                        ${mouseY * 0.015}px
                    )`;
            }
        }
    );


    /* ========================================================
       SMOOTH CURSOR RING
    ======================================================== */

    function animateCursorRing() {

        ringX +=
            (mouseX - ringX) * 0.15;

        ringY +=
            (mouseY - ringY) * 0.15;


        cursorRing.style.left =
            `${ringX}px`;

        cursorRing.style.top =
            `${ringY}px`;


        requestAnimationFrame(
            animateCursorRing
        );
    }


    animateCursorRing();


    /* ========================================================
       CURSOR HOVER
    ======================================================== */

    document.addEventListener(
        "mouseover",
        (event) => {

            const target =
                event.target;


            const interactive =
                target.closest(
                    "a, button, .feature-card, .robot, .family-card"
                );


            if (interactive) {

                cursor.classList.add(
                    "hovering"
                );

                cursorRing.classList.add(
                    "hovering"
                );
            }
        }
    );


    document.addEventListener(
        "mouseout",
        (event) => {

            const target =
                event.target;


            const interactive =
                target.closest(
                    "a, button, .feature-card, .robot, .family-card"
                );


            if (
                interactive &&
                !interactive.contains(
                    event.relatedTarget
                )
            ) {

                cursor.classList.remove(
                    "hovering"
                );

                cursorRing.classList.remove(
                    "hovering"
                );
            }
        }
    );


    /* ========================================================
       CURSOR CLICK EFFECT
    ======================================================== */

    document.addEventListener(
        "mousedown",
        () => {

            cursor.classList.add(
                "click"
            );
        }
    );


    document.addEventListener(
        "mouseup",
        () => {

            cursor.classList.remove(
                "click"
            );
        }
    );


    /* ========================================================
       ORIGINAL SENTINEL ROBOT
    ======================================================== */

    if (robot) {

        /* ----------------------------------------------------
           ROBOT HOVER
        ---------------------------------------------------- */

        robot.addEventListener(
            "mouseenter",
            () => {

                robot.classList.add(
                    "danger"
                );


                cursor.classList.add(
                    "robot-target"
                );

                cursorRing.classList.add(
                    "robot-target"
                );


                if (robotMessage) {

                    robotMessage.classList.add(
                        "danger-message"
                    );
                }


                if (robotMessageText) {

                    robotMessageText.textContent =
                        "⚠ Suspicious activity detected!";
                }


                if (robotStatus) {

                    robotStatus.textContent =
                        "● THREAT DETECTED";

                    robotStatus.style.color =
                        "#ff2020";
                }
            }
        );


        /* ----------------------------------------------------
           ROBOT LEAVE
        ---------------------------------------------------- */

        robot.addEventListener(
            "mouseleave",
            () => {

                robot.classList.remove(
                    "danger"
                );


                cursor.classList.remove(
                    "robot-target"
                );

                cursorRing.classList.remove(
                    "robot-target"
                );


                if (robotMessage) {

                    robotMessage.classList.remove(
                        "danger-message"
                    );
                }


                if (robotMessageText) {

                    robotMessageText.textContent =
                        "No threats detected. System secure.";
                }


                if (robotStatus) {

                    robotStatus.textContent =
                        "● ACTIVE";

                    robotStatus.style.color =
                        "";
                }
            }
        );


        /* ----------------------------------------------------
           ROBOT CLICK
        ---------------------------------------------------- */

        robot.addEventListener(
            "click",
            () => {

                robot.classList.add(
                    "robot-scan"
                );


                setTimeout(
                    () => {

                        robot.classList.remove(
                            "robot-scan"
                        );

                    },
                    700
                );
            }
        );
    }


    /* ========================================================
       ROBOT FAMILY
    ======================================================== */

    const familyCards =
        document.querySelectorAll(
            ".family-card"
        );


    /* --------------------------------------------------------
       SENTINEL
       Primary security intelligence
    -------------------------------------------------------- */

    const sentinelAgent =
        document.querySelector(
            ".sentinel-agent"
        );


    /* --------------------------------------------------------
       SCOUT
       Reconnaissance
    -------------------------------------------------------- */

    const scoutAgent =
        document.querySelector(
            ".scout-agent"
        );


    /* --------------------------------------------------------
       NEXUS
       AI intelligence
    -------------------------------------------------------- */

    const nexusAgent =
        document.querySelector(
            ".nexus-agent"
        );


    /* --------------------------------------------------------
       WARDEN
       Threat response
    -------------------------------------------------------- */

    const wardenAgent =
        document.querySelector(
            ".warden-agent"
        );


    /* ========================================================
       FAMILY CARD INTERACTION
    ======================================================== */

    familyCards.forEach(
        (card) => {

            card.addEventListener(
                "mouseenter",
                () => {

                    card.classList.add(
                        "agent-hover"
                    );


                    const role =
                        getAgentRole(card);


                    setFamilyMessage(
                        card,
                        "ACTIVE",
                        role
                    );
                }
            );


            card.addEventListener(
                "mouseleave",
                () => {

                    card.classList.remove(
                        "agent-hover"
                    );


                    stopAgentBehavior(
                        card
                    );
                }
            );
        }
    );


    /* ========================================================
       GET AGENT ROLE
    ======================================================== */

    function getAgentRole(card) {

        if (
            card.classList.contains(
                "sentinel-agent"
            )
        ) {

            return "PRIMARY DEFENSE";
        }


        if (
            card.classList.contains(
                "scout-agent"
            )
        ) {

            return "URL RECON";
        }


        if (
            card.classList.contains(
                "nexus-agent"
            )
        ) {

            return "AI INTELLIGENCE";
        }


        if (
            card.classList.contains(
                "warden-agent"
            )
        ) {

            return "THREAT RESPONSE";
        }


        return "ONLINE";
    }


    /* ========================================================
       FAMILY MESSAGE
    ======================================================== */

    function setFamilyMessage(
        card,
        status,
        role
    ) {

        const statusElement =
            card.querySelector(
                ".agent-status"
            );


        if (!statusElement) {
            return;
        }


        if (
            card.classList.contains(
                "sentinel-agent"
            )
        ) {

            statusElement.innerHTML =
                `<span></span> ${status}`;
        }


        if (
            card.classList.contains(
                "scout-agent"
            )
        ) {

            statusElement.innerHTML =
                `<span></span> SCANNING`;
        }


        if (
            card.classList.contains(
                "nexus-agent"
            )
        ) {

            statusElement.innerHTML =
                `<span></span> PROCESSING`;
        }


        if (
            card.classList.contains(
                "warden-agent"
            )
        ) {

            statusElement.innerHTML =
                `<span></span> MONITORING`;
        }
    }


    /* ========================================================
       STOP AGENT BEHAVIOR
    ======================================================== */

    function stopAgentBehavior(card) {

        card.classList.remove(
            "agent-hover",
            "agent-searching",
            "agent-processing",
            "agent-defense",
            "agent-alert"
        );


        const statusElement =
            card.querySelector(
                ".agent-status"
            );


        if (!statusElement) {
            return;
        }


        statusElement.innerHTML =
            `<span></span> ONLINE`;
    }


    /* ========================================================
       SCOUT BEHAVIOR
    ======================================================== */

    if (scoutAgent) {

        scoutAgent.addEventListener(
            "mouseenter",
            () => {

                scoutAgent.classList.add(
                    "agent-searching"
                );
            }
        );
    }


    /* ========================================================
       NEXUS BEHAVIOR
    ======================================================== */

    if (nexusAgent) {

        nexusAgent.addEventListener(
            "mouseenter",
            () => {

                nexusAgent.classList.add(
                    "agent-processing"
                );
            }
        );
    }


    /* ========================================================
       WARDEN BEHAVIOR
    ======================================================== */

    if (wardenAgent) {

        wardenAgent.addEventListener(
            "mouseenter",
            () => {

                wardenAgent.classList.add(
                    "agent-defense"
                );
            }
        );
    }


    /* ========================================================
       SENTINEL FAMILY BEHAVIOR
    ======================================================== */

    if (sentinelAgent) {

        sentinelAgent.addEventListener(
            "click",
            () => {

                sentinelAgent.classList.add(
                    "agent-alert"
                );


                setTimeout(
                    () => {

                        sentinelAgent.classList.remove(
                            "agent-alert"
                        );

                    },
                    900
                );
            }
        );
    }


    /* ========================================================
       LIVE RADAR STATUS
    ======================================================== */

    const scannerMessages = [

        "Scanning global threat signals...",

        "Analyzing suspicious patterns...",

        "Monitoring phishing indicators...",

        "Checking threat intelligence...",

        "Analyzing network signals...",

        "AI threat engine active..."
    ];


    let scannerIndex = 0;


    if (scannerStatusText) {

        setInterval(
            () => {

                scannerIndex =
                    (
                        scannerIndex + 1
                    ) %
                    scannerMessages.length;


                scannerStatusText.style.opacity =
                    "0";


                setTimeout(
                    () => {

                        scannerStatusText.textContent =
                            scannerMessages[
                                scannerIndex
                            ];


                        scannerStatusText.style.opacity =
                            "1";

                    },
                    250
                );

            },
            2500
        );
    }


    /* ========================================================
       FEATURE CARD SCROLL ANIMATION
    ======================================================== */

    if (featureCards.length > 0) {

        const cardObserver =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target.classList.add(
                                    "visible"
                                );
                            }
                        }
                    );
                },
                {
                    threshold: 0.15
                }
            );


        featureCards.forEach(
            (card) => {

                cardObserver.observe(
                    card
                );
            }
        );
    }


    /* ========================================================
       URL ANALYZER
    ======================================================== */

    async function analyzeURL() {

        const url =
            urlInput
                ? urlInput.value.trim()
                : "";


        /* ----------------------------------------------------
           EMPTY URL
        ---------------------------------------------------- */

        if (!url) {

            showResult(
                "error",
                "Please enter a URL.",
                "",
                "",
                ""
            );

            return;
        }


        /* ----------------------------------------------------
           URL VALIDATION
        ---------------------------------------------------- */

        let validURL;


        try {

            validURL =
                new URL(url);

        } catch {

            showResult(
                "error",
                "Invalid URL",
                "Please enter a valid URL such as https://example.com",
                "",
                ""
            );

            return;
        }


        /* ----------------------------------------------------
           HTTP / HTTPS ONLY
        ---------------------------------------------------- */

        if (
            validURL.protocol !== "http:" &&
            validURL.protocol !== "https:"
        ) {

            showResult(
                "error",
                "Invalid URL",
                "Only HTTP and HTTPS URLs are supported.",
                "",
                ""
            );

            return;
        }


        /* ====================================================
           ANALYZING STATE
        ==================================================== */

        if (analysisResult) {

            analysisResult.style.display =
                "block";


            analysisResult.classList.remove(
                "result-scam",
                "result-legitimate",
                "result-error"
            );
        }


        if (resultTitle) {

            resultTitle.textContent =
                "⟳ ANALYZING URL...";
        }


        if (resultUrl) {

            resultUrl.textContent =
                `URL: ${url}`;
        }


        if (resultRisk) {

            resultRisk.textContent =
                "Risk Score: Calculating...";
        }


        if (resultConfidence) {

            resultConfidence.textContent =
                "Confidence: Calculating...";
        }


        /* ====================================================
           DISABLE BUTTON
        ==================================================== */

        if (analyzeButton) {

            analyzeButton.disabled =
                true;


            analyzeButton.innerHTML =
                "Analyzing...";
        }


        /* ====================================================
           SENTINEL SCANNING
        ==================================================== */

        if (robot) {

            robot.classList.add(
                "robot-scanning"
            );
        }


        if (robotMessageText) {

            robotMessageText.textContent =
                "◉ AI threat engine analyzing URL...";
        }


        /* ====================================================
           FAMILY ROBOTS ACTIVATE
        ==================================================== */

        activateFamilyAnalysis();


        /* ====================================================
           BACKEND REQUEST
        ==================================================== */

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/api/analyze-url",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Accept":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                url: url
                            })
                    }
                );


            /* ------------------------------------------------
               READ RESPONSE
            ------------------------------------------------ */

            let data;


            try {

                data =
                    await response.json();

            } catch {

                throw new Error(
                    "Backend returned an invalid response."
                );
            }


            /* ------------------------------------------------
               BACKEND ERROR
            ------------------------------------------------ */

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Backend returned an error."
                );
            }


            console.log(
                "SentinelAI API Response:",
                data
            );


            /* =================================================
               MODEL RESULT
            ================================================= */

            const rawPrediction =
    String(
        data.prediction || ""
    ).toLowerCase();

const prediction = rawPrediction;


            const riskScore =
                Number(
                    data.risk_score
                );


            const confidence =
                Number(
                    data.confidence
                );


                        if (document.getElementById("urlReasons")) {
                document.getElementById("urlReasons").innerHTML = (data.reasons || []).map(r => `<div class="reason-item"><span>•</span>${r}</div>`).join("");
            }
            if (document.getElementById("urlExplanation")) {
                document.getElementById("urlExplanation").textContent = data.explainable_ai?.summary || "No explanation provided.";
            }
            if (document.getElementById("urlRiskComp") && data.components) {
                document.getElementById("urlRiskComp").textContent = (data.components.url_risk?.risk_score || 0).toFixed(2) + "%";
            }

            /* =================================================
               STOP SCANNING
            ================================================= */

            if (robot) {

                robot.classList.remove(
                    "robot-scanning"
                );
            }


            stopFamilyAnalysis();


            /* =================================================
               PHISHING
            ================================================= */

            if (
                prediction === "scam"
            ) {

                showResult(
                    "scam",
                    "⚠ PHISHING DETECTED",
                    data.url || url,
                    riskScore,
                    confidence
                );


                /* ---------------------------------------------
                   SENTINEL DANGER
                --------------------------------------------- */

                if (robot) {

                    robot.classList.add(
                        "danger"
                    );
                }


                if (robotMessage) {

                    robotMessage.classList.add(
                        "danger-message"
                    );
                }


                if (robotMessageText) {

                    robotMessageText.textContent =
                        "⚠ Phishing threat detected!";
                }


                if (robotStatus) {

                    robotStatus.textContent =
                        "● THREAT DETECTED";

                    robotStatus.style.color =
                        "#ff2020";
                }


                /* ---------------------------------------------
                   FAMILY RESPONSE
                --------------------------------------------- */

                activateFamilyThreat();
            }


            /* =================================================
               LEGITIMATE
            ================================================= */

            else {

                showResult(
                    "legitimate",
                    "✓ LEGITIMATE URL",
                    data.url || url,
                    riskScore,
                    confidence
                );


                if (robot) {

                    robot.classList.remove(
                        "danger"
                    );
                }


                if (robotMessage) {

                    robotMessage.classList.remove(
                        "danger-message"
                    );
                }


                if (robotMessageText) {

                    robotMessageText.textContent =
                        "✓ URL appears legitimate.";
                }


                if (robotStatus) {

                    robotStatus.textContent =
                        "● SECURE";

                    robotStatus.style.color =
                        "#00ff88";
                }


                /* ---------------------------------------------
                   FAMILY SECURE
                --------------------------------------------- */

                activateFamilySecure();
            }


        } catch (error) {

            console.error(
                "SentinelAI Error:",
                error
            );


            let errorMessage =
                error.message;


            if (
                error.message.includes(
                    "Failed to fetch"
                )
            ) {

                errorMessage =
                    "Cannot connect to SentinelAI backend. Make sure FastAPI is running on port 8000.";
            }


            showResult(
                "error",
                "Unable to analyze URL",
                errorMessage,
                "",
                ""
            );


            /* ---------------------------------------------
               ORIGINAL ROBOT ERROR
            --------------------------------------------- */

            if (robot) {

                robot.classList.remove(
                    "robot-scanning"
                );
            }


            if (robotMessageText) {

                robotMessageText.textContent =
                    "⚠ Unable to connect to threat engine.";
            }


            if (robotStatus) {

                robotStatus.textContent =
                    "● OFFLINE";

                robotStatus.style.color =
                    "#ff2020";
            }


            stopFamilyAnalysis();
        }


        /* ====================================================
           RESTORE BUTTON
        ==================================================== */

        finally {

            if (analyzeButton) {

                analyzeButton.disabled =
                    false;


                analyzeButton.innerHTML =
                    'Analyze URL <span>→</span>';
            }
        }
    }


    /* ========================================================
       FAMILY — ANALYSIS MODE
    ======================================================== */

    function activateFamilyAnalysis() {

        if (scoutAgent) {

            scoutAgent.classList.add(
                "agent-searching"
            );


            setFamilyStatus(
                scoutAgent,
                "SCANNING"
            );
        }


        if (nexusAgent) {

            nexusAgent.classList.add(
                "agent-processing"
            );


            setFamilyStatus(
                nexusAgent,
                "PROCESSING"
            );
        }


        if (wardenAgent) {

            setFamilyStatus(
                wardenAgent,
                "MONITORING"
            );
        }


        if (sentinelAgent) {

            setFamilyStatus(
                sentinelAgent,
                "ANALYZING"
            );
        }
    }


    /* ========================================================
       FAMILY — STOP ANALYSIS
    ======================================================== */

    function stopFamilyAnalysis() {

        if (scoutAgent) {

            scoutAgent.classList.remove(
                "agent-searching"
            );
        }


        if (nexusAgent) {

            nexusAgent.classList.remove(
                "agent-processing"
            );
        }
    }


    /* ========================================================
       FAMILY — THREAT MODE
    ======================================================== */

    function activateFamilyThreat() {

        if (sentinelAgent) {

            sentinelAgent.classList.add(
                "agent-alert"
            );


            setFamilyStatus(
                sentinelAgent,
                "THREAT"
            );
        }


        if (scoutAgent) {

            setFamilyStatus(
                scoutAgent,
                "THREAT FOUND"
            );
        }


        if (nexusAgent) {

            setFamilyStatus(
                nexusAgent,
                "MODEL ALERT"
            );
        }


        if (wardenAgent) {

            wardenAgent.classList.add(
                "agent-defense"
            );


            setFamilyStatus(
                wardenAgent,
                "DEFENDING"
            );
        }
    }


    /* ========================================================
       FAMILY — SECURE MODE
    ======================================================== */

    function activateFamilySecure() {

        if (sentinelAgent) {

            setFamilyStatus(
                sentinelAgent,
                "SECURE"
            );
        }


        if (scoutAgent) {

            setFamilyStatus(
                scoutAgent,
                "CLEAR"
            );
        }


        if (nexusAgent) {

            setFamilyStatus(
                nexusAgent,
                "CONFIRMED"
            );
        }


        if (wardenAgent) {

            setFamilyStatus(
                wardenAgent,
                "STANDBY"
            );
        }
    }


    /* ========================================================
       SET FAMILY STATUS
    ======================================================== */

    function setFamilyStatus(
        card,
        text
    ) {

        if (!card) {
            return;
        }


        const status =
            card.querySelector(
                ".agent-status"
            );


        if (!status) {
            return;
        }


        status.innerHTML =
            `<span></span> ${text}`;
    }


    /* ========================================================
       DISPLAY RESULT
    ======================================================== */

    function showResult(
        type,
        title,
        url,
        risk,
        confidence
    ) {

        if (!analysisResult) {
            return;
        }


        analysisResult.style.display =
            "block";


        analysisResult.classList.remove(
            "result-scam",
            "result-legitimate",
            "result-error"
        );


        if (type === "scam") {

            analysisResult.classList.add(
                "result-scam"
            );
        }


        if (type === "legitimate") {

            analysisResult.classList.add(
                "result-legitimate"
            );
        }


        if (type === "error") {

            analysisResult.classList.add(
                "result-error"
            );
        }


        if (resultTitle) {

            resultTitle.textContent =
                title;
        }


        if (resultUrl) {

            resultUrl.textContent =
                url
                    ? `URL: ${url}`
                    : "";
        }


        if (resultRisk) {

            resultRisk.textContent =
                risk !== "" &&
                !Number.isNaN(
                    Number(risk)
                )
                    ? `Risk Score: ${Number(risk).toFixed(2)}/100`
                    : "";
        }


        if (resultConfidence) {

            resultConfidence.textContent =
                confidence !== "" &&
                !Number.isNaN(
                    Number(confidence)
                )
                    ? `Confidence: ${Number(confidence).toFixed(2)}%`
                    : "";
        }
    }


    /* ========================================================
       ANALYZE BUTTON
    ======================================================== */

    if (analyzeButton) {

        analyzeButton.addEventListener(
            "click",
            analyzeURL
        );
    }


    /* ========================================================
       ENTER KEY
    ======================================================== */

    if (urlInput) {

        urlInput.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter"
                ) {

                    event.preventDefault();

                    analyzeURL();
                }
            }
        );
    }


    /* ========================================================
       NAVIGATION ACTIVE STATE
    ======================================================== */

    const navLinks =
        document.querySelectorAll(
            "nav a"
        );


    navLinks.forEach(
        (link) => {

            link.addEventListener(
                "click",
                () => {

                    navLinks.forEach(
                        (item) => {

                            item.classList.remove(
                                "active"
                            );
                        }
                    );


                    link.classList.add(
                        "active"
                    );
                }
            );
        }
    );


    /* ========================================================
       SMOOTH SCROLL
    ======================================================== */

    document.querySelectorAll(
        'a[href^="#"]'
    ).forEach(
        (link) => {

            link.addEventListener(
                "click",
                (event) => {

                    const targetId =
                        link.getAttribute(
                            "href"
                        );


                    if (
                        targetId &&
                        targetId !== "#"
                    ) {

                        const target =
                            document.querySelector(
                                targetId
                            );


                        if (target) {

                            event.preventDefault();


                            target.scrollIntoView({
                                behavior:
                                    "smooth"
                            });
                        }
                    }
                }
            );
        }
    );


    /* ========================================================
       SENTINEL CONSOLE
    ======================================================== */

    console.log(
        "%c SENTINEL AI ",
        "background:#ff6600;color:#000;font-weight:bold;padding:6px 10px;border-radius:4px;"
    );


    console.log(
        "AI Threat Intelligence System initialized."
    );


    console.log(
        "Robot Family initialized: Sentinel | Scout | Nexus | Warden"
    );

});


// ============================================================
// MESSAGE ANALYZER
// ============================================================

async function analyzeMessage() {

    const messageInput =
        document.getElementById("messageInput");

    const analyzeBtn =
        document.getElementById("analyzeMessageBtn");

    const resultBox =
        document.getElementById("messageAnalysisResult");

    const resultTitle =
        document.getElementById("messageResultTitle");

    const riskBadge =
        document.getElementById("messageRiskBadge");

    const confidence =
        document.getElementById("messageConfidence");

    const confidenceFill =
        document.getElementById("messageConfidenceFill");

    const reasons =
        document.getElementById("messageReasons");

    const analyzedMessage =
        document.getElementById("analyzedMessageText");

    // MESSAGE RESULT COLORS
if (resultBox) {
    resultBox.classList.remove(
        "scam-result",
        "safe-result"
    );
}

    // ========================================================
    // GET MESSAGE
    // ========================================================

    const message =
        messageInput
            ? messageInput.value.trim()
            : "";


    // ========================================================
    // CHECK EMPTY MESSAGE
    // ========================================================

    if (!message) {

        alert(
            "Please enter a message to analyze."
        );

        if (messageInput) {
            messageInput.focus();
        }

        return;
    }


    // ========================================================
    // BUTTON LOADING STATE
    // ========================================================

    if (analyzeBtn) {

        analyzeBtn.disabled = true;

        analyzeBtn.innerHTML =
            "Analyzing...";
    }


    // ========================================================
    // SHOW RESULT BOX
    // ========================================================

    if (resultBox) {

        resultBox.style.display =
            "block";
    }


    // ========================================================
    // LOADING UI
    // ========================================================

    if (resultTitle) {

        resultTitle.textContent =
            "⟳ ANALYZING MESSAGE...";
    }

    if (riskBadge) {

        riskBadge.textContent =
            "ANALYZING";
    }

    if (confidence) {

        confidence.textContent =
            "Calculating...";
    }

    if (confidenceFill) {

        confidenceFill.style.width =
            "0%";
    }


    // ========================================================
    // BACKEND REQUEST
    // ========================================================

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/api/analyze-message",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        // ====================================================
        // READ RESPONSE
        // ====================================================

        let data;

        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "Backend returned an invalid response."
            );
        }


        // ====================================================
        // BACKEND ERROR
        // ====================================================

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Backend returned an error."
            );
        }


        console.log(
            "SentinelAI Message API Response:",
            data
        );


        // ====================================================
        // GET BACKEND VALUES
        // ====================================================

        const rawPrediction =
    String(
        data.prediction || ""
    ).toLowerCase().trim();

const prediction = rawPrediction;

const risk =
    Number(
        data.risk_score ?? 0
    );

const conf =
    Number(
        data.confidence ?? 0
    );


        // ====================================================
        // NORMALIZE VALUES
        // ====================================================

        const riskValue =
            Math.max(
                0,
                Math.min(
                    100,
                    risk
                )
            );

        const confidenceValue =
            Math.max(
                0,
                Math.min(
                    100,
                    conf
                )
            );


        // ====================================================
        // DISPLAY CONFIDENCE
        // ====================================================

        if (confidence) {

            confidence.textContent =
                confidenceValue.toFixed(2) + "%";
        }

        if (confidenceFill) {

            confidenceFill.style.width =
                confidenceValue + "%";
        }


        // ====================================================
        // DISPLAY ANALYZED MESSAGE
        // ====================================================

        
        if (analyzedMessage) {
            analyzedMessage.textContent = data.message || message;
        }

        const transTitle = document.getElementById("translationTitle");
        const transInfo = document.getElementById("translationInfo");
        
        if (transTitle && transInfo && data.detected_language) {
            transTitle.style.display = "block";
            transInfo.style.display = "block";
            
            let infoHtml = `<strong>Detected Language:</strong> ${data.detected_language ? data.detected_language.toUpperCase() : 'UNKNOWN'}<br>`;
            infoHtml += `<strong>Translation Attempted:</strong> ${data.translation_attempted ? 'Yes' : 'No'}<br>`;
            infoHtml += `<strong>Translation Success:</strong> ${data.translation_success ? 'Yes' : 'No'}<br>`;
            
            if (data.translation_success && data.translated_message) {
                infoHtml += `<br><strong>Translated Text:</strong><br><em>${data.translated_message}</em>`;
            }
            
            infoHtml += `<br><strong>Analysis Source:</strong> ${data.analysis_source === 'translated_text' ? 'Translated Text' : 'Original Text'}`;
            
            transInfo.innerHTML = infoHtml;
        } else if (transTitle && transInfo) {
            transTitle.style.display = "none";
            transInfo.style.display = "none";
        }



                if (document.getElementById("messageRiskComp") && data.components) {
            document.getElementById("messageRiskComp").textContent = (data.components.message_risk?.risk_score || 0).toFixed(2) + "%";
            document.getElementById("messageSemanticRiskComp").textContent = (data.components.semantic_risk?.risk_score || 0).toFixed(2) + "%";
            document.getElementById("messagePatternRiskComp").textContent = (data.components.pattern_risk?.risk_score || 0).toFixed(2) + "%";
        }
        if (document.getElementById("messageExplanation")) {
            document.getElementById("messageExplanation").textContent = data.explainable_ai?.summary || "No explanation provided.";
        }

        // ====================================================
        // CLEAR OLD REASONS
        // ====================================================

        if (reasons) {

            reasons.innerHTML = "";
        }


        // ====================================================
        // SCAM DETECTED
        // ====================================================

        if (prediction === "scam") {


            if (resultBox) {
    resultBox.classList.add("scam-result");
}
            

            if (resultTitle) {

                resultTitle.textContent =
                    "⚠ SCAM DETECTED";
            }

            if (riskBadge) {

                riskBadge.textContent =
                    "HIGH RISK";
            }


                        // -----------------------------------------------
            // DYNAMIC XAI REASONS
            // -----------------------------------------------

            const xai = data.explainable_ai || {};
            const riskFactors = Array.isArray(xai.risk_factors) ? xai.risk_factors : [];

            if (reasons) {
                const addReason = (text) => {
                    const reasonDiv = document.createElement("div");
                    reasonDiv.className = "reason-item";
                    reasonDiv.innerHTML = `<span>⚠</span> ${text}`;
                    reasons.appendChild(reasonDiv);
                };

                if (xai.summary) {
                    addReason(xai.summary);
                }

                if (xai.verdict_explanation) {
                    addReason(xai.verdict_explanation);
                }

                riskFactors.forEach((factor) => {
                    addReason(factor);
                });

                if (!xai.summary && !xai.verdict_explanation && riskFactors.length === 0) {
                    addReason("SentinelAI detected suspicious indicators.");
                }
            }

        }


        // ====================================================
        // SUSPICIOUS MESSAGE
        // ====================================================

        else if (prediction === "suspicious") {

            if (resultBox) {
                resultBox.classList.add("suspicious-result");
            }

            if (resultTitle) {
                resultTitle.textContent = "⚠️ REVIEW / SUSPICIOUS";
                resultTitle.style.color = "#ffaa00";
            }

            if (riskBadge) {
                riskBadge.textContent = "MEDIUM RISK";
                riskBadge.style.color = "#ffaa00";
                riskBadge.style.borderColor = "#ffaa00";
            }

            const xai = data.explainable_ai || {};
            const riskFactors = Array.isArray(xai.risk_factors) ? xai.risk_factors : [];

            if (reasons) {
                const addReason = (text) => {
                    const reasonDiv = document.createElement("div");
                    reasonDiv.className = "reason-item";
                    reasonDiv.innerHTML = `<span>⚠️</span> ${text}`;
                    reasons.appendChild(reasonDiv);
                };

                if (xai.summary) { addReason(xai.summary); }
                if (xai.verdict_explanation) { addReason(xai.verdict_explanation); }
                riskFactors.forEach((f) => addReason(f));

                if (!xai.summary && !xai.verdict_explanation && riskFactors.length === 0) {
                    addReason("The message content appears legitimate, but the embedded URL has insufficient evidence to establish that it is safe.");
                }
            }
        }

        // ====================================================
        // SAFE MESSAGE
        // ====================================================

        else if (prediction === "safe" || prediction === "legitimate" || prediction === "local") {

            if (resultTitle) {

                resultTitle.textContent =
                    "✓ MESSAGE SAFE";
            }

            if (riskBadge) {

                riskBadge.textContent =
                    "LOW RISK";
            }


                        // -----------------------------------------------
            // DYNAMIC SAFE REASONS
            // -----------------------------------------------

            const xai = data.explainable_ai || {};
            const positiveSignals = Array.isArray(xai.positive_signals) ? xai.positive_signals : [];

            if (reasons) {
                const addReason = (text) => {
                    const reasonDiv = document.createElement("div");
                    reasonDiv.className = "reason-item";
                    reasonDiv.innerHTML = `<span>✅</span> ${text}`;
                    reasons.appendChild(reasonDiv);
                };

                if (xai.summary) {
                    addReason(xai.summary);
                }

                if (xai.verdict_explanation) {
                    addReason(xai.verdict_explanation);
                }

                positiveSignals.forEach((signal) => {
                    addReason(signal);
                });

                if (!xai.summary && !xai.verdict_explanation && positiveSignals.length === 0) {
                    addReason("No significant scam indicators were detected.");
                }
            }

        }


        // ====================================================
        // UNKNOWN RESPONSE
        // ====================================================

        else {

            throw new Error(
                "Unexpected message prediction: " +
                prediction
            );
        }


        // ====================================================
        // SUCCESS LOG
        // ====================================================

        console.log(
            "Message prediction:",
            prediction
        );

        console.log(
            "Risk score:",
            riskValue
        );

        console.log(
            "Confidence:",
            confidenceValue
        );

    }


    // ========================================================
    // ERROR
    // ========================================================

    catch (error) {

        console.error(
            "Message analysis error:",
            error
        );


        if (resultTitle) {

            resultTitle.textContent =
                "ANALYSIS ERROR";
        }

        if (riskBadge) {

            riskBadge.textContent =
                "SERVER ERROR";
        }

        if (confidence) {

            confidence.textContent =
                "0%";
        }

        if (confidenceFill) {

            confidenceFill.style.width =
                "0%";
        }


        if (reasons) {

            reasons.innerHTML = `
                <div class="reason-item">
                    <span>•</span>
                    ${
                        error.message.includes(
                            "Failed to fetch"
                        )
                        ? "Unable to connect to SentinelAI backend. Make sure FastAPI is running on port 8000."
                        : error.message
                    }
                </div>
            `;
        }
    }


    // ========================================================
    // RESTORE BUTTON
    // ========================================================

    finally {

        if (analyzeBtn) {

            analyzeBtn.disabled =
                false;

            analyzeBtn.innerHTML = `
                <span>⚡</span>
                Analyze Message
            `;
        }
    }
}


// ============================================================
// MESSAGE ANALYZER BUTTON
// ============================================================

const analyzeMessageBtn =
    document.getElementById(
        "analyzeMessageBtn"
    );

if (analyzeMessageBtn) {

    analyzeMessageBtn.addEventListener(
        "click",
        analyzeMessage
    );
}


// ============================================================
// MESSAGE ENTER KEY
// ============================================================

const messageInput =
    document.getElementById(
        "messageInput"
    );

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        (event) => {

            // Ctrl + Enter to analyze
            if (
                event.key === "Enter" &&
                event.ctrlKey
            ) {

                event.preventDefault();

                analyzeMessage();
            }
        }
    );
}


// ============================================================
// MESSAGE CHARACTER COUNTER
// ============================================================

const messageCharCount =
    document.getElementById(
        "messageCharCount"
    );

if (
    messageInput &&
    messageCharCount
) {

    messageInput.addEventListener(
        "input",
        () => {

            messageCharCount.textContent =
                `${messageInput.value.length} / 5000`;
        }
    );
}
/* ============================================================
   SENTINELAI — EMAIL ANALYZER
============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    const emailSender = document.getElementById("emailSender");
    const emailSubject = document.getElementById("emailSubject");
    const emailBody = document.getElementById("emailBody");

    const analyzeEmailBtn = document.getElementById("analyzeEmailBtn");

    const emailAnalysisResult =
        document.getElementById("emailAnalysisResult");

    const emailResultTitle =
        document.getElementById("emailResultTitle");

    const emailRiskBadge =
        document.getElementById("emailRiskBadge");

    const emailConfidence =
        document.getElementById("emailConfidence");

    const emailConfidenceFill =
        document.getElementById("emailConfidenceFill");

    const emailReasons =
        document.getElementById("emailReasons");

    const emailSenderResult =
        document.getElementById("emailSenderResult");

    const emailDomainResult =
        document.getElementById("emailDomainResult");

    const emailUrls =
        document.getElementById("emailUrls");

    const analyzedEmailText =
        document.getElementById("analyzedEmailText");

    const emailCharCount =
        document.getElementById("emailCharCount");

    const emailMessageRisk =
        document.getElementById("emailMessageRisk");

    const emailSemanticRisk =
        document.getElementById("emailSemanticRisk");

    const emailPatternRisk =
        document.getElementById("emailPatternRisk");

    const emailUrlRisk =
        document.getElementById("emailUrlRisk");

    const emailSenderRisk =
        document.getElementById("emailSenderRisk");


    /* ---------------------------------------------------------
       CHARACTER COUNTER
    --------------------------------------------------------- */

    if (emailBody && emailCharCount) {

        emailBody.addEventListener("input", () => {

            emailCharCount.textContent =
                `${emailBody.value.length} / 10000`;

        });

    }


    /* ---------------------------------------------------------
       ANALYZE EMAIL
    --------------------------------------------------------- */

    if (analyzeEmailBtn) {

        analyzeEmailBtn.addEventListener("click", async () => {

            const sender = emailSender.value.trim();
            const subject = emailSubject.value.trim();
            const body = emailBody.value.trim();


            /* Validation */

            if (!sender) {
                alert("Please enter the sender email address.");
                emailSender.focus();
                return;
            }

            if (!subject) {
                alert("Please enter the email subject.");
                emailSubject.focus();
                return;
            }

            if (!body) {
                alert("Please paste the email content.");
                emailBody.focus();
                return;
            }


            /* Loading state */

            analyzeEmailBtn.disabled = true;

            analyzeEmailBtn.innerHTML =
                `<span>⏳</span> Analyzing Email...`;

            emailAnalysisResult.classList.remove("show");


            try {

                const response = await fetch(
                    "http://127.0.0.1:8000/api/analyze-email",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            sender: sender,
                            subject: subject,
                            body: body
                        })
                    }
                );


                if (!response.ok) {

                    const errorText =
                        await response.text();

                    throw new Error(
                        `Server error ${response.status}: ${errorText}`
                    );

                }


                const data = await response.json();


                console.log(
                    "Email Analysis Result:",
                    data
                );


                /* ------------------------------------------------
                   NORMALIZE PREDICTION
                ------------------------------------------------ */

                let prediction =
                    String(data.prediction || "")
                        .toLowerCase()
                        .trim();

                


                const risk =
                    Number(data.risk_score || 0);

                const confidence =
                    Number(data.confidence || 0);


                /* ------------------------------------------------
                   RESULT TITLE
                ------------------------------------------------ */

                if (prediction === "scam") {

    emailResultTitle.textContent = "SCAM";
    emailRiskBadge.textContent = "HIGH RISK";

    // SCAM = RED
    emailResultTitle.style.color = "#ff3333";
    emailRiskBadge.style.color = "#ff3333";
    emailRiskBadge.style.borderColor = "#ff3333";

}

else if (prediction === "scam") {

    emailResultTitle.textContent = "PHISHING";
    emailRiskBadge.textContent = "HIGH RISK";

    // PHISHING = RED
    emailResultTitle.style.color = "#ff3333";
    emailRiskBadge.style.color = "#ff3333";
    emailRiskBadge.style.borderColor = "#ff3333";

}

else if (prediction === "suspicious") {

    emailResultTitle.textContent = "SUSPICIOUS";
    emailRiskBadge.textContent = "MEDIUM RISK";

    // SUSPICIOUS = ORANGE
    emailResultTitle.style.color = "#ffaa00";
    emailRiskBadge.style.color = "#ffaa00";
    emailRiskBadge.style.borderColor = "#ffaa00";

}

else {

    emailResultTitle.textContent = "SAFE";
    emailRiskBadge.textContent = "LOW RISK";

    // SAFE = GREEN
    emailResultTitle.style.color = "#00ff66";
    emailRiskBadge.style.color = "#00ff66";
    emailRiskBadge.style.borderColor = "#00ff66";

}


                /* ------------------------------------------------
                   CONFIDENCE
                ------------------------------------------------ */

                const safeConfidence =
                    Math.max(
                        0,
                        Math.min(100, confidence)
                    );

                emailConfidence.textContent =
                    `${safeConfidence.toFixed(2)}%`;

                emailConfidenceFill.style.width =
                    `${safeConfidence}%`;

                emailConfidenceFill.style.width = `${confidence}%`;

if (prediction === "safe" || prediction === "legitimate" || prediction === "local") {
    emailConfidenceFill.style.background = "#00ff66"; // GREEN
} else {
    emailConfidenceFill.style.background = "#ff3333"; // RED
}


                /* ------------------------------------------------
                   SENDER
                ------------------------------------------------ */

                emailSenderResult.textContent =
                    `Sender: ${data.sender || sender}`;

                emailDomainResult.textContent =
                    `Domain: ${data.sender_domain || "Unknown"}`;


                /* ------------------------------------------------
                   DETECTION REASONS
                ------------------------------------------------ */

                emailReasons.innerHTML = "";

                const reasons =
                    Array.isArray(data.reasons)
                        ? data.reasons
                        : [];


                if (reasons.length === 0) {

                    emailReasons.innerHTML = `
                        <div class="reason-item">
                            <span>•</span>
                            No suspicious indicators detected.
                        </div>
                    `;

                }

                else {

                    reasons.forEach(reason => {

                        const item =
                            document.createElement("div");

                        item.className =
                            "reason-item";

                        item.innerHTML = `
                            <span>•</span>
                            ${escapeEmailHTML(reason)}
                        `;

                        emailReasons.appendChild(item);

                    });

                }


                /* ------------------------------------------------
                   DETECTED URLS
                ------------------------------------------------ */

                emailUrls.innerHTML = "";

                const detectedUrls =
                    Array.isArray(data.detected_urls)
                        ? data.detected_urls
                        : [];


                if (detectedUrls.length === 0) {

                    emailUrls.innerHTML = `
                        <div class="reason-item">
                            <span>•</span>
                            No URLs detected.
                        </div>
                    `;

                }

                else {

                    detectedUrls.forEach(url => {

                        const item =
                            document.createElement("div");

                        item.className =
                            "reason-item";

                        const urlResult =
                            (data.url_results || [])
                                .find(
                                    result =>
                                        result.url === url
                                );


                        let urlStatus =
                            "Detected";

                        if (urlResult) {

                            urlStatus =
                                `${urlResult.prediction.toUpperCase()} — ${Number(
                                    urlResult.risk_score || 0
                                ).toFixed(2)}% risk`;

                        }


                        item.innerHTML = `
                            <span>🔗</span>
                            <span>
                                ${escapeEmailHTML(url)}
                                <small style="display:block; opacity:.7;">
                                    ${escapeEmailHTML(urlStatus)}
                                </small>
                            </span>
                        `;

                        emailUrls.appendChild(item);

                    });

                }


                /* ------------------------------------------------
                   AI COMPONENTS
                ------------------------------------------------ */

                const components =
                    data.components || {};


                emailMessageRisk.textContent =
                    `${Number(
                        components.message_risk?.risk_score || 0
                    ).toFixed(2)}%`;


                emailSemanticRisk.textContent =
                    `${Number(
                        components.semantic_risk?.risk_score || 0
                    ).toFixed(2)}%`;


                emailPatternRisk.textContent =
                    `${Number(
                        components.pattern_risk?.risk_score || 0
                    ).toFixed(2)}%`;


                emailUrlRisk.textContent =
                    `${Number(
                        components.url_risk?.risk_score || 0
                    ).toFixed(2)}%`;


                emailSenderRisk.textContent =
                    `${Number(
                        components.sender_risk?.risk_score || 0
                    ).toFixed(2)}%`;


                /* ------------------------------------------------
                   ANALYZED EMAIL
                ------------------------------------------------ */

                analyzedEmailText.innerHTML = `
                    <strong>From:</strong>
                    ${escapeEmailHTML(sender)}
                    <br><br>

                    <strong>Subject:</strong>
                    ${escapeEmailHTML(subject)}
                    <br><br>

                    <strong>Body:</strong><br>
                    ${escapeEmailHTML(body).replace(/\n/g, "<br>")}
                `;


                /* ------------------------------------------------
                   SHOW RESULT
                ------------------------------------------------ */

                emailAnalysisResult.classList.add("show");


                /* Smooth scroll */

                setTimeout(() => {

                    emailAnalysisResult.scrollIntoView({
                        behavior: "smooth",
                        block: "nearest"
                    });

                }, 100);


            }

            catch (error) {

                console.error(
                    "Email analysis failed:",
                    error
                );

                alert(
                    "Unable to analyze the email. Make sure the SentinelAI backend is running."
                );

            }

            finally {

                analyzeEmailBtn.disabled = false;

                analyzeEmailBtn.innerHTML =
                    `<span>⚡</span> Analyze Email`;

            }

        });

    }


    /* ---------------------------------------------------------
       HTML ESCAPE
       Prevents email content from being interpreted as HTML.
    --------------------------------------------------------- */

    function escapeEmailHTML(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }

});
// ============================================================
// SENTINELAI — SCREENSHOT ANALYZER
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const screenshotInput =
        document.getElementById("screenshotInput");

    const analyzeScreenshotBtn =
        document.getElementById("analyzeScreenshotBtn");

    const screenshotAnalysisResult =
        document.getElementById("screenshotAnalysisResult");

    const screenshotResultTitle =
        document.getElementById("screenshotResultTitle");

    const screenshotRiskBadge =
        document.getElementById("screenshotRiskBadge");

    const screenshotConfidence =
        document.getElementById("screenshotConfidence");

    const screenshotConfidenceFill =
        document.getElementById("screenshotConfidenceFill");

    const screenshotReasons =
        document.getElementById("screenshotReasons");

    const screenshotExtractedText =
        document.getElementById("screenshotExtractedText");

    const screenshotUrls =
        document.getElementById("screenshotUrls");

    const screenshotOCRConfidence =
        document.getElementById("screenshotOCRConfidence");


    // ========================================================
    // ANALYZE SCREENSHOT (handled below in dedicated section)
    // ========================================================


    // ============================================================
    // IMAGE PREVIEW
    // ============================================================

    if (screenshotInput) {

        screenshotInput.addEventListener(
            "change",
            () => {

                const file =
                    screenshotInput.files &&
                    screenshotInput.files[0];


                if (!file) {
                    return;
                }


                console.log(
                    "Screenshot selected:",
                    file.name
                );
            }
        );
    }


    // ============================================================
    // HTML ESCAPE
    // ============================================================

    function escapeScreenshotHTML(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

});
/* ============================================================
   SCREENSHOT ANALYZER — FILE SELECTION
============================================================ */

/* ============================================================
   SENTINELAI — SCREENSHOT ANALYZER
============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    const screenshotInput =
        document.getElementById("screenshotInput");

    const chooseScreenshotBtn =
        document.getElementById("chooseScreenshotBtn");

    const screenshotUploadArea =
        document.getElementById("screenshotUploadArea");

    const screenshotFileName =
        document.getElementById("screenshotFileName");

    const screenshotPreviewContainer =
        document.getElementById("screenshotPreviewContainer");

    const screenshotPreview =
        document.getElementById("screenshotPreview");

    const screenshotStatus =
        document.getElementById("screenshotStatus");

    const analyzeScreenshotBtn =
        document.getElementById("analyzeScreenshotBtn");

    const screenshotAnalysisResult =
        document.getElementById("screenshotAnalysisResult");

    const screenshotResultTitle =
        document.getElementById("screenshotResultTitle");

    const screenshotRiskBadge =
        document.getElementById("screenshotRiskBadge");

    const screenshotConfidence =
        document.getElementById("screenshotConfidence");

    const screenshotConfidenceFill =
        document.getElementById("screenshotConfidenceFill");

    const screenshotOcrConfidence =
        document.getElementById("screenshotOcrConfidence");

    const screenshotUrls =
        document.getElementById("screenshotUrls");

    const screenshotReasons =
        document.getElementById("screenshotReasons");

    const screenshotMessageRisk =
        document.getElementById("screenshotMessageRisk");

    const screenshotSemanticRisk =
        document.getElementById("screenshotSemanticRisk");

    const screenshotPatternRisk =
        document.getElementById("screenshotPatternRisk");

    const screenshotUrlRisk =
        document.getElementById("screenshotUrlRisk");

    const screenshotExtractedText =
        document.getElementById("screenshotExtractedText");

    const screenshotExplanation =
        document.getElementById("screenshotExplanation");


    /* ========================================================
       CHECK ELEMENTS
    ======================================================== */

    if (!screenshotInput ||
        !chooseScreenshotBtn ||
        !analyzeScreenshotBtn) {

        console.error(
            "Screenshot Analyzer elements missing."
        );

        return;
    }


    let selectedScreenshot = null;


    /* ========================================================
       CHOOSE SCREENSHOT
    ======================================================== */

    chooseScreenshotBtn.addEventListener(
        "click",
        (event) => {

            event.stopPropagation();

            screenshotInput.click();

        }
    );


    /* ========================================================
       UPLOAD AREA CLICK
    ======================================================== */

    screenshotUploadArea?.addEventListener(
        "click",
        (event) => {

            if (
                event.target === chooseScreenshotBtn ||
                chooseScreenshotBtn.contains(event.target)
            ) {
                return;
            }

            screenshotInput.click();

        }
    );


    /* ========================================================
       FILE SELECTED
    ======================================================== */

    screenshotInput.addEventListener(
        "change",
        () => {

            const file =
                screenshotInput.files[0];

            if (!file) {
                return;
            }


            if (!file.type.startsWith("image/")) {

                screenshotFileName.textContent =
                    "Invalid image file.";

                screenshotInput.value = "";

                return;
            }


            selectedScreenshot = file;


            screenshotFileName.textContent =
                file.name;


            /* ------------------------------------------------
               PREVIEW
            ------------------------------------------------ */

            const reader =
                new FileReader();

            reader.onload = (event) => {

                screenshotPreview.src =
                    event.target.result;

                screenshotPreviewContainer.classList.add(
                    "active"
                );

            };

            reader.readAsDataURL(file);


            screenshotStatus.textContent =
                "Screenshot selected — ready for analysis";


            analyzeScreenshotBtn.disabled = false;

        }
    );


    /* ========================================================
       DRAG & DROP
    ======================================================== */

    screenshotUploadArea?.addEventListener(
        "dragover",
        (event) => {

            event.preventDefault();

            screenshotUploadArea.classList.add(
                "dragover"
            );

        }
    );


    screenshotUploadArea?.addEventListener(
        "dragleave",
        () => {

            screenshotUploadArea.classList.remove(
                "dragover"
            );

        }
    );


    screenshotUploadArea?.addEventListener(
        "drop",
        (event) => {

            event.preventDefault();

            screenshotUploadArea.classList.remove(
                "dragover"
            );


            const file =
                event.dataTransfer.files[0];

            if (!file) {
                return;
            }


            if (!file.type.startsWith("image/")) {

                screenshotStatus.textContent =
                    "Please select an image file.";

                return;
            }


            selectedScreenshot = file;

            screenshotFileName.textContent =
                file.name;


            const reader =
                new FileReader();

            reader.onload = (event) => {

                screenshotPreview.src =
                    event.target.result;

                screenshotPreviewContainer.classList.add(
                    "active"
                );

            };

            reader.readAsDataURL(file);


            screenshotStatus.textContent =
                "Screenshot selected — ready for analysis";

        }
    );


    /* ========================================================
       ANALYZE SCREENSHOT
    ======================================================== */

    analyzeScreenshotBtn.addEventListener(
        "click",
        async () => {

            const file =
                selectedScreenshot ||
                screenshotInput.files[0];


            if (!file) {

                screenshotStatus.textContent =
                    "Please select a screenshot first.";

                return;
            }


            /* ------------------------------------------------
               LOADING STATE
            ------------------------------------------------ */

            analyzeScreenshotBtn.disabled = true;

            screenshotStatus.textContent =
                "Analyzing screenshot...";


            try {

                const formData =
                    new FormData();

                formData.append(
                    "file",
                    file
                );


                /* ------------------------------------------------
                   BACKEND REQUEST
                ------------------------------------------------ */

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/api/analyze-screenshot",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                console.log(
                    "SCREENSHOT API RESPONSE:",
                    data
                );


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Screenshot analysis failed."
                    );

                }


                /* =================================================
                   BASIC RESULT
                ================================================= */

                const prediction =
                    String(
                        data.prediction || "unknown"
                    ).toLowerCase();


                const confidence =
                    Number(
                        data.confidence ??
                        data.risk_score ??
                        0
                    );


                /* =================================================
                   SHOW RESULT
                ================================================= */

                screenshotAnalysisResult.classList.add(
                    "show"
                );


                /* =================================================
                   VERDICT
                ================================================= */

                screenshotResultTitle.textContent =
                    prediction.toUpperCase();


                /* =================================================
                   RISK BADGE
                ================================================= */

                if (prediction === "scam") {

                    screenshotRiskBadge.textContent =
                        "HIGH RISK";

                    screenshotRiskBadge.style.background =
                        "rgba(255, 51, 51, 0.15)";

                    screenshotRiskBadge.style.borderColor =
                        "#ff3333";

                    screenshotRiskBadge.style.color =
                        "#ff3333";


                } else if (prediction === "suspicious") {

                    screenshotRiskBadge.textContent =
                        "MEDIUM RISK";

                    screenshotRiskBadge.style.background =
                        "rgba(255, 102, 0, 0.15)";

                    screenshotRiskBadge.style.borderColor =
                        "#ff6600";

                    screenshotRiskBadge.style.color =
                        "#ff6600";


                } else {

                    screenshotRiskBadge.textContent =
                        "LOW RISK";

                    screenshotRiskBadge.style.background =
                        "rgba(0, 255, 102, 0.1)";

                    screenshotRiskBadge.style.borderColor =
                        "#00ff66";

                    screenshotRiskBadge.style.color =
                        "#00ff66";

                }


                /* =================================================
                   VERDICT COLOR
                ================================================= */

                if (prediction === "scam") {

                    screenshotResultTitle.style.color =
                        "#ff3333";

                } else if (prediction === "suspicious") {

                    screenshotResultTitle.style.color =
                        "#ff6600";

                } else {

                    screenshotResultTitle.style.color =
                        "#00ff66";

                }


                /* =================================================
                   CONFIDENCE
                ================================================= */

                screenshotConfidence.textContent =
                    `${confidence.toFixed(2)}%`;


                screenshotConfidenceFill.style.width =
                    `${Math.min(confidence, 100)}%`;


                if (prediction === "safe" || prediction === "legitimate" || prediction === "local") {

                    screenshotConfidenceFill.style.background =
                        "#00ff66";

                } else {

                    screenshotConfidenceFill.style.background =
                        "#ff3333";

                }


                /* =================================================
                   OCR CONFIDENCE
                ================================================= */

                const ocrConfidence =
                    Number(
                        data.ocr_confidence ?? 0
                    );


                screenshotOcrConfidence.textContent =
                    `OCR Confidence: ${ocrConfidence.toFixed(2)}%`;


                /* =================================================
                   AI COMPONENTS
                ================================================= */

                const components =
                    data.components || {};


                const messageRisk =
                    Number(
                        components.message_risk?.risk_score ?? 0
                    );


                const semanticRisk =
                    Number(
                        components.semantic_risk?.risk_score ?? 0
                    );


                const patternRisk =
                    Number(
                        components.pattern_risk?.risk_score ?? 0
                    );


                const urlRisk =
                    Number(
                        components.url_risk?.risk_score ?? 0
                    );


                screenshotMessageRisk.textContent =
                    `${messageRisk.toFixed(2)}%`;


                screenshotSemanticRisk.textContent =
                    `${semanticRisk.toFixed(2)}%`;


                screenshotPatternRisk.textContent =
                    `${patternRisk.toFixed(2)}%`;


                screenshotUrlRisk.textContent =
                    `${urlRisk.toFixed(2)}%`;


                /* =================================================
                   DETECTED URLS
                ================================================= */

                const urls =
                    data.detected_urls || [];


                const recoveredUrls =
                    data.recovered_ocr_urls || [];


                const allUrls =
                    [
                        ...new Set(
                            [
                                ...urls,
                                ...recoveredUrls
                            ]
                        )
                    ];


                if (allUrls.length === 0) {

                    screenshotUrls.innerHTML = `
                        <div class="reason-item">
                            <span>•</span>
                            No URLs detected.
                        </div>
                    `;

                } else {

                    screenshotUrls.innerHTML =
                        allUrls.map(
                            (url) => `
                                <div class="reason-item">
                                    <span>🔗</span>
                                    <span>${escapeScreenshotHTML(url)}</span>
                                </div>
                            `
                        ).join("");

                }


                /* =================================================
                   DETECTION INDICATORS
                ================================================= */

                const reasons =
                    data.reasons || [];


                if (reasons.length === 0) {

                    screenshotReasons.innerHTML = `
                        <div class="reason-item">
                            <span>•</span>
                            No suspicious indicators detected.
                        </div>
                    `;

                } else {

                    screenshotReasons.innerHTML =
                        reasons.map(
                            (reason) => `
                                <div class="reason-item">
                                    <span>⚠</span>
                                    <span>${escapeScreenshotHTML(reason)}</span>
                                </div>
                            `
                        ).join("");

                }


                /* =================================================
                   EXTRACTED OCR TEXT
                ================================================= */

                screenshotExtractedText.textContent =
                    data.extracted_text ||
                    "No text could be extracted from the screenshot.";


                /* =================================================
                   EXPLAINABLE AI
                ================================================= */

                const explanation =
                    data.explainable_ai || {};


                let explanationHTML = "";


                if (explanation.summary) {

                    explanationHTML += `
                        <div class="reason-item">
                            <span>⚠</span>
                            <span>
                                ${escapeScreenshotHTML(
                                    explanation.summary
                                )}
                            </span>
                        </div>
                    `;

                }


                if (explanation.verdict_explanation) {

                    explanationHTML += `
                        <div class="reason-item">
                            <span>⚠</span>
                            <span>
                                ${escapeScreenshotHTML(
                                    explanation.verdict_explanation
                                )}
                            </span>
                        </div>
                    `;

                }


                if (
                    Array.isArray(
                        explanation.risk_factors
                    )
                ) {

                    explanation.risk_factors.forEach(
                        (factor) => {

                            explanationHTML += `
                                <div class="reason-item">
                                    <span>⚠</span>
                                    <span>
                                        ${escapeScreenshotHTML(
                                            factor
                                        )}
                                    </span>
                                </div>
                            `;

                        }
                    );

                }


                if (
                    Array.isArray(
                        explanation.positive_signals
                    )
                ) {

                    explanation.positive_signals.forEach(
                        (signal) => {

                            explanationHTML += `
                                <div class="reason-item">
                                    <span>✓</span>
                                    <span>
                                        ${escapeScreenshotHTML(
                                            signal
                                        )}
                                    </span>
                                </div>
                            `;

                        }
                    );

                }


                if (!explanationHTML) {

                    explanationHTML = `
                        <div class="reason-item">
                            <span>•</span>
                            <span>
                                No additional explanation available.
                            </span>
                        </div>
                    `;

                }


                screenshotExplanation.innerHTML =
                    explanationHTML;


                /* =================================================
                   STATUS
                ================================================= */

                screenshotStatus.textContent =
                    "Analysis completed successfully";


                /* =================================================
                   SCROLL TO RESULT
                ================================================= */

                screenshotAnalysisResult.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            } catch (error) {

                console.error(
                    "Screenshot analysis error:",
                    error
                );


                screenshotStatus.textContent =
                    "Analysis failed. Check the backend.";


                screenshotAnalysisResult.classList.add(
                    "show"
                );


                screenshotResultTitle.textContent =
                    "ERROR";


                screenshotResultTitle.style.color =
                    "#ff3333";


                screenshotRiskBadge.textContent =
                    "ANALYSIS ERROR";


                screenshotRiskBadge.style.color =
                    "#ff3333";


                screenshotConfidence.textContent =
                    "0%";


                screenshotConfidenceFill.style.width =
                    "0%";

            } finally {

                analyzeScreenshotBtn.disabled =
                    false;

            }

        }
    );


    /* ========================================================
       HTML ESCAPE HELPER
    ======================================================== */

    function escapeScreenshotHTML(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }

});