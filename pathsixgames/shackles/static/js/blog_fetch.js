// This function is used to switch between pages on the adventure log!!! Do not delete!
function switchPage(page) {
  window.location.href = page;
}

fetch(adventureLogUrl)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  })
  .then((data) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(data, "text/html");
    const blogContainer = document.getElementById("blog-container");
    const newSection = doc.getElementById("new");

    if (newSection) {
      const title = newSection.querySelector("h2");
      const date = newSection.querySelector("h3");
      const image = newSection.querySelector("img");
      const firstParagraph = newSection.querySelector("p");

      if (title) {
        const entryTitle = document.createElement("h2");
        entryTitle.innerHTML = title.innerHTML;
        blogContainer.appendChild(entryTitle);
      }

      if (date) {
        const entryDate = document.createElement("h3");
        entryDate.innerHTML = date.innerHTML;
        blogContainer.appendChild(entryDate);
      }

      if (image) {
        const entryImage = document.createElement("img");
        entryImage.src = image.src;
        entryImage.alt = image.alt;
        blogContainer.appendChild(entryImage);
      }

      if (firstParagraph) {
        const entryParagraph = document.createElement("p");
        entryParagraph.innerHTML = firstParagraph.innerHTML;
        blogContainer.appendChild(entryParagraph);
      }
    }
  })
  .catch((error) => {
    console.log("An error occurred:", error);
  });
