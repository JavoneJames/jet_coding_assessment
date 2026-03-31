function getUserInput() {
  const displayError = document.getElementById("display-error");
  const inputText = document.getElementById("search-bar");
  const userInput = inputText.value.replace(/\s+/g, '');
  return userInput;
}

function buttonHandler() {
  const button = document.getElementById("search-button");

  button.addEventListener("click", async () => {
    const displayError = document.getElementById("display-error");
    try {
      const userInput = getUserInput();
			console.log(userInput)
      if (!userInput) {
        displayError.textContent = "Please enter a postcode";
      } else {
        displayError.textContent = "";
        window.location.href = `/frontend/results.html?postcode=${encodeURIComponent(userInput)}`;
      }
    } catch (err) {
      console.error("error", err);
      displayError.textContent = err.message;
    }
  });
}

buttonHandler();
