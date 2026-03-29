const button = document.getElementById("search-button");
const inputText = document.getElementById("search-bar");
const displayError = document.getElementById("display-error");

button.addEventListener("click", async () => {
  try {
    const userInput = inputText.value.trim();
    if (!userInput) {
      displayError.textContent = "Please enter a postcode";
      console.log("no input");
      return;
    }
    displayError.textContent = "";
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${encodeURIComponent(userInput)}`,
    );
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    const restaurants = Object.values(data);

    if (restaurants.length == 0) {
      displayError.textContent = `No restaurants found near ${userInput}`;
    } else {
      document.getElementById("display-error").textContent = "";
    }
    window.location.href = `/frontend/results.html?postcode=${encodeURIComponent(userInput)}`;
  } catch (err) {
    console.error("error", err);
    displayError.textContent = err.message;
  }
});
