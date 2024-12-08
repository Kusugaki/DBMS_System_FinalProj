// Function to handle form submission
function handleFormSubmission(url, data, formId) {
    // Send a request to the Flask server
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        // Optionally, reset the form after successful submission
        document.getElementById(formId).reset();
    })
    .catch(error => console.error('Error:', error));
}

// Add product button click event
document.getElementById('button-add').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission

    // FETCH FORM INPUTS
    var product_name = document.getElementById('input-product-name').value;
    var category     = document.getElementById('input-category').value;
    var price        = document.getElementById('input-price').value;
    var quantity     = document.getElementById('input-quantity').value;

    // Prepare data object
    var data = {
        product_name: product_name,
        category: category,
        price: price,
        quantity: quantity
    };

    // Call the function to handle the fetch request
    handleFormSubmission('/add-product-input-event', data, 'form-add-product');
});

// Log-in button click event
document.getElementById('button-log-in').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission

    // FETCH FORM INPUTS
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Prepare data object
    var data = {
        username: username,
        password: password
    };

    // Call the function to handle the fetch request
    handleFormSubmission('/log-in-input-event', data, 'form-log-in');
});