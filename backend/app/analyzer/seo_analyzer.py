import re
from collections import Counter
from typing import Dict, Any, List, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from app.schemas import (
    MetaDataAnalysis, HeadingAnalysis, HeadingItem, ContentAnalysis,
    KeywordFrequency, LinkAnalysis, LinkItem, ImageAnalysis, TechnicalSEOAnalysis
)

STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for",
    "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by",
    "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one",
    "all", "would", "there", "their", "what", "so", "up", "out", "if", "about",
    "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no",
    "just", "him", "know", "take", "people", "into", "year", "your", "good", "some",
    "could", "them", "see", "other", "than", "then", "now", "look", "only", "come",
    "its", "over", "think", "also", "back", "after", "use", "two", "how", "our",
    "work", "first", "well", "way", "even", "new", "want", "because", "any", "these",
    "give", "day", "most", "us", "is", "are", "was", "were", "has", "had", "been"
}

def analyze_metadata(soup: BeautifulSoup, page_url: str) -> MetaDataAnalysis:
    title_tag = soup.find('title')
    title = title_tag.string.strip() if title_tag and title_tag.string else None
    title_len = len(title) if title else 0
    
    if not title:
        title_status = "Missing"
    elif title_len < 30:
        title_status = "Too Short"
    elif title_len > 65:
        title_status = "Too Long"
    else:
        title_status = "Optimal"

    meta_desc = None
    desc_tag = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
    if desc_tag and desc_tag.get('content'):
        meta_desc = desc_tag.get('content').strip()
    
    desc_len = len(meta_desc) if meta_desc else 0
    if not meta_desc:
        desc_status = "Missing"
    elif desc_len < 70:
        desc_status = "Too Short"
    elif desc_len > 165:
        desc_status = "Too Long"
    else:
        desc_status = "Optimal"

    canonical_tag = soup.find('link', attrs={'rel': re.compile(r'^canonical$', re.I)})
    canonical_url = canonical_tag.get('href') if canonical_tag else None
    canonical_matches = True
    if canonical_url:
        canonical_matches = (canonical_url.rstrip('/') == page_url.rstrip('/'))

    robots_tag = soup.find('meta', attrs={'name': re.compile(r'^robots$', re.I)})
    robots_meta = robots_tag.get('content') if robots_tag else None
    is_indexable = True
    if robots_meta and ('noindex' in robots_meta.lower()):
        is_indexable = False

    # Open Graph & Twitter Cards
    og_data = {}
    for tag in soup.find_all('meta', property=re.compile(r'^og:', re.I)):
        prop = tag.get('property', '').lower()
        val = tag.get('content', '')
        if prop and val:
            og_data[prop] = val

    tw_data = {}
    for tag in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:', re.I)}):
        name = tag.get('name', '').lower()
        val = tag.get('content', '')
        if name and val:
            tw_data[name] = val

    html_tag = soup.find('html')
    lang = html_tag.get('lang') if html_tag else None

    meta_charset = soup.find('meta', charset=True)
    charset = meta_charset.get('charset') if meta_charset else "utf-8"

    return MetaDataAnalysis(
        title=title,
        title_length=title_len,
        title_status=title_status,
        description=meta_desc,
        description_length=desc_len,
        description_status=desc_status,
        canonical_url=canonical_url,
        canonical_matches=canonical_matches,
        robots_meta=robots_meta,
        is_indexable=is_indexable,
        open_graph=og_data,
        twitter_card=tw_data,
        lang=lang,
        charset=charset
    )

def analyze_headings(soup: BeautifulSoup) -> HeadingAnalysis:
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    h1_list = [h.get_text(strip=True) for h in soup.find_all('h1') if h.get_text(strip=True)]
    h1_count = len(h1_list)
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))

    hierarchy_issues = []
    if h1_count == 0:
        hierarchy_issues.append("Missing <h1> tag. Every page should have exactly one <h1> tag.")
    elif h1_count > 1:
        hierarchy_issues.append(f"Multiple <h1> tags detected ({h1_count}). Use a single primary <h1> per page.")

    tree = []
    prev_level = 0
    for h in headings:
        tag_name = h.name.lower()
        level = int(tag_name[1])
        text = h.get_text(strip=True)
        if not text:
            continue

        if prev_level > 0 and level > prev_level + 1:
            issue = f"Skipped heading level: <{tag_name}> appeared directly after <h{prev_level}>"
            if issue not in hierarchy_issues:
                hierarchy_issues.append(issue)

        prev_level = level
        tree.append(HeadingItem(tag=tag_name, text=text, level=level))

    return HeadingAnalysis(
        h1_count=h1_count,
        h1_list=h1_list,
        h2_count=h2_count,
        h3_count=h3_count,
        total_headings=len(headings),
        hierarchy_issues=hierarchy_issues,
        headings_tree=tree[:15]
    )

def analyze_content(soup: BeautifulSoup) -> ContentAnalysis:
    # Remove script, style, nav, footer for body text analysis
    for s in soup(['script', 'style', 'noscript', 'header', 'footer', 'nav', 'svg']):
        s.decompose()

    text = soup.get_text(separator=' ')
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{2,}\b', text)]
    word_count = len(words)

    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 20]
    paragraph_count = len(paragraphs)

    # Calculate Flesch Reading Ease
    sentences = re.split(r'[.!?]+', text)
    sentence_count = max(1, len([s for s in sentences if s.strip()]))
    syllables = sum(count_syllables(w) for w in words)
    
    if word_count > 0:
        flesch = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllables / word_count))
        flesch = max(0.0, min(100.0, flesch))
    else:
        flesch = 50.0

    if flesch >= 70:
        reading_diff = "Easy"
    elif flesch >= 50:
        reading_diff = "Medium"
    elif flesch >= 30:
        reading_diff = "Hard"
    else:
        reading_diff = "Very Hard"

    # Top keywords
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    counts = Counter(filtered_words)
    top_keywords = []
    total_filtered = max(1, len(filtered_words))
    for kw, cnt in counts.most_common(10):
        density = round((cnt / total_filtered) * 100, 2)
        top_keywords.append(KeywordFrequency(keyword=kw, count=cnt, density_percent=density))

    # Repeated text check
    p_texts = [p.lower() for p in paragraphs]
    has_repeated = len(p_texts) != len(set(p_texts)) and len(paragraphs) > 3

    # Freshness signals
    freshness = []
    time_tags = soup.find_all('time')
    if time_tags:
        freshness.append(f"Contains <time> timestamp tag ({len(time_tags)} found)")
    
    year_match = re.search(r'\b(202[4-6])\b', text)
    if year_match:
        freshness.append(f"Current year reference detected ({year_match.group(1)})")

    return ContentAnalysis(
        word_count=word_count,
        paragraph_count=paragraph_count,
        reading_ease_score=round(flesch, 1),
        reading_difficulty=reading_diff,
        top_keywords=top_keywords,
        has_repeated_text=has_repeated,
        freshness_signals=freshness,
        content_structure_score=85 if paragraph_count >= 5 else 50
    )

def count_syllables(word: str) -> int:
    word = word.lower()
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    return max(1, count)

def analyze_links(soup: BeautifulSoup, page_url: str, domain: str) -> LinkAnalysis:
    links = soup.find_all('a', href=True)
    total_links = len(links)
    
    internal_count = 0
    external_count = 0
    nofollow_count = 0
    
    sample_links = []
    anchor_counts = Counter()

    for a in links:
        href = a['href'].strip()
        text = a.get_text(strip=True)
        rel = a.get('rel', [])
        if isinstance(rel, str):
            rel = rel.split()
        
        is_nofollow = 'nofollow' in [r.lower() for r in rel]
        if is_nofollow:
            nofollow_count += 1

        parsed_href = urlparse(href)
        is_internal = False
        if not parsed_href.netloc or parsed_href.netloc == domain or domain in parsed_href.netloc:
            is_internal = True
            internal_count += 1
        else:
            external_count += 1

        if text:
            anchor_counts[text.lower()] += 1

        if len(sample_links) < 10:
            sample_links.append(LinkItem(
                href=href[:80],
                text=text[:40] if text else "[No Anchor Text]",
                is_internal=is_internal,
                is_nofollow=is_nofollow
            ))

    top_anchors = [{"anchor": k, "count": v} for k, v in anchor_counts.most_common(5)]
    
    opps = []
    if internal_count < 5:
        opps.append("Add more internal links to strengthen page authority and topic clusters.")
    if nofollow_count > total_links * 0.5 and total_links > 0:
        opps.append("High proportion of nofollow links detected; ensure internal links use dofollow.")

    return LinkAnalysis(
        total_links=total_links,
        internal_links_count=internal_count,
        external_links_count=external_count,
        nofollow_count=nofollow_count,
        sample_links=sample_links,
        top_anchor_texts=top_anchors,
        internal_linking_opportunities=opps
    )

def analyze_images(soup: BeautifulSoup) -> ImageAnalysis:
    images = soup.find_all('img')
    total_images = len(images)
    
    missing_alt = 0
    empty_alt = 0
    with_alt = 0
    sample_missing = []

    for img in images:
        src = img.get('src', '')
        alt = img.get('alt')
        
        if alt is None:
            missing_alt += 1
            if len(sample_missing) < 5 and src:
                sample_missing.append(src[:80])
        elif alt.strip() == '':
            empty_alt += 1
        else:
            with_alt += 1

    return ImageAnalysis(
        total_images=total_images,
        missing_alt_count=missing_alt,
        empty_alt_count=empty_alt,
        images_with_alt_count=with_alt,
        sample_missing_alt=sample_missing
    )

def analyze_technical(fetch_res: Dict[str, Any], soup: BeautifulSoup) -> TechnicalSEOAnalysis:
    viewport = soup.find('meta', attrs={'name': re.compile(r'^viewport$', re.I)})
    has_viewport = viewport is not None and 'width=' in viewport.get('content', '').lower()

    canonical = soup.find('link', attrs={'rel': re.compile(r'^canonical$', re.I)})
    has_canonical = canonical is not None

    headers = fetch_res.get('headers', {})
    
    return TechnicalSEOAnalysis(
        is_https=fetch_res.get('is_https', False),
        status_code=fetch_res.get('status_code', 200),
        response_time_ms=fetch_res.get('response_time_ms', 0),
        redirect_count=fetch_res.get('redirect_count', 0),
        final_url=fetch_res.get('final_url', fetch_res.get('url', '')),
        has_mobile_viewport=has_viewport,
        robots_txt_found=fetch_res.get('robots_txt_found', False),
        sitemap_xml_found=fetch_res.get('sitemap_xml_found', False),
        has_canonical=has_canonical,
        server_header=headers.get('server') or headers.get('Server'),
        cache_control=headers.get('cache-control') or headers.get('Cache-Control')
    )
