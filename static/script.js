document.addEventListener('DOMContentLoaded', function() {
    // Function to handle dynamic table updates
    function fetchProducts() {
        fetch('/get-products')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('dynamic-table-tbody');
                tableBody.innerHTML = ''; // Clear existing table rows

                data.forEach(product => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${product.id}</td>
                        <td>${product.product_name}</td>
                        <td>${product.category}</td>
                        <td>${product.price}</td>
                        <td>${product.quantity}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }).catch(error => console.error('Error fetching products:', error));
    }

    // Call fetchProducts() to load data when the page loads
    fetchProducts();

    // Function to check if the user is logged in
    async function checkLoginStatus() {
        const response = await fetch('/is-logged-in');
        return response.ok; // Returns true if logged in, false otherwise
    }

    // Function to handle form submission
    async function handleFormSubmission(url, data, formId) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const responseData = await response.json();
            console.log('Server response:', responseData);
    
            // Check if the form exists before resetting
            const formElement = document.getElementById(formId);    
            if (formElement) {
                formElement.reset(); // Reset the form only if it exists
            } else {
                console.error(`Form with ID ${formId} not found.`);
            }
    
            return responseData;
        } catch (error) {
            console.error('Error:', error);
            alert('Error: ' + error.message); // Show error message to user
            throw error;
        }
    }

    // Log-in button click event
    document.getElementById('button-log-in').addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent default form submission

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const data = { username: username, password: password };
        const reply = await handleFormSubmission('/log-in-input-event', data, 'form-log-in');

        if (reply.role === "admin") {
            // Additional admin logic if needed
        }

        const section = document.getElementById("user-dash");
        section.classList.remove("hidden");
    });

    // Add product button click event
    document.getElementById('button-add').addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent default form submission

        const isLoggedIn = await checkLoginStatus();
        if (!isLoggedIn) {
            alert('You must be logged in to add products.');
            return;
        }

        const product_name = document.getElementById('input-product-name').value;
        const category     = document.getElementById('input-category').value;
        const price        = document.getElementById('input-price').value;
        const quantity     = document.getElementById('input-quantity').value;

        const data = {
            product_name: product_name,
            category: category,
            price: price,
            quantity: quantity
        };

        await handleFormSubmission('/add-product-input-event', data, 'form-add-product');
        fetchProducts();
    });

    // Delete product button click event
    document.getElementById('button-delete').addEventListener('click', async function(event) {
        event.preventDefault();
        
        const isLoggedIn = await checkLoginStatus();
        if (!isLoggedIn) {
            alert('You must be logged in to delete products.');
            return;
        }

        const product_id = document.getElementById('input-delete').value;
        const data = { product_id: product_id };
        await handleFormSubmission('/delete-input-event', data, 'form-delete-product');
        document.addEventListener('DOMContentLoaded', fetchProducts());
        document.getElementById('dynamic-table-body').addEventListener('DOMContentLoaded', fetchProducts());
    });
    
    // Update product button click event
    document.getElementById('button-update').addEventListener('click', async function(event) {
        event.preventDefault();
        
        const isLoggedIn = await checkLoginStatus();
        if (!isLoggedIn) {
            alert('You must be logged in to update products.');
            return;
        }
        
        const product_id   = document.getElementById('input-update').value;
        const product_name = document.getElementById('input-product-name').value;
        const category     = document.getElementById('input-category').value;
        const price        = document.getElementById('input-price').value;
        const quantity     = document.getElementById('input-quantity').value;
      
        const data = {
            product_id: product_id,
            product_name: product_name,
            category: category,
            price: price,
            quantity: quantity
        };
        
        await handleFormSubmission('/update-input-event', data, 'form-update-product');
        document.addEventListener('DOMContentLoaded', fetchProducts());
        document.getElementById('dynamic-table-body').addEventListener('DOMContentLoaded', fetchProducts());
    });

    document.getElementById('button-history').addEventListener('click', async function() {
        try {
            const response = await fetch('/get-log');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            
            // Display the log content in the log-content div
            const logContentDiv = document.getElementById('log-content');
            if (data.log) {
                logContentDiv.innerText = data.log; // Display log content
            } else {
                logContentDiv.innerText = 'No log content available.';
            }
        } catch (error) {
            console.error('Error fetching log:', error);
            document.getElementById('log-content').innerText = 'Error fetching log: ' + error.message;
        }
    });

    document.getElementById("button-log-out").addEventListener('click', async function(event) {
        event.preventDefault();
        const response = await fetch('/logout', { method: 'POST' });
        if (response.ok) {
            alert('Logged out successfully.');
            location.reload();
        } else {
            alert('Error logging out.');
        }
    });

    async function submitCreateAccountForm(event) {
        event.preventDefault(); // Prevent the default form submission

        const username = document.getElementById('create-username').value;
        const password = document.getElementById('create-password').value;
        const role     = document.getElementById('role').value;

        const response = await fetch('/create-account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, 
                                   password: password, 
                                   role: role }),
        });

        const result = await response.json();
        alert(result.message); // Show the response message

        if (response.ok) {
            document.getElementById('create-account-form').classList.add('hidden');; // Hide the form on success
        }
    }

    // Attach the submit function to the form
    document.getElementById('create-account-form').addEventListener('submit', submitCreateAccountForm);

    document.getElementById('create-account').addEventListener('click', function showCreateAccountForm() {
        document.getElementById('create-account-form').classList.remove('hidden');
    });

});