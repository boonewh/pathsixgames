// Select all images within the container
const images = document.querySelectorAll(".container4 img");

// Define the Intersection Observer
const observer = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add("pop");
          observer.unobserve(entry.target);
        }, 500 * index); // Delay the animation here!
      }
    });
  },
  {
    threshold: 0.1,
    rootMargin: "-150px 0px 0px 0px",
  }
);

// Observe each image
images.forEach((image) => {
  observer.observe(image);
});
