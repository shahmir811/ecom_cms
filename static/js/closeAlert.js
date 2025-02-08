// Closes the alert after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
	setTimeout(function () {
		let alerts = document.querySelectorAll('.alert');
		alerts.forEach(alert => {
			let bsAlert = new bootstrap.Alert(alert);
			bsAlert.close();
		});
	}, 5000);
});
