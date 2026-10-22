import os
import sys
import json
import urllib.request
import urllib.error

def call_gemini(product_name, supplier_cost, target_price, api_key):
    margin = round(float(target_price) - float(supplier_cost), 2)
    roi = round((margin / max(float(supplier_cost), 0.01)) * 100, 1)

    prompt = (
        f"You are an elite e-commerce conversion copywriter. Create a dropshipping launch kit for: '{product_name}'. "
        f"Supplier cost: ${supplier_cost}, Selling price: ${target_price} (Profit: ${margin}). "
        "Return ONLY valid JSON with keys: "
        "'headline' (catchy 6-word hook), "
        "'subheadline' (1 sentence benefit), "
        "'bullets' (array of 3 punchy feature bullets), "
        "'tiktok_hook' (3-second viral video opening script), "
        "'seo_tags' (comma-separated keywords)."
    )

    if api_key and len(api_key.strip()) > 10:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key.strip()}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_text)
                parsed["margin"] = margin
                parsed["roi"] = roi
                parsed["mode"] = "LIVE GEMINI API"
                return parsed
        except Exception:
            pass

    return {
        "headline": f"Upgrade Your Daily Routine With {product_name}",
        "subheadline": f"Engineered for maximum performance, durability, and instant everyday convenience.",
        "bullets": [
            f"Premium build quality designed to outlast standard alternatives",
            f"Plug-and-play setup — ready to use in under 30 seconds",
            f"Backed by our 30-Day Money-Back Performance Guarantee"
        ],
        "tiktok_hook": f"Stop scrolling! If you still haven't tried this {product_name}, you're doing it the hard way...",
        "seo_tags": f"{product_name.lower()}, trending gadgets 2026, viral tech",
        "margin": margin,
        "roi": roi,
        "mode": "LOCAL INSTANT ENGINE"
    }

def export_html_store(product_name, price, data, out_dir, stripe_link=""):
    os.makedirs(out_dir, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in product_name.lower())
    filepath = os.path.join(out_dir, f"{slug}_store.html")
    bullets_html = "".join(f"<li>✅ {b}</li>" for b in data.get("bullets", []))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name} — Official Store</title>
<style>
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,sans-serif; background:#090d16; color:#f8fafc; }}
  .hero {{ max-width:760px; margin:60px auto; padding:40px; background:#111827; border:1px solid #1e293b; border-radius:20px; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
  .badge {{ display:inline-block; background:#065f46; color:#34d399; padding:6px 14px; border-radius:999px; font-size:12px; font-weight:700; }}
  h1 {{ font-size:38px; margin:16px 0 10px; background:linear-gradient(90deg,#34d399,#38bdf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
  p.sub {{ font-size:18px; color:#94a3b8; line-height:1.6; }}
  ul {{ list-style:none; padding:0; margin:28px 0; }}
  li {{ padding:12px 0; border-bottom:1px solid #1f2937; font-size:16px; color:#e2e8f0; }}
  .price-row {{ display:flex; align-items:center; justify-content:space-between; margin-top:30px; padding-top:20px; border-top:1px solid #1e293b; }}
  .price {{ font-size:36px; font-weight:800; color:#34d399; }}
  .btn {{ background:linear-gradient(90deg,#10b981,#059669); color:white; padding:16px 34px; border-radius:12px; font-size:18px; font-weight:700; text-decoration:none; display:inline-block; }}
</style>
</head>
<body>
  <div class="hero">
    <span class="badge">🔥 TRENDING 2026 RELEASE</span>
    <h1>{data.get('headline')}</h1>
    <p class="sub">{data.get('subheadline')}</p>
    <ul>{bullets_html}</ul>
    <div class="price-row">
      <div>
        <div style="font-size:12px;color:#64748b;text-transform:uppercase;">Special Launch Price</div>
        <div class="price">${price}</div>
      </div>
      <a href="#checkout" class="btn" onclick="alert('Order Checkout Triggered for {product_name} ($' + '{price})!')">Buy Now — Fast Shipping</a>
    </div>
  </div>
</body>
</html>"""
    with open(filepath, "w") as f:
        f.write(html)
    return filepath

if __name__ == "__main__":
    prod = sys.argv[1] if len(sys.argv) > 1 else "Magnetic RGB Desk Lamp"
    cost = sys.argv[2] if len(sys.argv) > 2 else "8.50"
    price = sys.argv[3] if len(sys.argv) > 3 else "34.99"
    key = sys.argv[4] if len(sys.argv) > 4 else ""
    base = os.path.expanduser("~/gemini-cashflow/exports")
    res = call_gemini(prod, cost, price, key)
    saved_file = export_html_store(prod, price, res, base)
    res["exported_file"] = saved_file
    print(json.dumps(res))
