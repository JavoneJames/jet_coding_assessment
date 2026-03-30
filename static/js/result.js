async function fetchRestaurantsFromServer() {

  const urlParams = new URLSearchParams(window.location.search);
  const postcode = urlParams.get("postcode");
  const displayError = document.getElementById("display-error");

  try {
    const res = await fetch(`/restaurants/${encodeURIComponent(postcode)}`);
    if (!res.ok) throw new Error(`Server errpr: ${res.status}`);
    return res.json();
  } catch (err) {
    console.error("Error fetching restaurants:", err);
    displayError.textContent = err.message;
  }

}

function renderRestaurants(fetchedRestaurants) {

  const resultsDiv = document.getElementById("results");
  const displayError = document.getElementById("display-error");
  const template = document.getElementById("restaurant-template");

  resultsDiv.innerHTML = "";

  if (Object.keys(fetchedRestaurants).length === 0) {
    displayError.textContent = "No restaurants found.";
    return;
  }

  Object.keys(fetchedRestaurants).forEach((key) => {
    const restaurant = fetchedRestaurants[key];
    const clone = template.content.cloneNode(true);
    clone.querySelector(".name").textContent = restaurant.name;
    clone.querySelector(".cuisines").textContent = restaurant.cuisines.join(", ");
    clone.querySelector(".rating").textContent = restaurant.rating;
    clone.querySelector(".address").textContent = restaurant.address;
    resultsDiv.appendChild(clone);
  });

}

async function initialize() {
  const fetchedRestaurants = await fetchRestaurantsFromServer();
  if (fetchedRestaurants) {
    renderRestaurants(fetchedRestaurants);
  }
}

initialize();
