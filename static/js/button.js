function getUserInput() {
  const displayError = document.getElementById("display-error");
  const inputText = document.getElementById("search-bar");
  const userInput = inputText.value.replace(/\s+/g, "");
  return userInput;
}

function validationHandler(userInput) {
  const pattern =
    /^(GIR 0AA|(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRV-Y]?))\s?[0-9][ABD-HJLNP-UW-Z]{2}$/;
  return pattern.test(userInput);
}

function buttonHandler() {
  const button = document.getElementById("search-button");

  button.addEventListener("click", async () => {
    const displayError = document.getElementById("display-error");
    try {
      const userInput = getUserInput();
      validatedUserInput = validationHandler(userInput);
      if (!validatedUserInput) {
        displayError.textContent = "Please enter a valid postcode";
      } else {
				const res = await fetch(`/validate-postcode/${encodeURIComponent(userInput)}`);
				if (res.status != 200){
					displayError.textContent = "Please enter a valid postcode";
					console.log("error")
				}else{
					console.log("working")
					displayError.textContent = "";
					window.location.href = `/frontend/results.html?postcode=${encodeURIComponent(userInput)}`;
				}
      }
    } catch (err) {
      console.error("error", err);
      displayError.textContent = err.message;
    }
  });
}

buttonHandler();
