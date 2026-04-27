import streamlit as st
import re
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,58,237,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 110%, rgba(34,211,238,0.07) 0%, transparent 55%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 5rem; max-width: 1280px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.8rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 1.1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0eeff;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #7070a0;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.35), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
}

/* ── Text input override ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: #f0eeff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.12) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a3a5a !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #a78bfa !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.72rem 2.2rem !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,58,237,0.5) !important;
    opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f0eeff;
    margin: 0 0 1.2rem;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(167,139,250,0.4);
    background: rgba(124,58,237,0.06);
}
.step-card.done {
    border-color: rgba(34,211,238,0.3);
    background: rgba(34,211,238,0.03);
}
.step-card.error {
    border-color: rgba(248,113,113,0.3);
    background: rgba(248,113,113,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #a78bfa; }
.step-card.done::before   { background: #22d3ee; }
.step-card.error::before  { background: #f87171; }

.step-header-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #a78bfa;
    opacity: 0.75;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: #e8e4dc;
}
.step-badge {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
}
.badge-waiting { color: #3a3a5a; }
.badge-running { color: #a78bfa; }
.badge-done    { color: #22d3ee; }
.badge-error   { color: #f87171; }

.step-desc {
    font-size: 0.8rem;
    color: #50507a;
    font-family: 'DM Sans', sans-serif;
    line-height: 1.5;
}
.step-detail {
    font-size: 0.78rem;
    color: #6060a0;
    font-family: 'DM Mono', monospace;
    line-height: 1.6;
    margin-top: 0.5rem;
    word-break: break-word;
}

/* ── URL pill ── */
.url-pill {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2a2a48;
    border-radius: 4px;
    padding: 0.15rem 0.55rem;
    font-size: 0.68rem;
    color: #38bdf8;
    margin: 0.15rem 0.25rem 0.15rem 0;
    font-family: 'DM Mono', monospace;
    word-break: break-all;
}

/* ── Results section ── */
.results-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 0.3rem;
}
.results-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #f0eeff;
    letter-spacing: -0.02em;
}
.results-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #3a3a5a;
    letter-spacing: 0.1em;
}

/* ── Report panel ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(34,211,238,0.2);
    border-top: 3px solid #22d3ee;
    border-radius: 16px;
    padding: 2.2rem 2.8rem;
    margin-top: 1.2rem;
    margin-bottom: 2rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    padding-bottom: 0.9rem;
    margin-bottom: 1.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.panel-label.cyan   { color: #22d3ee; }
.panel-label.violet { color: #a78bfa; }

.report-content {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 1.95;
    color: #cdc8c0;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Feedback panel ── */
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(167,139,250,0.2);
    border-top: 3px solid #a78bfa;
    border-radius: 16px;
    padding: 2rem 2.6rem;
    margin-bottom: 1.5rem;
}
.feedback-content {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    line-height: 1.9;
    color: #9090b8;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(34,211,238,0.35) !important;
    color: #22d3ee !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(34,211,238,0.08) !important;
    border-color: rgba(34,211,238,0.6) !important;
}

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    color: #404060 !important;
    cursor: pointer;
}

/* ── Warning ── */
div[data-testid="stAlert"] {
    background: rgba(248,113,113,0.06) !important;
    border: 1px solid rgba(248,113,113,0.25) !important;
    color: #f87171 !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.25); border-radius: 4px; }

/* ── Example chips ── */
.chip {
    display: inline-block;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    color: #7070a0;
    font-family: 'DM Sans', sans-serif;
    margin: 0.2rem 0.3rem 0.2rem 0;
}

/* ── Footer notice ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #2a2a42;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">⬡ &nbsp; Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping,
        writing, and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "step_states" not in st.session_state:
    st.session_state.step_states = {i: ("waiting", "", "") for i in range(1, 5)}
if "output" not in st.session_state:
    st.session_state.output = {}


# ── HELPER: render one step card ─────────────────────────────────────────────
def render_step_card(ph, num: int, title: str, desc: str, state: str, detail: str = ""):
    badge_map = {
        "waiting": ("WAITING",   "badge-waiting", ""),
        "running": ("● RUNNING", "badge-running", "active"),
        "done":    ("✓ DONE",    "badge-done",    "done"),
        "error":   ("✖ ERROR",   "badge-error",   "error"),
    }
    badge_txt, badge_cls, card_cls = badge_map.get(state, ("", "", ""))
    detail_html = f'<div class="step-detail">{detail}</div>' if detail else ""
    ph.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header-row">
            <span class="step-num">0{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-badge {badge_cls}">{badge_txt}</span>
        </div>
        <div class="step-desc">{desc}</div>
        {detail_html}
    </div>
    """, unsafe_allow_html=True)


# ── TWO-COLUMN LAYOUT: input left, pipeline right ────────────────────────────
col_left, col_gap, col_right = st.columns([5, 0.4, 4])

with col_left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025…",
        key="topic_input",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="margin-top:0.2rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                     color:#3a3a5a;letter-spacing:0.15em;">TRY →</span>
        <span class="chip">LLM Agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    STEP_META = [
        (1, "Search Agent",    "Discovers recent, reliable web sources"),
        (2, "Reader / Scraper","Extracts deep content from top URLs"),
        (3, "Writer",          "Drafts the full research report"),
        (4, "Critic",          "Reviews and scores report quality"),
    ]

    # Create placeholders so we can update them live during the run
    step_phs = {num: st.empty() for num, _, _ in STEP_META}
    for num, title, desc in STEP_META:
        state, detail, _ = st.session_state.step_states[num]
        render_step_card(step_phs[num], num, title, desc, state, detail)


# ── PIPELINE RUN ──────────────────────────────────────────────────────────────
def update_step(num, state, detail=""):
    _, _, title_cache = st.session_state.step_states[num]
    st.session_state.step_states[num] = (state, detail, title_cache)
    meta = {n: (t, d) for n, t, d in STEP_META}
    title, desc = meta[num]
    render_step_card(step_phs[num], num, title, desc, state, detail)


if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        # Reset
        st.session_state.output = {}
        for num, title, desc in STEP_META:
            render_step_card(step_phs[num], num, title, desc, "waiting")

        state_data = {}
        error_flag = False

        # ── Step 1: Search ────────────────────────────────────────────────────
        update_step(1, "running", "Querying the web for relevant sources…")
        try:
            from agents import build_search_agent
            from tools import web_search

            def extract_urls(t):
                return re.findall(r"https?://[^\s)>\]]+", t or "")

            agent = build_search_agent()
            result = agent.invoke({"messages": [("user",
                f"Use the web_search tool. Return top 5 recent, reliable items for '{topic}'. "
                "For each item include Title, URL, and Snippet.")]})
            state_data["search_results"] = result["messages"][-1].content
            state_data["top_urls"] = extract_urls(state_data["search_results"])

            if not state_data["top_urls"]:
                state_data["search_results"] = web_search.invoke({"query": topic})
                state_data["top_urls"] = extract_urls(state_data["search_results"])

            pills = "".join(f'<span class="url-pill">{u}</span>' for u in state_data["top_urls"][:5])
            update_step(1, "done", f"Found {len(state_data['top_urls'])} sources<br>{pills}")
        except Exception as e:
            update_step(1, "error", str(e)[:120])
            error_flag = True

        # ── Step 2: Scrape ────────────────────────────────────────────────────
        if not error_flag:
            update_step(2, "running", "Scraping top URLs for content…")
            try:
                from tools import scrape_url

                def is_valid(c):
                    if not c: return False
                    t = c.strip().lower()
                    bad = ["could not scrape","not accessible","access restrictions",
                           "access denied","forbidden","captcha","cloudflare",
                           "attention required","please enable cookies","you have been blocked"]
                    return len(t) > 200 and not any(b in t for b in bad)

                state_data["scraped_content"] = ""
                state_data["selected_url"] = ""
                for url in state_data["top_urls"][:5]:
                    scraped = scrape_url.invoke({"url": url})
                    if is_valid(scraped):
                        state_data["scraped_content"] = scraped
                        state_data["selected_url"] = url
                        break

                if not state_data["scraped_content"]:
                    snips = re.findall(r"Snippet:\s*(.+)", state_data["search_results"] or "")
                    state_data["scraped_content"] = (
                        "Direct scraping blocked. Using search snippets.\n\n"
                        + "\n\n".join(f"- {s.strip()}" for s in snips if s.strip())
                    )
                    update_step(2, "done", "All URLs blocked — using snippet fallback")
                else:
                    domain = state_data["selected_url"].split("/")[2]
                    chars  = len(state_data["scraped_content"])
                    update_step(2, "done",
                        f'Scraped <span class="url-pill">{domain}</span> · {chars:,} characters extracted')
            except Exception as e:
                update_step(2, "error", str(e)[:120])
                error_flag = True

        # ── Step 3: Writer ────────────────────────────────────────────────────
        if not error_flag:
            update_step(3, "running", "Drafting the full research report…")
            try:
                from agents import writer_chain
                combined = (
                    f"SEARCH RESULTS:\n{state_data['search_results']}\n\n"
                    f"SELECTED URL:\n{state_data.get('selected_url','')}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state_data['scraped_content']}"
                )
                state_data["report"] = writer_chain.invoke({"topic": topic, "research": combined})
                wc = len(str(state_data["report"]).split())
                update_step(3, "done", f"Report complete · {wc:,} words written")
            except Exception as e:
                update_step(3, "error", str(e)[:120])
                error_flag = True

        # ── Step 4: Critic ────────────────────────────────────────────────────
        if not error_flag:
            update_step(4, "running", "Reviewing and critiquing the report…")
            try:
                from agents import critic_chain
                state_data["feedback"] = critic_chain.invoke({"report": state_data["report"]})
                update_step(4, "done", "Critique complete — feedback ready below")
            except Exception as e:
                update_step(4, "error", str(e)[:120])

        st.session_state.output = state_data


# ── RESULTS: full-width, stacked ─────────────────────────────────────────────
out = st.session_state.output

if out.get("report"):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    safe_topic = topic.replace("<","&lt;").replace(">","&gt;") if topic else st.session_state.get("topic_input","")
    wc = len(str(out["report"]).split())
    st.markdown(f"""
    <div class="results-header">
        <span class="results-title">{safe_topic}</span>
        <span class="results-meta">{wc:,} WORDS &nbsp;·&nbsp; PIPELINE COMPLETE</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Report ────────────────────────────────────────────────────────────────
    report_text = str(out["report"])
    report_html = report_text.replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
    <div class="report-panel">
        <div class="panel-label cyan">📄 &nbsp; Research Report</div>
        <div class="report-content">{report_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download Report (.txt)",
        data=report_text,
        file_name=f"research_{safe_topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )

    # ── Critic Feedback ───────────────────────────────────────────────────────
    if out.get("feedback"):
        feedback_text = str(out["feedback"])
        feedback_html = feedback_text.replace("<","&lt;").replace(">","&gt;")
        st.markdown(f"""
        <div class="feedback-panel" style="margin-top:2rem;">
            <div class="panel-label violet">🧠 &nbsp; Critic Feedback</div>
            <div class="feedback-content">{feedback_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Raw search results (collapsed) ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Raw Search Results"):
        st.text(out.get("search_results", ""))

elif not run_btn:
    st.markdown("""
    <div class="notice">
        Enter a topic above and hit ⚡ Run Research Pipeline to begin
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind &nbsp;·&nbsp; Powered by LangChain Multi-Agent Pipeline &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)