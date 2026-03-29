const resultsDiv = document.getElementById("results");
const displayError = document.getElementById("display-error");
const template = document.getElementById("restaurant-template");

// get postcode from query string
const urlParams = new URLSearchParams(window.location.search);
const postcode = urlParams.get("postcode");
console.log(postcode);
if (!postcode) {
  displayError.textContent = "No postcode provided.";
} else {
  fetch(`/restaurants/${encodeURIComponent(postcode)}`)
    .then((res) => {
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      const restaurants = Object.values(data);
      console.log(restaurants);
      if (restaurants.length === 0) {
        displayError.textContent = `No restaurants found near ${postcode}`;
        return;
      }
      resultsDiv.innerHTMl = "";
      restaurants.forEach((restaurant) => {
        const clone = template.content.cloneNode(true);
        clone.querySelector(".name").textContent = restaurant.name;
        clone.querySelector(".cuisines").textContent =
          restaurant.cuisines.join(", ");
        clone.querySelector(".rating").textContent = restaurant.rating;
        clone.querySelector(".address").textContent = restaurant.address;
        resultsDiv.appendChild(clone);
      });
    })
    .catch((err) => {
      console.error("Error fetching restaurants:", err);
      displayError.textContent = err.message;
    });
}
