function updateBookingHistory() {
    fetch('/booking_history/')
        .then(response => response.json())
        .then(data => {
            let bookingList = document.getElementById('booking-list');
            bookingList.innerHTML = '';
            data.bookings.forEach(booking => {
                let item = `<li>Transport: ${booking.transport} | Date: ${booking.booking_date} | Seat: ${booking.seat_number}</li>`;
                bookingList.innerHTML += item;
            });
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    updateBookingHistory();
});




// Booking button interaction
document.querySelector('.book-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent form from submitting right away for demo purposes

    // Simulate loading
    const button = this;
    button.textContent = "Booking...";
    button.style.backgroundColor = "#00796b";

    // Simulate delay
    setTimeout(() => {
        button.textContent = "Booked!";
        button.style.backgroundColor = "#00bfa5";
    }, 2000);
});
