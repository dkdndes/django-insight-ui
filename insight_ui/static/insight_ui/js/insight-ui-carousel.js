InsightUI.Carousel = {
    init: function () {
        const carousel = document.getElementById("carousel");
  const images = carousel.querySelectorAll("img");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const dotsContainer = document.getElementById("dots");

  const totalImages = images.length;
  let currentIndex = 0;
  let autoplayInterval;
  let startX = 0;

  function updateCarousel() {
    const offset = -currentIndex * 100;
    carousel.style.transform = `translateX(${offset}%)`;
    updateDots();
  }

  function updateDots() {
    const dots = dotsContainer.querySelectorAll("button");
    dots.forEach((dot, index) => {
      dot.classList.toggle("bg-white", index !== currentIndex);
      dot.classList.toggle("bg-blue-500", index === currentIndex);
    });
  }

  function createDots() {
    for (let i = 0; i < totalImages; i++) {
      const dot = document.createElement("button");
      dot.className = "w-3 h-3 rounded-full bg-white border border-gray-400 transition";
      dot.addEventListener("click", () => {
        currentIndex = i;
        updateCarousel();
        restartAutoplay();
      });
      dotsContainer.appendChild(dot);
    }
    updateDots();
  }

  function showNext() {
    currentIndex = (currentIndex + 1) % totalImages;
    updateCarousel();
  }

  function showPrev() {
    currentIndex = (currentIndex - 1 + totalImages) % totalImages;
    updateCarousel();
  }

  function startAutoplay() {
    autoplayInterval = setInterval(showNext, 5000);
  }

  function stopAutoplay() {
    clearInterval(autoplayInterval);
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  // Touch Events for Swipe
  carousel.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
  });

  carousel.addEventListener("touchend", (e) => {
    const endX = e.changedTouches[0].clientX;
    const diff = endX - startX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) {
        showPrev();
      } else {
        showNext();
      }
      restartAutoplay();
    }
  });

  // Event Listeners
  prevBtn.addEventListener("click", () => {
    showPrev();
    restartAutoplay();
  });

  nextBtn.addEventListener("click", () => {
    showNext();
    restartAutoplay();
  });

  // Init
  createDots();
  updateCarousel();
  startAutoplay();
    }
};
document.addEventListener('DOMContentLoaded', InsightUI.Carousel.init);
