let prevButton = document.getElementById('prev');
let nextButton = document.getElementById('next');
let container = document.querySelector('.container');
let items = container.querySelectorAll('.list .item');
let indicator = document.querySelector('.indicators');
let dots = indicator.querySelectorAll('ul li');

let active = 0; 
let firstPosition = 0;
let lastPosition = items.length - 1;

function updateIndicators() {
    dots.forEach(dot => dot.classList.remove('active'));
    dots[active].classList.add('active');

    indicator.querySelector('.number').innerHTML = `0${active + 1}`;
}

function updateItems() {
    let itemOld = container.querySelector('.list .item.active');
    itemOld.classList.remove('active');
    itemOld.classList.remove('prev');
    itemOld.classList.remove('next');
    
    items[active].classList.add('active');
  
    if (active > 0) {
        items[active].classList.add('next'); 
    } else {
        items[active].classList.add('prev'); 
    }

    updateIndicators(); 
}

nextButton.onclick = () => {
    active = active + 1 > lastPosition ? 0 : active + 1; 
    updateItems();
};

prevButton.onclick = () => {
    active = active - 1 < firstPosition ? lastPosition : active - 1; 
    updateItems();
};

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        active = index; 
        updateItems(); 
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("contactModal");
    var openBtn = document.getElementById("openModal");
    var closeBtn = document.getElementById("close");

    if (openBtn) {
        openBtn.onclick = function () {
            modal.style.display = "flex"; 
        };
    }

    if (closeBtn) {
        closeBtn.onclick = function () {
            modal.style.display = "none"; 
        };
    }

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none"; 
        }
    };
});

let startX;
let endX;

container.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

container.addEventListener('touchend', (e) => {
    endX = e.changedTouches[0].clientX;
    handleSwipe();
});

function handleSwipe() {
    if (startX - endX > 50) {
     
        nextSlide();
    } else if (endX - startX > 50) {
  
        prevSlide();
    }
}

function nextSlide() {
    active = active + 1 > lastPosition ? 0 : active + 1;
    updateItems();
}

function prevSlide() {
    active = active - 1 < firstPosition ? lastPosition : active - 1;
    updateItems();
}
