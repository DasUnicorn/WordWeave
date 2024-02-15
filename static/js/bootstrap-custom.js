// JavaScript to initialize Bootstrap toasts after DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });

    // Show toasts when there are messages
    if (toastList.length > 0) {
        toastList.forEach(function (toast) {
            toast.show();
        });
    }
});
