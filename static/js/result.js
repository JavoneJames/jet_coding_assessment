async function fetchRestaurantsFromServer() {
  const urlParams = new URLSearchParams(window.location.search);
  const postcode = urlParams.get("postcode");
  const displayError = document.getElementById("display-error");

  try {
    const res = await fetch(`/restaurants/${encodeURIComponent(postcode)}`);
    if (res.status != 200) throw new Error(`Server errpr: ${res.status}`);
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

  if (fetchedRestaurants.length === 0) {
    displayError.textContent = "No restaurants found.";
    return;
  }

  Object.values(fetchedRestaurants).forEach((restaurant) => {
    const clone = template.content.cloneNode(true);
    clone.querySelector(".name").textContent = restaurant.name;
    clone.querySelector(".cuisines").textContent =
      restaurant.cuisines.join(", ");
    clone.querySelector(".rating").textContent = restaurant.rating;
    clone.querySelector(".address").textContent = restaurant.address;
    resultsDiv.appendChild(clone);
  });
}

function searchHandler(fetchedRestaurants) {
  console.log(fetchedRestaurants);
  const searchInput = document.getElementById("search-bar");
  const restaurantsArray = Object.values(fetchedRestaurants);

  const fuse = new Fuse(restaurantsArray, {
    keys: [
      "name",
      { name: "cuisines", getFn: (r) => (r.cuisines || []).join(" ") },
    ],
    threshold: 0.3,
  });

  searchInput.addEventListener("input", () => {
    const search = searchInput.value;
    let filteredResults;
    if (search) {
      filteredResults = fuse.search(search).map((result) => result.item);
    } else {
      filteredResults = restaurantsArray;
    }
    renderFilteredRestaurants(fetchedRestaurants, filteredResults);
  });
}

function renderFilteredRestaurants(fetchedRestaurants, filteredResults) {
  const displayError = document.getElementById("display-error");
  if (filteredResults.length > 0) {
    displayError.textContent = "";
    renderRestaurants(filteredResults);
  } else {
    displayError.textContent = "No restaurants found.";
    document.getElementById("results").innerHTML = "";
  }
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
      const selectedRatings = getSelectedRatings(checkboxes);
      const filteredRestaurantsByRating = getFilteredRestaurantsByRating(
        fetchedRestaurants,
        selectedRatings,
      );
      renderFilteredRestaurants(
        fetchedRestaurants,
        filteredRestaurantsByRating,
      );
    });
  });
}

function getSelectedRatings(checkboxes) {
  return checkboxes.filter((cb) => cb.checked).map((cb) => Number(cb.value));
}

function getFilteredRestaurantsByRating(fetchedRestaurants, selectedRatings) {
  return Object.values(fetchedRestaurants).filter((restaurant) => {
    const roundRating = Math.round(restaurant.rating);
    return (
      selectedRatings.length === 0 || selectedRatings.includes(roundRating)
    );
  });
}

async function initialize() {
  const fetchedRestaurants = await fetchRestaurantsFromServer();
  if (Object.keys(fetchedRestaurants).length === 0) return;
  renderRestaurants(fetchedRestaurants);
  searchHandler(fetchedRestaurants);
  ratingHandler(fetchedRestaurants);
}

initialize();
