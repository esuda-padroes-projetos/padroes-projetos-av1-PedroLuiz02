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
    

      const bagIcon = document.getElementById('bagIcon');
      const dropdownMenuBag = document.getElementById('dropdownMenuBag');
      const closeMenuBag = document.getElementById('closeMenuBag');
    
      if (bagIcon && dropdownMenuBag && closeMenuBag) {
          bagIcon.addEventListener('click', () => {
              dropdownMenuBag.classList.add('active');
          });
    
          closeMenuBag.addEventListener('click', () => {
              dropdownMenuBag.classList.remove('active');
          });
    
          document.addEventListener('click', (e) => {
              if (!dropdownMenuBag.contains(e.target) && !bagIcon.contains(e.target)) {
                  dropdownMenuBag.classList.remove('active');
              }
          });
      }
    

        const quantityInput = document.getElementById("quantity");
        const aumentarBtn = document.getElementById("aumentar");
        const diminuirBtn = document.getElementById("diminuir");
      
        if (quantityInput && aumentarBtn && diminuirBtn) {
            aumentarBtn.addEventListener("click", () => {
            quantityInput.value = parseInt(quantityInput.value) + 1;
          });
      
          diminuirBtn.addEventListener("click", () => {
            if (parseInt(quantityInput.value) > 1) {
              quantityInput.value = parseInt(quantityInput.value) - 1;
            }
          });
        }
    });
    