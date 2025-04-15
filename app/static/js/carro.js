function toggleDetalhes(button) {
  const card = button.closest('.carro-card');
  const icon = button.querySelector('i');
  const detalhes = card.querySelector('.carro-detalhes');

  if (card.classList.contains('detalhes-ativo')) {
    detalhes.style.maxHeight = '0px';
    detalhes.style.opacity = '0';
    detalhes.style.padding = '0';
    detalhes.style.position = 'absolute'; 
  } else {
    detalhes.style.opacity = '1';
    detalhes.style.padding = '15px';
    detalhes.style.position = 'relative'; 
    setTimeout(() => {
      detalhes.style.maxHeight = '1000px'; 
    }, 10);
  }

  card.classList.toggle('detalhes-ativo');
  icon.classList.toggle('fa-plus');
  icon.classList.toggle('fa-minus');
  button.setAttribute('aria-expanded', card.classList.contains('detalhes-ativo'));
}


document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.swiper-container').forEach(container => {
      const slides = container.querySelectorAll('.swiper-slide');
      
      //
      if (slides.length > 0) {
          new Swiper(container, {
              loop: slides.length > 1, 
              navigation: slides.length > 1 ? {
                  nextEl: container.querySelector('.swiper-button-next'),
                  prevEl: container.querySelector('.swiper-button-prev'),
              } : false,
              pagination: slides.length > 1 ? {
                  el: container.querySelector('.swiper-pagination'),
                  clickable: true,
              } : false,
          });
      }
  });
});
