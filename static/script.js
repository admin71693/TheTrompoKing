// Trompo King - Main JavaScript

// Hide navbar on scroll (mobile)
let lastScrollY = window.scrollY;
let ticking = false;
window.addEventListener('scroll', function() {
    if (!ticking) {
        window.requestAnimationFrame(function() {
            const navbar = document.querySelector('.navbar');
            if (window.innerWidth <= 768) {
                if (window.scrollY > lastScrollY && window.scrollY > 60) {
                    navbar.style.transform = 'translateY(-100%)';
                } else {
                    navbar.style.transform = 'translateY(0)';
                }
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            lastScrollY = window.scrollY;
            ticking = false;
        });
        ticking = true;
    }
});

// Initialize on DOM loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌮 Trompo King website loaded!');
    
    // Smooth scrolling for anchor links
    setupSmoothScrolling();
    
    // Fetch API data for demonstration
    fetchRestaurantData();
    
    // Initialize chatbot
    initChatbot();
    
    // Close mobile menu when clicking nav links
    const navLinks = document.querySelectorAll('.nav-links li a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const hamburger = document.getElementById('hamburger-menu');
            const menu = document.getElementById('nav-links');
            hamburger.classList.remove('active');
            menu.classList.remove('active');
        });
    });
});

/**
 * Toggle chat modal open/close
 */
function toggleChatModal(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    const modal = document.getElementById('chat-modal');
    if (modal) {
        modal.classList.toggle('active');
        if (modal.classList.contains('active')) {
            document.getElementById('chat-input').focus();
        }
    }
}

/**
 * Close chat modal
 */
function closeChatModal(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    const modal = document.getElementById('chat-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Send chat message
 */
async function sendChatMessage(event) {
    console.log('=== sendChatMessage called ===');
    console.log('Event:', event);
    
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    const input = document.getElementById('chat-input');
    const messagesDiv = document.getElementById('chat-messages');
    
    console.log('Input element:', input);
    console.log('Messages div:', messagesDiv);
    
    const message = input.value.trim();
    
    console.log('Message to send:', message);
    console.log('Message length:', message.length);
    
    if (!message) {
        console.log('Message is empty, returning');
        return;
    }
    
    // Add user message
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message user';
    userMsgDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;
    messagesDiv.appendChild(userMsgDiv);
    console.log('User message added to DOM');
    
    input.value = '';
    
    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    console.log('Scrolled to bottom');
    
    try {
        console.log('About to send fetch request to /api/chatbot with message:', message);
        
        // Send to chatbot API
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        console.log('Fetch response received:', response);
        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Response data:', data);
            console.log('Bot response text:', data.response);
            
            const botMsgDiv = document.createElement('div');
            botMsgDiv.className = 'chat-message bot';
            botMsgDiv.innerHTML = `<p>${escapeHtml(data.response)}</p>`;
            messagesDiv.appendChild(botMsgDiv);
            console.log('Bot message added to DOM');
        } else {
            console.log('Response not OK, status:', response.status);
            const botMsgDiv = document.createElement('div');
            botMsgDiv.className = 'chat-message bot';
            botMsgDiv.innerHTML = `<p>Sorry, I couldn't understand that. Try asking about hours, menu, or locations!</p>`;
            messagesDiv.appendChild(botMsgDiv);
        }
    } catch (error) {
        console.error('Chat error caught:', error);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
        
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'chat-message bot';
        botMsgDiv.innerHTML = `<p>Oops! Something went wrong. Try again!</p>`;
        messagesDiv.appendChild(botMsgDiv);
    }
    
    // Scroll to bottom
    setTimeout(() => {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        console.log('Final scroll to bottom');
    }, 0);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Send a predefined message from suggestion buttons
 */
function sendPredefinedMessage(message) {
    console.log('Sending predefined message:', message);
    
    // First, open the modal
    const modal = document.getElementById('chat-modal');
    if (modal && !modal.classList.contains('active')) {
        modal.classList.add('active');
        console.log('Modal opened');
    }
    
    // Then set the message and send it
    const input = document.getElementById('chat-input');
    if (input) {
        input.value = message;
        input.focus();
        console.log('Input value set to:', input.value);
    }
    
    // Simulate sending message after a short delay with proper event
    setTimeout(() => {
        console.log('Calling sendChatMessage with message:', message);
        sendChatMessage({ preventDefault: () => {}, stopPropagation: () => {} });
    }, 100);
}

/**
 * Handle Enter key press in chat input
 */
function handleChatKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendChatMessage();
    }
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu(event) {
    event.stopPropagation();
    const hamburger = document.getElementById('hamburger-menu');
    const menu = document.getElementById('nav-links');
    hamburger.classList.toggle('active');
    menu.classList.toggle('active');
}

/**
 * Setup smooth scrolling for all anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

/**
 * Fetch restaurant data from API
 */
async function fetchRestaurantData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        console.log('Restaurant Data:', data);
        return data;
    } catch (error) {
        console.error('Error fetching restaurant data:', error);
    }
}

/**
 * Fetch all locations from API
 */
async function fetchLocations() {
    try {
        const response = await fetch('/api/locations');
        const locations = await response.json();
        console.log('All Locations:', locations);
        return locations;
    } catch (error) {
        console.error('Error fetching locations:', error);
    }
}

/**
 * Get specific location by ID
 */
async function getLocation(locationId) {
    try {
        const response = await fetch(`/api/locations/${locationId}`);
        const location = await response.json();
        console.log(`Location ${locationId}:`, location);
        return location;
    } catch (error) {
        console.error(`Error fetching location ${locationId}:`, error);
    }
}

/**
 * Initialize Google Map on the page
 */
function initMap() {
    // Check if Google Maps API is loaded
    if (typeof google === 'undefined' || !google.maps) {
        console.error('Google Maps API not loaded');
        return;
    }

    // Fetch locations and initialize map
    fetchLocations().then(locations => {
        if (!locations || locations.length === 0) {
            console.error('No locations found');
            return;
        }

        // Center on first location
        const center = {
            lat: locations[0].lat,
            lng: locations[0].lng
        };

        // Create map
        const mapElement = document.getElementById('map');
        if (!mapElement) {
            console.log('Map element not found on this page');
            return;
        }

        const map = new google.maps.Map(mapElement, {
            zoom: 12,
            center: center,
            mapTypeControl: true,
            fullscreenControl: true
        });

        // Add markers for each location
        locations.forEach((location, index) => {
            addMarker(map, location);
        });

        // Store map reference globally for other functions
        window.trompoMap = map;
    });
}

/**
 * Add a marker to the map
 */
function addMarker(map, location) {
    const marker = new google.maps.Marker({
        position: {
            lat: location.lat,
            lng: location.lng
        },
        map: map,
        title: location.name,
        icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });

    // Create info window
    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="padding: 10px; font-family: Arial, sans-serif;">
                <h3 style="margin: 0 0 8px 0; color: #c41e3a;">${location.name}</h3>
                <p style="margin: 5px 0;"><strong>📍</strong> ${location.address}</p>
                <p style="margin: 5px 0;"><strong>📞</strong> <a href="tel:${location.phone}">${location.phone}</a></p>
                <p style="margin: 5px 0;"><strong>⏰</strong> ${location.hours}</p>
                <p style="margin: 8px 0; font-size: 0.9em; color: #666;">${location.description}</p>
            </div>
        `
    });

    // Show info window on click
    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });

    // Auto-open first marker
    if (location.id === 1) {
        infoWindow.open(map, marker);
    }
}

/**
 * View a specific location on the map
 */
function viewOnMap(locationId) {
    console.log('=== viewOnMap called ===');
    console.log('locationId:', locationId, 'type:', typeof locationId);
    
    // Convert to number if string
    const id = parseInt(locationId, 10);
    console.log('Converted id:', id);
    
    if (!window.trompoMap) {
        console.warn('Map not initialized yet, attempting to initialize...');
        // Try to reinitialize the map
        setTimeout(() => {
            if (window.trompoMap) {
                console.log('Map is now initialized, retrying viewOnMap');
                viewOnMap(locationId);
            } else {
                console.error('Map could not be initialized');
                alert('Map is not available. Please refresh the page.');
            }
        }, 500);
        return;
    }

    console.log('Map is initialized, fetching location...');
    getLocation(id).then(location => {
        if (location) {
            console.log('Location found:', location);
            
            // Pan to location
            window.trompoMap.panTo({
                lat: location.lat,
                lng: location.lng
            });
            
            // Zoom to location
            window.trompoMap.setZoom(15);
            console.log('Map panned and zoomed to location');
            
            // Scroll to map container on mobile
            const mapContainer = document.querySelector('.map-container');
            if (mapContainer) {
                console.log('Scrolling to map container');
                mapContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } else {
            console.error('Location returned as null/undefined');
            alert('Location not found. Please try again.');
        }
    }).catch(error => {
        console.error('Error in viewOnMap:', error);
        alert('Error loading location. Please try again.');
    });
}

/**
 * Form validation
 */
function validateContactForm(name, email, message) {
    if (!name || name.trim() === '') {
        alert('Please enter your name');
        return false;
    }
    
    if (!email || !isValidEmail(email)) {
        alert('Please enter a valid email address');
        return false;
    }
    
    if (!message || message.trim() === '') {
        alert('Please enter a message');
        return false;
    }
    
    return true;
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Analytics - Track page views
 */
function trackPageView() {
    console.log('Page viewed:', window.location.pathname);
}

// Call analytics on page load
trackPageView();

// Initialize map when page has Google Maps API
window.addEventListener('load', function() {
    if (typeof google !== 'undefined' && google.maps) {
        initMap();
    }
    
    // Initialize chatbot
    initChatbot();
});

/* ============================================
   CHATBOT FUNCTIONALITY
   ============================================ */

/**
 * Initialize chatbot event listeners
 */
function initChatbot() {
    console.log('Initializing chatbot modal...');
    // The new modal doesn't need initialization
    // All event handlers are attached to the floating button and suggestion buttons
}

/**
 * Clear chat history
 */
function clearChat(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    console.log('Clearing chat...');
    const messagesDiv = document.getElementById('chat-messages');
    if (messagesDiv) {
        messagesDiv.innerHTML = `<div class="chat-message bot">
            <p>Hey there! 👋 Chat cleared. What can I help you with?</p>
        </div>`;
    }
}

/**
 * Deprecated: Old typing indicator functions - no longer used
 */
function showTypingIndicator() {
    console.log('showTypingIndicator deprecated');
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    console.log('hideTypingIndicator deprecated');
}

/**
 * Deprecated: Old minimize/expand functions - no longer used
 */
function minimizeChatbot(event) {
    console.log('minimizeChatbot deprecated');
}

function expandChatbot(event) {
    console.log('expandChatbot deprecated');
}

/**
 * Deprecated: Old chatbot functions - no longer used with new modal
 */
function toggleChatbot() {
    console.log('toggleChatbot deprecated - using new modal system');
}

function askQuestion(question) {
    console.log('askQuestion deprecated - use sendPredefinedMessage instead');
    sendPredefinedMessage(question);
}

async function sendChatbotMessage() {
    console.log('sendChatbotMessage deprecated - use sendChatMessage instead');
}

function addChatMessage(text, type) {
    console.log('addChatMessage deprecated');
}
