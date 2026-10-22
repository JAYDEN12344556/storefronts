import os

with open("gemini_worker.py", "r") as f:
    code = f.read()

# Make sure export_html_store accepts a stripe link parameter and uses a real checkout button
old_sig = 'def export_html_store(product_name, price, data, out_dir):'
new_sig = 'def export_html_store(product_name, price, data, out_dir, stripe_link=""):'

old_btn_html = '      <a href="#checkout" class="btn" onclick="alert(\'Order Checkout Triggered for {product_name} ($' + '{price})!\')">Buy Now — Fast Shipping</a>'
new_btn_html = '      <a href="{stripe_link if stripe_link else \'#checkout\'}" class="btn" target="_blank">Buy Now — Secure Checkout</a>'

if old_sig in code:
    code = code.replace(old_sig, new_sig)
if old_btn_html in code:
    code = code.replace(old_btn_html, new_btn_html)

with open("gemini_worker.py", "w") as f:
    f.write(code)

print("✅ gemini_worker.py updated to support direct Stripe checkout URLs!")
