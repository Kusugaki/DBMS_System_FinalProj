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
    document.addEventListener('DOMContentLoaded', fetchProducts);

    // Function to handle form submission
    async function handleFormSubmission(url, data, formId) {
        try {
            // Send a request to the Flask server
            const response = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            // Check if the response is ok (status in the range 200-299)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const responseData = await response.json();
            console.log('Server response:', responseData);
            
            // Optionally, reset the form after successful submission
            document.getElementById(formId).reset();
            
            // Return the response data if needed
            return responseData;
        } catch (error) {
            console.error('Error:', error);
            throw error; // Rethrow the error to be handled by the caller
        }
    }

    // Log-in button click event
    document.getElementById('button-log-in').addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // FETCH FORM INPUTS
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Prepare data object
        const data = { username: username, password: password };
        
        // Call the function to handle the fetch request
        const reply = await handleFormSubmission('/log-in-input-event', data, 'form-log-in');
        
        if (reply.role === "admin") {
            window.location.assign('admin');
        } else {
            window.location.assign('employee');
        }
        
        // FETCH dashboard section to handle visibility 
        const section_dash = document.getElementById("user-dash");
        
        // toggle show dashboard
        if (section_dash.classList.contains("hidden")) {
            section_dash.classList.remove("hidden");
        } else {
            section_dash.classList.add("hidden");
        }
    });

    // Add product button click event
    document.getElementById('button-add').addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // FETCH FORM INPUTS
        const product_name = document.getElementById('input-product-name').value;
        const category     = document.getElementById('input-category').value;
        const price        = document.getElementById('input-price').value;
        const quantity     = document.getElementById('input-quantity').value;
        
        // Prepare data object
        var data = {
            product_name: product_name,
            category: category,
            price: price,
            quantity: quantity
        };
        
        // Call the function to handle the fetch request
        await handleFormSubmission('/add-product-input-event', data, 'form-add-product');
        
        fetchProducts();
    });


    document.getElementById('button-delete').addEventListener('click', async function(event) {
        event.preventDefault();
        const product_id = document.getElementById('input-delete').value;
        var data = { product_id: product_id };
        await handleFormSubmission('/delete-input-event', data, 'form-delete-product');
        fetchProducts();
    });


    document.getElementById('button-update').addEventListener('click', async function(event) {
        event.preventDefault();
        
        const checkbox = document.getElementById('input-update-checkbox');
        if (!checkbox.checked) {
            alert('Please confirm overwrite');
            return;
        }

        // FETCH FORM INPUTS
        const product_id   = document.getElementById('input-update').value;
        const product_name = document.getElementById('input-product-name').value;
        const category     = document.getElementById('input-category').value;
        const price        = document.getElementById('input-price').value;
        const quantity     = document.getElementById('input-quantity').value;
        
        // Prepare data object
        const data = {
            product_id: product_id,
            product_name: product_name,
            category: category,
            price: price,
            quantity: quantity
        };
        
        await handleFormSubmission('/update-input-event', data, 'form-update-product');
        // Clear form
        document.getElementById('form-add-product').reset();
        
        fetchProducts();
        
    });

    document.getElementById('button-history').addEventListener('click', function load_log() {
        console.log("HELLO WORLD");
        fetch('static\\turtles_cup.log')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('log-content').innerText = data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });

    document.getElementById("button-log-out").addEventListener('click', function(event) {
        event.preventDefault();
        handleFormSubmission('/logout', {'message':'log-out'}, 'form-add-product')
        // window.location.assign('../');
    });

});