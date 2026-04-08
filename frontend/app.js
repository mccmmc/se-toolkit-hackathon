const API_BASE = '/api';

// DOM Elements
const productsList = document.getElementById('productsList');
const shoppingList = document.getElementById('shoppingList');
const addProductForm = document.getElementById('addProductForm');
const productNameInput = document.getElementById('productName');
const productQuantityInput = document.getElementById('productQuantity');
const productMaxQuantityInput = document.getElementById('productMaxQuantity');
const productThresholdInput = document.getElementById('productThreshold');
const connectionStatus = document.getElementById('connectionStatus');

// WebSocket connection for real-time updates
let ws = null;
let wsReconnectTimer = null;

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        connectionStatus.textContent = '● Connected';
        connectionStatus.className = 'connection-status connected';
    };
    
    ws.onclose = () => {
        connectionStatus.textContent = '● Disconnected';
        connectionStatus.className = 'connection-status disconnected';
        // Reconnect after 3 seconds
        wsReconnectTimer = setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = () => {
        ws.close();
    };
    
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.action === 'refresh') {
                loadAndRenderProducts();
            }
        } catch (error) {
            console.error('WebSocket message error:', error);
        }
    };
}

// Fetch all products
async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        if (!response.ok) throw new Error('Failed to fetch products');
        return await response.json();
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
}

// Fetch shopping list (critical items)
async function fetchShoppingList() {
    try {
        const response = await fetch(`${API_BASE}/shopping-list`);
        if (!response.ok) throw new Error('Failed to fetch shopping list');
        return await response.json();
    } catch (error) {
        console.error('Error fetching shopping list:', error);
        return [];
    }
}

// Create a new product
async function createProduct(name, quantity, threshold, maxQuantity) {
    try {
        const response = await fetch(`${API_BASE}/products`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, quantity, threshold, max_quantity: maxQuantity }),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create product');
        }
        return await response.json();
    } catch (error) {
        console.error('Error creating product:', error);
        throw error;
    }
}

// Delete a product
async function deleteProduct(productId) {
    try {
        const response = await fetch(`${API_BASE}/products/${productId}`, {
            method: 'DELETE',
        });
        if (!response.ok) throw new Error('Failed to delete product');
    } catch (error) {
        console.error('Error deleting product:', error);
        throw error;
    }
}

// Adjust quantity (increment/decrement)
async function adjustQuantity(productId, action) {
    try {
        const response = await fetch(`${API_BASE}/products/${productId}/${action}`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to adjust quantity');
        }
        return await response.json();
    } catch (error) {
        console.error('Error adjusting quantity:', error);
        throw error;
    }
}

// Mark product as bought (reset to max quantity)
async function markAsBought(productId) {
    try {
        const response = await fetch(`${API_BASE}/products/${productId}/bought`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to mark as bought');
        }
        return await response.json();
    } catch (error) {
        console.error('Error marking as bought:', error);
        throw error;
    }
}

// Render products list
function renderProducts(products) {
    if (products.length === 0) {
        productsList.innerHTML = `
            <div class="empty-state">
                <p>No products yet. Add your first product above!</p>
            </div>
        `;
        return;
    }

    productsList.innerHTML = products
        .map((product) => {
            const isLowStock = product.quantity <= product.threshold;
            return `
                <div class="product-card ${isLowStock ? 'low-stock' : ''}" data-id="${product.id}">
                    <div class="product-info">
                        <div class="product-name">${escapeHtml(product.name)}</div>
                        <div class="product-details">
                            Quantity: <span class="quantity-label">${product.quantity}</span> / ${product.max_quantity} | 
                            Threshold: <span class="threshold">≤ ${product.threshold}</span>
                        </div>
                    </div>
                    <div class="product-actions">
                        <div class="quantity-controls">
                            <button class="btn-adjust btn-decrement" onclick="handleDecrement(${product.id})" ${product.quantity <= 0 ? 'disabled' : ''}>−</button>
                            <span class="quantity-display">${product.quantity}</span>
                            <button class="btn-adjust btn-increment" onclick="handleIncrement(${product.id})">+</button>
                        </div>
                        <button class="btn btn-success" onclick="handleBought(${product.id})" ${product.quantity >= product.max_quantity ? 'disabled' : ''}>✓ Bought</button>
                        <button class="btn btn-danger" onclick="handleDelete(${product.id})">Delete</button>
                    </div>
                </div>
            `;
        })
        .join('');
}

// Render shopping list
function renderShoppingList(items) {
    if (items.length === 0) {
        shoppingList.innerHTML = `
            <p class="empty-message">All items are well stocked!</p>
        `;
        return;
    }

    shoppingList.innerHTML = items
        .map((product) => {
            return `
                <div class="shopping-item" data-id="${product.id}">
                    <div class="shopping-item-info">
                        <div class="shopping-item-name">${escapeHtml(product.name)}</div>
                        <div class="shopping-item-details">
                            Current: ${product.quantity} / ${product.max_quantity} | Need to buy: ${product.max_quantity - product.quantity}
                        </div>
                    </div>
                    <button class="btn btn-success btn-sm" onclick="handleBought(${product.id})">✓ Bought</button>
                </div>
            `;
        })
        .join('');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event handlers
async function handleIncrement(productId) {
    try {
        await adjustQuantity(productId, 'increment');
        await loadAndRenderProducts();
    } catch (error) {
        alert('Failed to increment quantity');
    }
}

async function handleDecrement(productId) {
    try {
        await adjustQuantity(productId, 'decrement');
        await loadAndRenderProducts();
    } catch (error) {
        alert(error.message || 'Failed to decrement quantity');
    }
}

async function handleBought(productId) {
    try {
        await markAsBought(productId);
        await loadAndRenderProducts();
    } catch (error) {
        alert('Failed to mark as bought');
    }
}

async function handleDelete(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    try {
        await deleteProduct(productId);
        await loadAndRenderProducts();
    } catch (error) {
        alert('Failed to delete product');
    }
}

// Load and render products
async function loadAndRenderProducts() {
    const [products, shoppingItems] = await Promise.all([
        fetchProducts(),
        fetchShoppingList()
    ]);
    renderProducts(products);
    renderShoppingList(shoppingItems);
}

// Form submission
addProductForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = productNameInput.value.trim();
    const quantity = parseInt(productQuantityInput.value, 10);
    const maxQuantity = parseInt(productMaxQuantityInput.value, 10);
    const threshold = parseInt(productThresholdInput.value, 10);

    if (!name) {
        alert('Please enter a product name');
        return;
    }

    if (isNaN(quantity) || quantity < 0) {
        alert('Quantity must be a non-negative number');
        return;
    }

    if (isNaN(maxQuantity) || maxQuantity < 0) {
        alert('Max quantity must be a non-negative number');
        return;
    }

    if (quantity > maxQuantity) {
        alert('Starting quantity cannot exceed max quantity');
        return;
    }

    if (isNaN(threshold) || threshold < 0) {
        alert('Threshold must be a non-negative number');
        return;
    }

    try {
        await createProduct(name, quantity, threshold, maxQuantity);
        addProductForm.reset();
        productQuantityInput.value = 5;
        productMaxQuantityInput.value = 10;
        productThresholdInput.value = 1;
        await loadAndRenderProducts();
    } catch (error) {
        alert(error.message || 'Failed to add product');
    }
});

// Initialize WebSocket connection
connectWebSocket();

// Initial load
loadAndRenderProducts();
