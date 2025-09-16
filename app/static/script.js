document.addEventListener("DOMContentLoaded", function () {
    var swiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        spaceBetween: 30,
        centeredSlides: true,
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
    });

    const userIcon = document.getElementById('userIcon');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const closeMenu = document.getElementById('closeMenu');

    if (userIcon && dropdownMenu && closeMenu) {
        userIcon.addEventListener('click', () => {
            dropdownMenu.classList.add('active');
        });

        closeMenu.addEventListener('click', () => {
            dropdownMenu.classList.remove('active');
        });

        document.addEventListener('click', (e) => {
            if (!dropdownMenu.contains(e.target) && !userIcon.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });
    }
});
