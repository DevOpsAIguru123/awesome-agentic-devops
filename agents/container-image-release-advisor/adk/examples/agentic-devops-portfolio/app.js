const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');

navToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});

nav?.addEventListener('click', (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    nav.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  }
});

const reveal = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      reveal.unobserve(entry.target);
    }
  }
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => reveal.observe(element));
document.querySelector('#year').textContent = String(new Date().getFullYear());
