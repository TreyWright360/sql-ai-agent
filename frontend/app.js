// Configuration
const CONFIG = {
    // Update this with your backend URL (Streamlit Cloud or FastAPI)
    API_URL: 'http://localhost:8000/api/query', // Change this to your deployed backend
    SESSION_ID: generateSessionId(),
};

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const visualizationArea = document.getElementById('visualizationArea');
const chartCanvas = document.getElementById('chartCanvas');
const dataTableContainer = document.getElementById('dataTableContainer');
const closeVizBtn = document.getElementById('closeViz');

// Chart instance
let currentChart = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Sample query buttons
    const sampleButtons = document.querySelectorAll('.sample-query-btn');
    sampleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.dataset.query;
            chatInput.value = query;
            sendMessage();
        });
    });

    // Send button
    sendBtn.addEventListener('click', sendMessage);

    // Enter key in input
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Close visualization
    closeVizBtn.addEventListener('click', () => {
        visualizationArea.style.display = 'none';
        if (currentChart) {
            currentChart.destroy();
            currentChart = null;
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

// Send Message Function
async function sendMessage() {
    const query = chatInput.value.trim();

    if (!query) return;

    // Disable input
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message to chat
    addMessage('user', query);

    // Clear input
    chatInput.value = '';

    // Show loading
    const loadingId = addLoadingMessage();

    try {
        // Call API
        const response = await queryBackend(query);

        // Remove loading
        removeMessage(loadingId);

        // Add assistant response
        addMessage('assistant', response.response);

        // Show visualization if data exists
        if (response.data && response.data.length > 0) {
            displayVisualization(response);
        }

    } catch (error) {
        console.error('Error:', error);
        removeMessage(loadingId);
        addMessage('assistant', `Sorry, I encountered an error: ${error.message}. Please try again.`);
    } finally {
        // Re-enable input
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Query Backend Function
async function queryBackend(query) {
    // For demo purposes, return mock data
    // In production, replace this with actual API call
    return getMockResponse(query);

    /* Production API Call (uncomment when backend is ready):
    const response = await fetch(CONFIG.API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            session_id: CONFIG.SESSION_ID
        })
    });

    if (!response.ok) {
        throw new Error('API request failed');
    }

    return await response.json();
    */
}

// Mock Response for Demo (Remove in production)
function getMockResponse(query) {
    const lowerQuery = query.toLowerCase();

    // Order count query
    if (lowerQuery.includes('how many orders')) {
        return {
            response: "There are 99,441 orders in the database.",
            data: [
                { metric: "Total Orders", value: 99441 }
            ],
            visualization: { type: "none" }
        };
    }

    // Monthly revenue query
    if (lowerQuery.includes('monthly revenue') || lowerQuery.includes('revenue trends')) {
        return {
            response: "Here are the monthly revenue trends for 2017. You can see steady growth throughout the year.",
            data: [
                { month: "2017-01", revenue: 120000 },
                { month: "2017-02", revenue: 135000 },
                { month: "2017-03", revenue: 158000 },
                { month: "2017-04", revenue: 142000 },
                { month: "2017-05", revenue: 168000 },
                { month: "2017-06", revenue: 185000 },
                { month: "2017-07", revenue: 195000 },
                { month: "2017-08", revenue: 210000 },
                { month: "2017-09", revenue: 225000 },
                { month: "2017-10", revenue: 238000 },
                { month: "2017-11", revenue: 265000 },
                { month: "2017-12", revenue: 290000 }
            ],
            visualization: { type: "line", title: "Monthly Revenue 2017" }
        };
    }

    // Top products query
    if (lowerQuery.includes('top') && (lowerQuery.includes('product') || lowerQuery.includes('categor'))) {
        return {
            response: "Here are the top 10 product categories by total sales value.",
            data: [
                { category: "Electronics", sales: 450000 },
                { category: "Furniture", sales: 380000 },
                { category: "Clothing", sales: 325000 },
                { category: "Books", sales: 280000 },
                { category: "Home & Garden", sales: 245000 },
                { category: "Sports", sales: 210000 },
                { category: "Toys", sales: 185000 },
                { category: "Beauty", sales: 165000 },
                { category: "Automotive", sales: 142000 },
                { category: "Food & Beverage", sales: 128000 }
            ],
            visualization: { type: "bar", title: "Top 10 Product Categories" }
        };
    }

    // Payment method query
    if (lowerQuery.includes('payment')) {
        return {
            response: "Here's the distribution of payment methods used by customers.",
            data: [
                { payment_method: "Credit Card", count: 45320, percentage: 45.6 },
                { payment_method: "Boleto", count: 28440, percentage: 28.6 },
                { payment_method: "Debit Card", count: 15680, percentage: 15.8 },
                { payment_method: "Voucher", count: 7890, percentage: 7.9 },
                { payment_method: "Not Defined", count: 2111, percentage: 2.1 }
            ],
            visualization: { type: "pie", title: "Payment Method Distribution" }
        };
    }

    // Default response
    return {
        response: "I understand you're asking about: \"" + query + "\". This is a demo with limited queries. Try one of the sample questions above for a full demonstration of the AI agent's capabilities.",
        data: null,
        visualization: { type: "none" }
    };
}

// Add Message to Chat
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = `<p>${content}</p>`;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv.id = 'msg_' + Date.now();
}

// Add Loading Message
function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    const loadingId = 'loading_' + Date.now();
    messageDiv.id = loadingId;
    messageDiv.className = 'message message-assistant';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="loading"></div>';

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return loadingId;
}

// Remove Message
function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

// Display Visualization
function displayVisualization(response) {
    visualizationArea.style.display = 'block';

    // Destroy previous chart
    if (currentChart) {
        currentChart.destroy();
    }

    const { data, visualization } = response;

    if (visualization.type === 'line' || visualization.type === 'bar') {
        createLineOrBarChart(data, visualization);
    } else if (visualization.type === 'pie') {
        createPieChart(data, visualization);
    }

    // Display data table
    displayDataTable(data);

    // Scroll to visualization
    visualizationArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Create Line or Bar Chart
function createLineOrBarChart(data, config) {
    const labels = data.map(item => Object.values(item)[0]);
    const values = data.map(item => Object.values(item)[1]);

    const ctx = chartCanvas.getContext('2d');
    currentChart = new Chart(ctx, {
        type: config.type,
        data: {
            labels: labels,
            datasets: [{
                label: config.title || 'Data',
                data: values,
                backgroundColor: config.type === 'bar'
                    ? 'rgba(31, 119, 180, 0.6)'
                    : 'transparent',
                borderColor: 'rgba(31, 119, 180, 1)',
                borderWidth: 2,
                tension: 0.4,
                fill: config.type === 'line'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: config.title || '',
                    color: '#ffffff',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#a0aec0' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#a0aec0' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Create Pie Chart
function createPieChart(data, config) {
    const labels = data.map(item => Object.values(item)[0]);
    const values = data.map(item => Object.values(item)[1]);

    const colors = [
        'rgba(31, 119, 180, 0.8)',
        'rgba(255, 127, 14, 0.8)',
        'rgba(44, 160, 44, 0.8)',
        'rgba(214, 39, 40, 0.8)',
        'rgba(148, 103, 189, 0.8)',
        'rgba(140, 86, 75, 0.8)',
        'rgba(227, 119, 194, 0.8)',
        'rgba(127, 127, 127, 0.8)'
    ];

    const ctx = chartCanvas.getContext('2d');
    currentChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: '#0a0e27',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        padding: 15
                    }
                },
                title: {
                    display: true,
                    text: config.title || '',
                    color: '#ffffff',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}

// Display Data Table
function displayDataTable(data) {
    if (!data || data.length === 0) {
        dataTableContainer.innerHTML = '';
        return;
    }

    const headers = Object.keys(data[0]);

    let tableHTML = '<table class="data-table"><thead><tr>';

    headers.forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });

    tableHTML += '</tr></thead><tbody>';

    data.forEach(row => {
        tableHTML += '<tr>';
        headers.forEach(header => {
            const value = row[header];
            const formatted = typeof value === 'number' ? formatNumber(value) : value;
            tableHTML += `<td>${formatted}</td>`;
        });
        tableHTML += '</tr>';
    });

    tableHTML += '</tbody></table>';

    dataTableContainer.innerHTML = tableHTML;
}

// Format Number
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
}

// Scroll Animation
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .tech-item, .arch-step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
