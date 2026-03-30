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
    clone.querySelector(".cuisines").textContent =
      restaurant.cuisines.join(", ");
    clone.querySelector(".rating").textContent = restaurant.rating;
    clone.querySelector(".address").textContent = restaurant.address;
    resultsDiv.appendChild(clone);
  });
}

function filterSearchResults(fetchedRestaurants, search) {
  if (!fetchedRestaurants) return restaurants;

  return Object.values(fetchedRestaurants).filter((restaurant) => {
    const nameMatch = restaurant.name
      .toLowerCase()
      .includes(search.toLowerCase());
    const cuisineMatch = restaurant.cuisines
      .join(", ")
      .toLowerCase()
      .includes(search.toLowerCase());
    return nameMatch || cuisineMatch;
  });
}

function searchHandler(fetchedRestaurants) {
  const searchInput = document.getElementById("search-bar");

  searchInput.addEventListener("input", () => {
    const search = searchInput.value;
    const filteredResults = filterSearchResults(fetchedRestaurants, search);

    if (filteredResults && filteredResults.length > 0) {
      renderRestaurants(filteredResults);
    } else {
      renderRestaurants(fetchedRestaurants);
    }
  });
}

function ratingHandler(fetchedRestaurants) {
  const ratingContainer = document.getElementById("rating-options");
  if (!ratingContainer) return;
  const inputs = ratingContainer.getElementsByTagName("input");
  const checkboxes = Array.from(inputs).filter(
    (input) => input.type === "checkbox",
  );

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const selectedRatings = checkboxes
        .filter((cb) => cb.checked)
        .map((cb) => Number(cb.value));
      console.log("Selected ratings:", selectedRatings);
    });
  });
}

async function initialize() {
  const fetchedRestaurants = await fetchRestaurantsFromServer();
  renderRestaurants(fetchedRestaurants);
  searchHandler(fetchedRestaurants);
  ratingHandler(fetchedRestaurants);
}

initialize();
