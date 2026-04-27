from agents import build_search_agent, writer_chain, critic_chain
from tools import web_search, scrape_url
import re


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\]]+", text or "")


def _get_best_url(urls: list[str]) -> str:
    return urls[0] if urls else ""


def _is_valid_scrape(content: str) -> bool:
    if not content:
        return False
    text = content.strip().lower()
    blocked_markers = [
        "could not scrape url",
        "not accessible for scraping",
        "access restrictions",
        "access denied",
        "forbidden",
        "captcha",
        "cloudflare",
        "attention required",
        "please enable cookies",
        "you have been blocked",
        "performance & security by cloudflare",
    ]
    return (len(text) > 200) and not any(marker in text for marker in blocked_markers)


def _snippets_from_search_results(search_results: str) -> str:
    snippets = re.findall(r"Snippet:\s*(.+)", search_results or "")
    if not snippets:
        return search_results or ""
    return "\n\n".join(f"- {s.strip()}" for s in snippets if s.strip())

def run_research_pipeline(topic : str) -> dict:
    
    state={}
    
    #search agent working
    print("\n"+" ="*50) 
    print("Step1-Search agent is working...")
    print("="*50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [(
            "user",
            "Use the web_search tool. Return top 5 recent, reliable items for "
            f"'{topic}'. For each item include Title, URL, and Snippet."
        )]
    })
    state["search_results"] = search_result["messages"][-1].content
    state["top_urls"] = _extract_urls(state["search_results"])

    # Fallback: if agent didn't call tool (no URLs), call tool directly.
    if not state["top_urls"]:
        state["search_results"] = web_search.invoke({"query": topic})
        state["top_urls"] = _extract_urls(state["search_results"])

    print("\n search result ",state['search_results'])
    

    #Step2- reader agent
    print("\n"+" ="*50)
    print("Step2- Reader agent is scraping top resources...")
    print("="*50)   
    
    best_url = _get_best_url(state["top_urls"])
    state["selected_url"] = best_url
    state["scraped_content"] = ""

    # Directly scrape the top URLs one by one to avoid LLM "access restriction" hallucinations.
    urls_to_try = state["top_urls"][:5]
    last_response = ""
    for url in urls_to_try:
        scraped = scrape_url.invoke({"url": url})
        last_response = scraped or ""
        if _is_valid_scrape(last_response):
            state["selected_url"] = url
            state["scraped_content"] = last_response
            break

    if not state["scraped_content"]:
        # If all URLs are blocked/paywalled, use high-signal snippets as fallback research.
        snippet_fallback = _snippets_from_search_results(state["search_results"])
        state["scraped_content"] = (
            "Direct scraping failed for top URLs (likely bot protection/paywall). "
            "Using search snippets as fallback context.\n\n"
            f"{snippet_fallback or last_response or 'No URL found to scrape.'}"
        )

    print("\nscraped content: \n", state['scraped_content'])
    
    #Step3- Writer chain
    print("\n"+" ="*50)
    print("Step3- Writer is drafting the report")
    print("="*50) 
    
    research_combined=(
        f"SEARCH RESULTS : \n {state['search_results']} \n \n"
        f"SELECTED URL : \n {state.get('selected_url', '')} \n \n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}" 
    )
    
    state["report"]=writer_chain.invoke({
        "topic":topic,
        "research": research_combined
    })
    
    print("\n Final report\n", state["report"])
    
    #critic report 
    
    print("\n"+" ="*50)
    print("Step4- Critic is reviewing the report")
    print("="*50)
    
    state["feedback"]=critic_chain.invoke({
            "report": state["report"]
        })
    print("\n critic report \n",state['feedback'])
    
    return state

if __name__== "__main__":
    topic =input("\n Enter a research topic:")
    run_research_pipeline(topic)