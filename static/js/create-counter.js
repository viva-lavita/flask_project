function countCharacters(inputId, counterId, limit) {
    var input = document.getElementById(inputId);
    var counter = document.getElementById(counterId);
    var remainingCharacters = limit - input.value.length;

    counter.textContent = remainingCharacters;
  }

  var titleInput = document.getElementById("title");
  var introInput = document.getElementById("intro");
  var textInput = document.getElementById("text");

  titleInput.addEventListener("input", function() {
    countCharacters("title", "titleCounter", 50);
  });

  introInput.addEventListener("input", function() {
    countCharacters("intro", "introCounter", 200);
  });

  textInput.addEventListener("input", function() {
    countCharacters("text", "textCounter", 2000);
  });