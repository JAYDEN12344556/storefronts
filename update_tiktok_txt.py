import os

with open("gemini_worker.py", "r") as f:
    code = f.read()

old_snippet = """    with open(filepath, "w") as f:
        f.write(html)
    
    # Auto-push to GitHub Pages repository if configured"""

new_snippet = """    with open(filepath, "w") as f:
        f.write(html)
        
    # Also export a dedicated TikTok Ad Script text file
    txt_filepath = os.path.join(out_dir, f"{slug}_tiktok_script.txt")
    txt_content = f\"\"\"=========================================
TIKTOK VIRAL AD CAMPAIGN: {product_name}
=========================================
[0:00 - 0:03] HOOK:
{data.get('tiktok_hook')}

[0:03 - 0:15] PROBLEM & SOLUTION:
{data.get('subheadline')}

[0:15 - 0:30] KEY FEATURES:
- {data.get('bullets', [''])[0]}
- {data.get('bullets', ['',''])[1] if len(data.get('bullets', [])) > 1 else ''}
- {data.get('bullets', ['','',''])[2] if len(data.get('bullets', [])) > 2 else ''}

[0:30 - 0:45] CALL TO ACTION:
Get yours today for just ${price}! Click the link in bio before this batch sells out.
=========================================
SEO TAGS: {data.get('seo_tags')}
\"\"\"
    with open(txt_filepath, "w") as tf:
        tf.write(txt_content)
    
    # Auto-push to GitHub Pages repository if configured"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    with open("gemini_worker.py", "w") as f:
        f.write(code)
    print("✅ gemini_worker.py updated to automatically export TikTok script text files!")
else:
    print("ℹ️ Worker already updated or signature changed.")
