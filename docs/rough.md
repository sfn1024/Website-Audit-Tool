this was the replacement: (green)

img_tags = soup.find_all("img")

    excluded_parents = {"template", "noscript"}
    tracking_keywords = {"pixel", "tracking", "beacon"}
    
    clean_img_tags = []
    for img in img_tags:
        # 1. Skip if inside <template> or <noscript>
        if any(p.name in excluded_parents for p in img.parents):
            continue
        
        # Get dimensions and attributes for filtering
        width = img.get("width", "").strip()
        height = img.get("height", "").strip()
        src = img.get("src", "").lower()
        style = img.get("style", "").lower()
        
        # 2. Skip tracking pixels (1x1 or 0x0)
        if width in ("0", "1") or height in ("0", "1"):
            continue
            
        # 3. Skip images with tracking keywords in URL
        if any(kw in src for kw in tracking_keywords):
            continue
            
        # 4. Skip hidden images
        if "display:none" in style.replace(" ", "") or "visibility:hidden" in style.replace(" ", ""):
            continue
            
        clean_img_tags.append(img)


This was replaced: (red)

    # Create a fresh copy for image counting to match browser DOM behavior
    # Browsers do not render content inside <template> or <noscript> in the main DOM tree.
    image_soup = BeautifulSoup(html, "lxml")
    for tag in image_soup(["template", "noscript"]):
        tag.decompose()

    clean_img_tags = image_soup.find_all("img")