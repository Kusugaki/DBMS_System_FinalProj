document.getElementById('button-add').addEventListener('click', function() {
    // FETCH FORM INPUTS
    var product_name = document.getElementById('input-product-name').value;
    var category     = document.getElementById('input-category').value;
    var price        = document.getElementById('input-price').value;
    var quantity     = document.getElementById('input-quantity').value;

    // CLEAR FORM INPUTS
    document.getElementById('form-add-product').reset();

    // Send a request to the Flask server
    fetch('/input-event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ product_name: product_name,
                               category: category,
                               price:price,
                               quantity:quantity })
    })
    .then(response => response.json())
    .then(data => console.log('Server response:', data))
    .catch(error => console.error('Error:', error));
});

function add_to_dynamic_table() {
    
}