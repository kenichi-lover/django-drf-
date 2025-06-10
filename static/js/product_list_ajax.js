// static/js/product_list_ajax.js

$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Handle Add Product Form Submission
    $('#addProductForm').submit(function(e) {
        e.preventDefault(); // Prevent default form submission

        const $form = $(this);
        const url = $form.attr('action');
        const formData = $form.serialize();
        const $errorDiv = $('#add-product-errors');

        $errorDiv.addClass('d-none').text(''); // Hide previous errors

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                // Assuming successful response includes the new product data
                // Clear the form
                $form[0].reset();
                // Add success message (optional, you can use Django messages or a toast)
                // Append new product to table (basic example, consider sorting/pagination)
                const newRow = `
                    <tr id="product-row-${response.id}">
                        <td>${response.id}</td>
                        <td><a href="/admin/myapp/product/${response.id}/change/">${response.name}</a></td>{# Adjust URL if not default admin change view #}
                        <td>${response.category_name || 'N/A'}</td>
                        <td>$${response.price}</td>
                        <td>${response.stock}</td>
                        <td>${response.is_active ? 'Yes' : 'No'}</td>
                        <td>
                            <a href="/admin/myapp/product/${response.id}/change/" class="btn btn-sm btn-info">Edit</a>{# Adjust URL #}
                            <button class="btn btn-sm btn-danger delete-product-btn" data-product-id="${response.id}">Delete</button>
                        </td>
                    </tr>
                `;
                $('#productTable tbody').append(newRow);
                // Optionally add a Django success message via AJAX
                // $.post('/admin/your_app/add_message/', {message: 'Product added successfully', tags: 'success'});
                // Or simply show a success alert
                alert('Product added successfully!');
            },
            error: function(xhr) {
                const errors = xhr.responseJSON;
                let errorHtml = '';
                if (errors) {
                    for (const field in errors) {
                        errorHtml += `<strong>${field}:</strong> ${errors[field].join('<br>')}<br>`;
                    }
                } else {
                    errorHtml = 'An unexpected error occurred.';
                }
                $errorDiv.removeClass('d-none').html(errorHtml);
            }
        });
    });

});