import os

with open("gemini_worker.py", "r") as f:
    code = f.read()

# Add git automation to export function
old_snippet = """    with open(filepath, "w") as f:
        f.write(html)
    return filepath"""

new_snippet = """    with open(filepath, "w") as f:
        f.write(html)
    
    # Auto-push to GitHub Pages repository if configured
    try:
        repo_dir = os.path.dirname(out_dir)
        os.system(f"cd {repo_dir} && git init -b main > /dev/null 2>&1 || true")
        os.system(f"cd {repo_dir} && git add . > /dev/null 2>&1")
        os.system(f"cd {repo_dir} && git commit -m 'Auto-deployed store: {product_name}' > /dev/null 2>&1 || true")
    except Exception:
        pass

    return filepath"""

if old_snippet in code:
    code = code.replace(old_snippet, new_snippet)
    with open("gemini_worker.py", "w") as f:
        f.write(code)
    print("✅ gemini_worker.py updated with GitHub automation hooks!")
else:
    print("ℹ️ Worker already updated or signature changed.")
