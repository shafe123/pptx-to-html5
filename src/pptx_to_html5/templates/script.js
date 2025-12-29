// Presentation navigation with support for hidden slides toggle
let currentSlide = 1;
let totalSlides = 0;
let showHidden = false;

function getAllSlides() {
    return Array.from(document.querySelectorAll('.slide'));
}

function getVisibleSlides() {
    if (showHidden) return getAllSlides();
    return getAllSlides().filter(s => !s.classList.contains('hidden-slide'));
}

document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('toggleHidden');
    if (toggle) {
        toggle.addEventListener('change', function(e) {
            showHidden = !!e.target.checked;
            // If showing hidden, remove the hiding class for display; if hiding, re-add
            const all = getAllSlides();
            all.forEach(s => {
                if (s.dataset.hidden === 'true') {
                    if (showHidden) s.classList.remove('hidden-slide');
                    else s.classList.add('hidden-slide');
                }
            });

            // Recalculate current slide index within visible slides
            const visible = getVisibleSlides();
            const active = document.querySelector('.slide.active');
            let newIndex = 0;
            if (active) {
                newIndex = visible.indexOf(active);
            }

            if (newIndex === -1) {
                // Active slide is hidden now; jump to first visible
                currentSlide = 1;
            } else {
                currentSlide = newIndex + 1;
            }

            totalSlides = visible.length;
            document.getElementById('totalSlides').textContent = totalSlides;
            updateSlide();
        });
    }

    document.getElementById('prevBtn').addEventListener('click', previousSlide);
    document.getElementById('nextBtn').addEventListener('click', nextSlide);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            previousSlide();
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
            e.preventDefault();
            nextSlide();
        } else if (e.key === 'Home') {
            goToSlide(1);
        } else if (e.key === 'End') {
            goToSlide(totalSlides);
        }
    });

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                previousSlide();
            }
        }
    }

    // Initialize counts and show first visible slide
    const visible = getVisibleSlides();
    totalSlides = visible.length;
    document.getElementById('totalSlides').textContent = totalSlides;
    // ensure starting slide is first visible
    currentSlide = 1;
    updateSlide();
});

function updateSlide() {
    const visible = getVisibleSlides();
    const all = getAllSlides();

    // Remove active from all
    all.forEach(s => s.classList.remove('active'));
    // Remove any running per-shape animations so they can restart when shown
    all.forEach(s => {
        const anims = s.querySelectorAll('.animatable');
        anims.forEach(a => {
            a.classList.remove('animate');
            // remove any custom properties to reset
            a.style.removeProperty('--anim-delay');
            a.style.removeProperty('--anim-duration');
        });
    });

    // Clamp currentSlide
    if (visible.length === 0) return;
    if (currentSlide < 1) currentSlide = 1;
    if (currentSlide > visible.length) currentSlide = visible.length;

    const slideToShow = visible[currentSlide - 1];
    if (!slideToShow) return;

    slideToShow.classList.add('active');

    // Play any per-shape animations configured on this slide
    const shapes = Array.from(slideToShow.querySelectorAll('.animatable'));
    shapes.forEach(el => {
        const delay = el.getAttribute('data-anim-delay') || '0';
        const duration = el.getAttribute('data-anim-duration') || '0.5';
        el.style.setProperty('--anim-delay', `${delay}s`);
        el.style.setProperty('--anim-duration', `${duration}s`);
        // Force reflow then add class to start animation
        void el.offsetWidth;
        el.classList.add('animate');
    });

    // Update counter
    document.getElementById('currentSlide').textContent = currentSlide;

    // Update progress bar
    const progress = (currentSlide / visible.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';

    // Update button states
    document.getElementById('prevBtn').disabled = currentSlide === 1;
    document.getElementById('nextBtn').disabled = currentSlide === visible.length;
}

function nextSlide() {
    const visible = getVisibleSlides();
    if (currentSlide < visible.length) {
        currentSlide++;
        updateSlide();
    }
}

function previousSlide() {
    if (currentSlide > 1) {
        currentSlide--;
        updateSlide();
    }
}

function goToSlide(slideNumber) {
    const visible = getVisibleSlides();
    if (slideNumber >= 1 && slideNumber <= visible.length) {
        currentSlide = slideNumber;
        updateSlide();
    }
}

// Prevent default space bar scrolling
window.addEventListener('keydown', function(e) {
    if (e.key === ' ' && e.target === document.body) {
        e.preventDefault();
    }
});
