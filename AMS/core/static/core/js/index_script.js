document.addEventListener('DOMContentLoaded', function() {
    // Slider Functionality
    let slideIndex = 0;

    function showSlides() {
        let slides = document.getElementsByClassName("slides")[0];
        let dots = document.getElementsByClassName("dot");

        slides.style.transform = `translateX(-${slideIndex * 100}%)`;

        for (let i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        dots[slideIndex].className += " active";
    }

    function changeSlide(n) {
        let slides = document.getElementsByClassName("slides")[0].children.length;
        slideIndex = (slideIndex + n + slides) % slides;
        showSlides();
    }

    function currentSlide(n) {
        slideIndex = n - 1;
        showSlides();
    }

    setInterval(() => {
        changeSlide(1);
    }, 4000);

    // Booking and Modal Functionality
    window.redirectToBooking = function() {
        window.location.href = "book_appointment";
    }

    window.confirmCancel = function() {
        var modal = document.getElementById("myModal");
        modal.style.display = "block";
    }

    window.closeModal = function() {
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
    }

    window.cancelAppointment = function() {
        closeModal();
        alert("Appointment canceled successfully.");
    }

    // Announcements Slider
    let currentAnnouncementIndex = 0;
    const announcements = document.querySelectorAll('.announcement-card');

    function showCurrentAnnouncement() {
        announcements.forEach((card, index) => {
            card.style.display = (index === currentAnnouncementIndex) ? 'block' : 'none';
        });
    }

    function changeAnnouncement(n) {
        currentAnnouncementIndex = (currentAnnouncementIndex + n + announcements.length) % announcements.length;
        showCurrentAnnouncement();
    }

    setInterval(() => {
        changeAnnouncement(1);
    }, 5000);

    showCurrentAnnouncement();


    // window.redirectToAppointments = function() {
    //     window.location.href = "{%url 'appointments' %}";
    // }
});
