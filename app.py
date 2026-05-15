from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)
import os
from dotenv import load_dotenv 
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

my_products = """
--- 👕 CLOTHING (Fashion Store) ---
1. T-shirt Basic (Black/White/Grey) - Sizes: S to XXL - Price: 35 TND
2. Slim Fit Blue Jeans - Sizes: 28 to 40 - Price: 65 TND
3. Oversized Hoodie (Beige/Black) - Sizes: M, L, XL - Price: 85 TND
4. Summer Floral Dress - Sizes: S, M, L - Price: 75 TND
5. Classic Leather Jacket - Sizes: L, XL - Price: 180 TND
6. Cargo Pants (Khaki/Olive) - Sizes: 30 to 38 - Price: 70 TND
7. Cotton Polo Shirt (Navy/Red) - Sizes: M to 3XL - Price: 55 TND
8. Linen Summer Shirt (White) - Sizes: S to XL - Price: 60 TND

--- 👟 FOOTWEAR (Shoes & Sneakers) ---
9. White Urban Sneakers - Sizes: 36 to 45 - Price: 95 TND
10. Professional Running Shoes (Pro-Run) - Sizes: 40 to 44 - Price: 145 TND
11. Classic Leather Boots (Brown) - Sizes: 41 to 45 - Price: 160 TND
12. Casual Summer Sandals - Sizes: 37 to 42 - Price: 45 TND
13. Formal Oxford Shoes (Black) - Sizes: 39 to 46 - Price: 130 TND

--- ⌚ ACCESSORIES & JEWELRY ---
14. Minimalist Silver Watch - Price: 120 TND
15. Polarized Sunglasses (Black) - Price: 55 TND
16. Leather Wallet (Black/Brown) - Price: 40 TND
17. Sports Backpack (Waterproof) - Price: 75 TND
18. Silver Bracelet (Men/Women) - Price: 65 TND
19. Luxury Silk Scarf - Price: 45 TND

--- 📱 ELECTRONICS & GADGETS ---
20. Wireless Earbuds (Noise Cancelling) - Price: 110 TND
21. Smart Fitness Tracker (Series 5) - Price: 85 TND
22. Portable Power Bank (20,000mAh) - Price: 65 TND
23. Bluetooth Portable Speaker - Price: 90 TND

--- 🧴 PERFUMES & CARE ---
24. "Desert Night" Perfume (100ml) - Price: 140 TND
25. Organic Beard Oil Kit - Price: 35 TND
26. Luxury Scented Candle (Vanilla/Oud) - Price: 28 TND
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        
# 3. Request l-Groq
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are a professional and friendly Shopping Assistant.
                    Your job is to help customers choose from the following products only: {my_products}.
                    You must ALWAYS respond in English.
                    Keep your answers short, clear, and professional. 
                    Always try to be helpful and suggest products from the list.
                    RULES:
                    1. If a customer asks for a category (like watches or clothes), don't just list them. Describe the options and ask follow-up questions to help them choose.
                    2. Always suggest a matching item (Cross-selling). Example: If they look at a watch, suggest a wallet or a formal shirt.
                    3. If they ask for something NOT in the list, politely tell them we don't have it and suggest the closest alternative.
                    4. Keep the tone enthusiastic, professional, and helpful.
                    5. Use bold text for product names and prices to make them stand
                    """
                },
                {"role": "user", "content": user_message}
            ]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Samahni, famma mochkla sghira fel server. 3awed jarreb chwaya akher."})

if __name__ == "__main__":
    app.run(debug=True)