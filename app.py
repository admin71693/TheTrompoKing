from flask import Flask, render_template, request, jsonify
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Email configuration - Update these with your email settings
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@trompoking.com')

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

mail = Mail(app)

# Context processor to make Google Maps API key available to all templates
@app.context_processor
def inject_google_maps_api_key():
    return {'google_maps_api_key': GOOGLE_MAPS_API_KEY}

# The Trompo King Locations Data
LOCATIONS = [
    {
        'id': 1,
        'name': 'The Trompo King Restaurant',
        'address': '1700 South 5th Street, Waco, TX 76706',
        'phone': '(555) 123-4567',
        'hours': 'Mon-Sun: 11:00 AM - 11:00 PM',
        'lat': 31.5432,
        'lng': -97.1162,
        'description': 'Our flagship downtown location featuring authentic Al Pastor Tacos and homemade salsa'
    },
    {
        'id': 2,
        'name': 'The Trompo King Food Truck at Bosque',
        'address': '4716 Bosque Boulevard, Waco, TX 76710',
        'phone': '(555) 234-5678',
        'hours': 'Mon-Sun: 11:30 AM - 10:30 PM',
        'lat': 31.5354,
        'lng': -97.1872,
        'description': 'Vibrant location perfect for lunch breaks and family dinners'
    },
    {
        'id': 3,
        'name': 'The Trompo King Food Truck at ValleyMills',
        'address': '602 South ValleyMills Drive, Waco, TX 76706',
        'phone': '(555) 345-6789',
        'hours': 'Mon-Sun: 10:00 AM - 10:00 PM',
        'lat': 31.5269,
        'lng': -97.1541,
        'description': 'Our newest location with drive-through and outdoor patio seating'
    }
]

# The Trompo King Menu Data
MENU_ITEMS = {
    'tacos': [
        {'name': 'Al Pastor Tacos', 'description': 'Authentic Mexican with marinated pork', 'price': 3.99, 'image': 'tacos-al-pastor.jpg'},
        {'name': 'Carne Asada Tacos', 'description': 'Grilled beef with fresh lime', 'price': 4.49, 'image': 'tacos-carne-asada.jpg'},
        {'name': 'Fish Tacos', 'description': 'Battered fish with cabbage slaw', 'price': 4.99, 'image': 'tacos-fish.jpg'},
        {'name': 'Chicken Tacos', 'description': 'Grilled chicken with pico de gallo', 'price': 3.79, 'image': 'tacos-chicken.jpg'},
        {'name': 'Barbacoa Tacos', 'description': 'Slow-cooked beef', 'price': 4.99, 'image': 'tacos-barbacoa.jpg'},
        {'name': 'Veggie Tacos', 'description': 'Grilled vegetables and cheese', 'price': 3.49, 'image': 'tacos-veggie.jpg'},
    ],
    'wings': [
        {'name': 'Spicy Chipotle Wings', 'description': 'Crispy wings with smoky chipotle sauce', 'price': 9.99, 'image': 'wings-chipotle.jpg'},
        {'name': 'Lime Garlic Wings', 'description': 'Tangy lime and garlic glazed wings', 'price': 9.99, 'image': 'wings-lime-garlic.jpg'},
        {'name': 'Mango Habanero Wings', 'description': 'Sweet mango with fiery habanero kick', 'price': 10.99, 'image': 'wings-mango-habanero.jpg'},
    ],
    'burritos': [
        {'name': 'Al Pastor Burrito', 'description': 'Large flour tortilla with al pastor meat', 'price': 8.99, 'image': 'burrito-al-pastor.jpg'},
        {'name': 'Carne Asada Burrito', 'description': 'Grilled beef burrito with beans and rice', 'price': 9.49, 'image': 'burrito-carne-asada.jpg'},
        {'name': 'Chicken Burrito', 'description': 'Grilled chicken with fresh toppings', 'price': 8.49, 'image': 'burrito-chicken.jpg'},
        {'name': 'Veggie Burrito', 'description': 'Black beans, rice, veggies and cheese', 'price': 7.99, 'image': 'burrito-veggie.jpg'},
        {'name': 'Super Burrito', 'description': 'Meat, beans, rice, sour cream, guac', 'price': 10.99, 'image': 'burrito-super.jpg'},
    ],
    'enchiladas': [
        {'name': 'Cheese Enchiladas', 'description': 'Three enchiladas with melted cheese sauce', 'price': 9.99, 'image': 'enchilada-cheese.jpg'},
        {'name': 'Chicken Enchiladas', 'description': 'Chicken enchiladas in mole sauce', 'price': 10.49, 'image': 'enchilada-chicken.jpg'},
        {'name': 'Beef Enchiladas', 'description': 'Beef enchiladas with red sauce', 'price': 10.99, 'image': 'enchilada-beef.jpg'},
        {'name': 'Sour Cream Enchiladas', 'description': 'Chicken enchiladas in sour cream sauce', 'price': 10.49, 'image': 'enchilada-sour-cream.jpg'},
        {'name': 'Verde Enchiladas', 'description': 'Three enchiladas in green sauce', 'price': 9.99, 'image': 'enchilada-verde.jpg'},
    ],
    'quesadillas': [
        {'name': 'Cheese Quesadilla', 'description': 'Melted cheese between tortillas', 'price': 6.99, 'image': 'quesadilla-cheese.jpg'},
        {'name': 'Chicken Quesadilla', 'description': 'Chicken, cheese, peppers and onions', 'price': 8.49, 'image': 'quesadilla-chicken.jpg'},
        {'name': 'Mushroom Quesadilla', 'description': 'Sautéed mushrooms and cheese', 'price': 7.99, 'image': 'quesadilla-mushroom.jpg'},
        {'name': 'Carne Asada Quesadilla', 'description': 'Grilled beef with melted cheese', 'price': 9.49, 'image': 'quesadilla-carne-asada.jpg'},
        {'name': 'Supreme Quesadilla', 'description': 'Meat, cheese, beans, guac, sour cream', 'price': 10.99, 'image': 'quesadilla-supreme.jpg'},
    ],
    'sides': [
        {'name': 'Mexican Rice', 'description': 'Traditional rice with tomato sauce', 'price': 2.49, 'image': 'side-rice.jpg'},
        {'name': 'Refried Beans', 'description': 'Classic refried beans', 'price': 2.49, 'image': 'side-beans.jpg'},
        {'name': 'Chips & Guacamole', 'description': 'Fresh tortilla chips with guac', 'price': 5.99, 'image': 'side-guac.jpg'},
        {'name': 'Chips & Salsa', 'description': 'Crispy chips with homemade salsa', 'price': 3.99, 'image': 'side-salsa.jpg'},
        {'name': 'Elote', 'description': 'Mexican street corn with mayo and cheese', 'price': 4.49, 'image': 'side-elote.jpg'},
        {'name': 'Chiles Rellenos', 'description': 'Stuffed poblano pepper', 'price': 7.99, 'image': 'side-chiles.jpg'},
    ],
    'beverages': [
        {'name': 'Horchata', 'description': 'Sweet rice milk drink', 'price': 2.99, 'image': 'drink-horchata.jpg'},
        {'name': 'Jamaica', 'description': 'Traditional hibiscus drink', 'price': 2.99, 'image': 'drink-jamaica.jpg'},
        {'name': 'Agua Fresca', 'description': 'Refreshing fruit water', 'price': 2.49, 'image': 'drink-agua-fresca.jpg'},
        {'name': 'Soft Drinks', 'description': 'Coke, Sprite, Fanta', 'price': 1.99, 'image': 'drink-soda.jpg'},
        {'name': 'Mexican Coke', 'description': 'Authentic Mexican Coca-Cola with real sugar', 'price': 2.49, 'image': 'drink-mexican-coke.jpg'},
        {'name': 'Lemonade', 'description': 'Fresh made lemonade', 'price': 2.49, 'image': 'drink-lemonade.jpg'},
    ]
}

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', menu_items=MENU_ITEMS)

@app.route('/locations')
def locations():
    return render_template('locations.html', locations=LOCATIONS)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', 'General Inquiry')
        message = request.form.get('message')
        
        try:
            # Send email to admin
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@trompoking.com')
            admin_msg = Message(
                subject=f'New Contact Form Submission: {subject}',
                recipients=[admin_email],
                body=f'''
    New contact form submission from The Trompo King website:

Name: {name}
Email: {email}
Phone: {phone if phone else "Not provided"}
Subject: {subject}

Message:
{message}

---
This is an automated message from the contact form.
                '''
            )
            mail.send(admin_msg)
            
            # Send confirmation email to user
            user_msg = Message(
                subject='We received your message - The Trompo King',
                recipients=[email],
                body=f'''
Hi {name},

Thank you for contacting The Trompo King! We received your message and will get back to you soon.

Best regards,
The Trompo King Team
                '''
            )
            mail.send(user_msg)
            
            return jsonify({'success': True, 'message': f'Thank you {name}! We will contact you soon.'})
        except Exception as e:
            print(f'Error sending email: {str(e)}')
            return jsonify({'success': False, 'message': 'Error sending message. Please try again.'}), 500
    
    return render_template('contact.html')

@app.route('/api/locations')
def get_locations():
    """API endpoint to get all The Trompo King locations"""
    return jsonify(LOCATIONS)

@app.route('/api/locations/<int:location_id>')
def get_location(location_id):
    """API endpoint to get specific location by ID"""
    location = next((loc for loc in LOCATIONS if loc['id'] == location_id), None)
    if location:
        return jsonify(location)
    return jsonify({'error': 'Location not found'}), 404

@app.route('/api/data')
def get_data():
    data = {
        'title': 'The Trompo King - Authentic Mexican Food',
        'description': 'Enjoy authentic Mexican cuisine at The Trompo King with 3 convenient locations',
        'locations': len(LOCATIONS),
        'speciality': 'Al Pastor Tacos'
    }
    return jsonify(data)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for AI chatbot responses"""
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    # Simple keyword-based responses
    response_text = get_chatbot_response(user_message)
    
    return jsonify({'response': response_text})

def get_chatbot_response(message):
    """Generate chatbot response based on user message"""
    
    # Hours-related queries
    if any(word in message for word in ['hour', 'open', 'close', 'time', 'when']):
        locations_info = '\n'.join([f"🕐 {loc['name']}: {loc['hours']}" for loc in LOCATIONS])
        return f"Great question! Here's when we're open:\n\n{locations_info}\n\nWe'd love to see you! 🌮"
    
    # Phone-related queries
    if any(word in message for word in ['phone', 'call', 'contact', 'number', 'reach']):
        phones_info = '\n'.join([f"📞 {loc['name']}: {loc['phone']}" for loc in LOCATIONS])
        return f"Need to reach us? Here are our numbers:\n\n{phones_info}\n\nGive us a ring! 📱"
    
    # Location-related queries
    if any(word in message for word in ['location', 'address', 'where', 'visit', 'find']):
        locations_info = '\n'.join([f"📍 {loc['name']}: {loc['address']}" for loc in LOCATIONS])
        return f"We've got 3 awesome spots for you:\n\n{locations_info}\n\nCome visit us! 🎉"
    
    # Menu/Food-related queries
    if any(word in message for word in ['menu', 'food', 'eat', 'taco', 'burrito', 'enchilada', 'quesadilla', 'al pastor', 'serve', 'have']):
        return "OMG yes! 🤤 We make amazing Al Pastor Tacos, Burritos, Enchiladas, Quesadillas, and SO much more! Everything is made fresh with authentic Mexican recipes. Check out our full menu when you visit or ask us about specific items! 🌮"
    
    # Welcome/Greeting
    if any(word in message for word in ['hi', 'hello', 'hey', 'greetings', 'salud', 'hola', 'wassup', 'sup']):
        return "¡Hola amigo! 👋 Welcome to The Trompo King! 🌮 I'm pumped to help! Ask me about hours, locations, our menu, or anything else. Let's make your day delicious!"
    
    # Thanks
    if any(word in message for word in ['thanks', 'thank', 'thx', 'appreciate', 'gracias']):
        return "You're welcome! So happy to help! 😊 Got any other questions? I'm here for you!"
    
    # Default response
    return "Thanks for your message! I'm an AI assistant here to help. You can ask me about:\n• Our operating hours\n• Locations and addresses\n• Phone numbers\n• Our menu\n\nWhat would you like to know? 🌮"

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
