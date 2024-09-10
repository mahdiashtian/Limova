function updateQueryParameters(key, value) {
    // Get the current URL
    const url = new URL(window.location.href);

    // Update the query parameter with the new value
    url.searchParams.set(key, value);

    // Handle pagination and sorting separately
    // Only modify the necessary parameters
    if (key === 'sort') {
        // Set the `sort` parameter and remove `page` parameter to avoid changing pages
        url.searchParams.set('sort', value);
        url.searchParams.delete('page');
    } else if (key === 'paginateBy') {
        // Set the `paginateBy` parameter and remove `page` parameter to avoid changing pages
        url.searchParams.set('paginateBy', value);
        url.searchParams.delete('page');
    }

    // Submit the form with updated query parameters
    window.location.href = url.href;
}

// Attach event listeners once the document is loaded
document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('SortBy');
    const paginateSelect = document.getElementById('paginateBy');

    function updateQueryParam(param, value) {
        const url = new URL(window.location.href);
        url.searchParams.set(param, value);
        window.location.href = url.toString();
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            updateQueryParam('sort', sortSelect.value);
        });
    }

    if (paginateSelect) {
        paginateSelect.addEventListener('change', function () {
            updateQueryParam('paginateBy', paginateSelect.value);
        });
    }
});
