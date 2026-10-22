import os

with open("gemini_worker.py", "r") as f:
    code = f.read()

# Replace the simple alert button with a real Stripe Checkout form
old_btn = '<a href="#checkout" class="btn" onclick="alert(\'Order Checkout Triggered for {product_name} ($' + '{price})!\')">Buy Now — Fast Shipping</a>'

new_btn = '''<form action="https://your-backend-server.com/create-checkout-session" method="POST">
        <input type="hidden" name="product_name" value="{product_name}">
        <input type="hidden" name="price" value="{price}">
        <button type="submit" class="btn">Buy Now — Secure Checkout</button>
      </form>'''

if old_btn in code:
    code = code.replace(old_btn, new_btn)
    with open("gemini_worker.py", "w") as f:
        f.write(code)
    print("✅ gemini_worker.py updated with Stripe Checkout integration!")
else:
    print("ℹ️ Button snippet already updated or format adjusted.")
