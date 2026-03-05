import os
import json
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

# Bathroom Vanities Product Database
BATHROOM_VANITIES = {
    "modern": [
        {
            "id": "mv001",
            "name": "Luxury Modern Wall Mount Vanity",
            "price": 899.99,
            "original_price": 1299.99,
            "image": "https://picsum.photos/seed/vanity1/400/300.jpg",
            "description": "Sleek modern design with soft-close drawers",
            "features": ["Soft-close", "Wall mount", "White marble top"],
            "sizes": ["24\"", "30\"", "36\"", "48\""],
            "category": "modern",
            "stock": 15,
            "rating": 4.8,
            "reviews": 234
        },
        {
            "id": "mv002", 
            "name": "Minimalist Floating Vanity Set",
            "price": 699.99,
            "original_price": 999.99,
            "image": "https://picsum.photos/seed/vanity2/400/300.jpg",
            "description": "Clean lines and minimalist aesthetic",
            "features": ["Floating design", "LED mirror", "Storage cabinet"],
            "sizes": ["30\"", "36\""],
            "category": "modern",
            "stock": 8,
            "rating": 4.6,
            "reviews": 156
        }
    ],
    "traditional": [
        {
            "id": "tv001",
            "name": "Classic Wood Vanity with Sink",
            "price": 749.99,
            "original_price": 1099.99,
            "image": "https://picsum.photos/seed/vanity3/400/300.jpg",
            "description": "Traditional craftsmanship meets modern functionality",
            "features": ["Solid wood", "Marble top", "Double sink"],
            "sizes": ["36\"", "48\"", "60\""],
            "category": "traditional",
            "stock": 12,
            "rating": 4.7,
            "reviews": 189
        }
    ],
    "luxury": [
        {
            "id": "lv001",
            "name": "Ultra Luxury Spa Vanity",
            "price": 2499.99,
            "original_price": 3499.99,
            "image": "https://picsum.photos/seed/vanity4/400/300.jpg",
            "description": "5-star hotel quality for your home",
            "features": ["Italian marble", "Gold fixtures", "Smart mirror", "Heated drawers"],
            "sizes": ["48\"", "60\"", "72\""],
            "category": "luxury",
            "stock": 3,
            "rating": 4.9,
            "reviews": 67
        }
    ]
}

# PayPal Configuration
PAYPAL_CONFIG = {
    "email": "phanor0811@outlook.com",
    "currency": "USD",
    "business_name": "Bathroom Vanities Global"
}

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 Bathroom Vanities Global - Luxury Bathroom Solutions</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-blue-600 text-white shadow-lg">
        <div class="container mx-auto px-4 py-4">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-bath text-2xl"></i>
                    <h1 class="text-2xl font-bold">Bathroom Vanities Global</h1>
                </div>
                <nav class="hidden md:flex space-x-6">
                    <a href="#modern" class="hover:text-blue-200">Modern</a>
                    <a href="#traditional" class="hover:text-blue-200">Traditional</a>
                    <a href="#luxury" class="hover:text-blue-200">Luxury</a>
                    <a href="#deals" class="hover:text-blue-200">Deals</a>
                </nav>
                <div class="flex items-center space-x-4">
                    <span class="text-sm">🌍 Worldwide Shipping</span>
                    <span class="text-sm">✅ PayPal Protected</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-5xl font-bold mb-4">Transform Your Bathroom Today</h2>
            <p class="text-xl mb-8">Premium Bathroom Vanities at Unbeatable Prices</p>
            <div class="flex justify-center space-x-4">
                <div class="bg-white text-blue-600 px-6 py-3 rounded-lg font-bold">
                    🎯 Up to 40% OFF
                </div>
                <div class="bg-green-500 text-white px-6 py-3 rounded-lg font-bold">
                    💰 PayPal Buyer Protection
                </div>
            </div>
        </div>
    </section>

    <!-- Products Section -->
    <section class="container mx-auto px-4 py-12">
        <div class="text-center mb-12">
            <h3 class="text-3xl font-bold mb-4">Featured Collections</h3>
            <p class="text-gray-600">Shop our premium bathroom vanities with worldwide shipping</p>
        </div>

        <div id="products" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Products will be loaded here -->
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2024 Bathroom Vanities Global. All rights reserved.</p>
            <p class="text-sm mt-2">🔒 Secure payments via PayPal | 🌍 Ships to 50+ countries</p>
        </div>
    </footer>

    <script>
        // Load products
        fetch('/api/products')
            .then(response => response.json())
            .then(products => {
                const container = document.getElementById('products');
                container.innerHTML = products.map(product => `
                    <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                        <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                        <div class="p-6">
                            <h4 class="text-xl font-bold mb-2">${product.name}</h4>
                            <p class="text-gray-600 mb-4">${product.description}</p>
                            <div class="flex justify-between items-center mb-4">
                                <div>
                                    <span class="text-2xl font-bold text-green-600">$${product.price}</span>
                                    <span class="text-sm text-gray-500 line-through ml-2">$${product.original_price}</span>
                                </div>
                                <div class="text-right">
                                    <div class="text-yellow-500">⭐ ${product.rating}</div>
                                    <div class="text-sm text-gray-500">(${product.reviews} reviews)</div>
                                </div>
                            </div>
                            <div class="mb-4">
                                ${product.features.map(feature => `<span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2 mb-2">${feature}</span>`).join('')}
                            </div>
                            <div class="flex space-x-2">
                                <button onclick="buyNow('${product.id}')" class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                                    🛒 Buy Now - PayPal
                                </button>
                                <button onclick="addToCart('${product.id}')" class="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300">
                                    ❤️
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');
            });

        function buyNow(productId) {
            // Redirect to PayPal checkout
            window.location.href = `/api/checkout/${productId}`;
        }

        function addToCart(productId) {
            alert('Product added to cart! Checkout with PayPal for secure payment.');
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/products')
def get_products():
    """Get all bathroom vanities"""
    all_products = []
    for category, products in BATHROOM_VANITIES.items():
        for product in products:
            product['category_display'] = category.title()
            all_products.append(product)
    return jsonify(all_products)

@app.route('/api/products/<category>')
def get_products_by_category(category):
    """Get products by category"""
    products = BATHROOM_VANITIES.get(category, [])
    return jsonify(products)

@app.route('/api/product/<product_id>')
def get_product(product_id):
    """Get specific product details"""
    for category, products in BATHROOM_VANITIES.items():
        for product in products:
            if product['id'] == product_id:
                return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/checkout/<product_id>')
def checkout_product(product_id):
    """Process checkout via PayPal"""
    # Find product
    product = None
    for category, products in BATHROOM_VANITIES.items():
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        if product:
            break
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Create PayPal checkout URL
    paypal_url = f"https://www.paypal.com/cgi-bin/webscr"
    params = {
        'cmd': '_xclick',
        'business': PAYPAL_CONFIG['email'],
        'item_name': product['name'],
        'item_number': product['id'],
        'amount': product['price'],
        'currency_code': PAYPAL_CONFIG['currency'],
        'return': 'https://your-app.vercel.app/success',
        'cancel_return': 'https://your-app.vercel.app/cancel',
        'notify_url': 'https://your-app.vercel.app/ipn'
    }
    
    param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    checkout_url = f"{paypal_url}?{param_string}"
    
    return jsonify({
        "product": product,
        "checkout_url": checkout_url,
        "paypal_email": PAYPAL_CONFIG['email'],
        "message": f"Redirecting to PayPal for {product['name']}"
    })

@app.route('/api/search')
def search_products():
    """Search bathroom vanities"""
    query = request.args.get('q', '').lower()
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 10000))
    
    results = []
    for category, products in BATHROOM_VANITIES.items():
        for product in products:
            if (query in product['name'].lower() or query in product['description'].lower()) and \
               min_price <= product['price'] <= max_price:
                product['category_display'] = category.title()
                results.append(product)
    
    return jsonify(results)

@app.route('/api/deals')
def get_deals():
    """Get special deals and discounts"""
    deals = []
    for category, products in BATHROOM_VANITIES.items():
        for product in products:
            discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
            if discount > 20:  # Only show items with more than 20% discount
                product['discount_percentage'] = round(discount, 1)
                product['category_display'] = category.title()
                deals.append(product)
    
    # Sort by discount percentage
    deals.sort(key=lambda x: x['discount_percentage'], reverse=True)
    return jsonify(deals)

@app.route('/api/analytics')
def get_analytics():
    """Get sales analytics (for dashboard)"""
    return jsonify({
        "total_products": sum(len(products) for products in BATHROOM_VANITIES.values()),
        "categories": list(BATHROOM_VANITIES.keys()),
        "average_price": np.mean([p['price'] for products in BATHROOM_VANITIES.values() for p in products]),
        "total_stock": sum(p['stock'] for products in BATHROOM_VANITIES.values() for p in products),
        "paypal_configured": True,
        "paypal_email": PAYPAL_CONFIG['email']
    })

# Keep existing API endpoints for Affiliate AI integration
@app.route('/api/portfolio/analytics/<user_id>')
def get_portfolio_analytics(user_id):
    return jsonify({
        'total_value': 125000,
        'total_invested': 100000,
        'total_gain_loss': 25000,
        'gain_loss_percentage': 25.0,
        'bathroom_vanity_sales': 15420,
        'monthly_vanity_revenue': 2850,
        'vanity_products_sold': 18
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🏠 Bathroom Vanities Global + Affiliate AI Backend starting on port {port}")
    print(f"💰 PayPal configured: {PAYPAL_CONFIG['email']}")
    print(f"🛍️  Total products: {sum(len(products) for products in BATHROOM_VANITIES.values())}")
    app.run(host='0.0.0.0', port=port)
