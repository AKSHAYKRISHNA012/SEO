import time
import httpx
from typing import Dict, Any, Tuple, Optional
from urllib.parse import urlparse

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 (SEOIntelligenceBot/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

async def fetch_webpage(url: str) -> Dict[str, Any]:
    # Ensure scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    start_time = time.time()
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=12.0, verify=False) as client:
        try:
            response = await client.get(url, headers=DEFAULT_HEADERS)
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            final_url = str(response.url)
            redirect_count = len(response.history)
            status_code = response.status_code
            html_content = response.text if status_code == 200 else ""
            headers_dict = dict(response.headers)
            
            # Asynchronously check robots.txt and sitemap.xml
            robots_found, sitemap_found = await check_robots_and_sitemap(client, parsed_url.scheme, domain)

            return {
                "success": True,
                "url": url,
                "final_url": final_url,
                "domain": domain,
                "status_code": status_code,
                "response_time_ms": elapsed_ms,
                "redirect_count": redirect_count,
                "headers": headers_dict,
                "html": html_content,
                "is_https": final_url.startswith("https://"),
                "robots_txt_found": robots_found,
                "sitemap_xml_found": sitemap_found,
                "error": None
            }
        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "url": url,
                "final_url": url,
                "domain": domain,
                "status_code": 0,
                "response_time_ms": elapsed_ms,
                "redirect_count": 0,
                "headers": {},
                "html": "",
                "is_https": url.startswith("https://"),
                "robots_txt_found": False,
                "sitemap_xml_found": False,
                "error": str(e)
            }

async def check_robots_and_sitemap(client: httpx.AsyncClient, scheme: str, domain: str) -> Tuple[bool, bool]:
    base_url = f"{scheme}://{domain}"
    robots_found = False
    sitemap_found = False

    try:
        r_resp = await client.get(f"{base_url}/robots.txt", headers=DEFAULT_HEADERS, timeout=4.0)
        if r_resp.status_code == 200 and "User-agent" in r_resp.text:
            robots_found = True
            if "Sitemap:" in r_resp.text:
                sitemap_found = True
    except Exception:
        pass

    if not sitemap_found:
        try:
            s_resp = await client.get(f"{base_url}/sitemap.xml", headers=DEFAULT_HEADERS, timeout=4.0)
            if s_resp.status_code == 200 and ("xml" in s_resp.headers.get("content-type", "") or "<urlset" in s_resp.text):
                sitemap_found = True
        except Exception:
            pass

    return robots_found, sitemap_found
