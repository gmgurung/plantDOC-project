document.addEventListener("DOMContentLoaded", function () {
  // Listen for clicks on the 'Select an Image' button to trigger file selection
  document.getElementById("selectImage").addEventListener("click", function () {
    document.getElementById("fileInput").click();
  });

  // Once a file is selected, handle the file input change
  document.getElementById("fileInput").addEventListener("change", function () {
    if (this.files.length > 0) {
      const file = this.files[0];
      predictDisease(file);
    } else {
      alert("Please select an image file first.");
    }
  });

  async function predictDisease(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      displayResult(result);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to predict the disease. Please try again.");
    }
  }

  function displayResult(result) {
    const resultDiv = document.getElementById("predictionResult");
    const confidencePercentage = (result.confidence * 100).toFixed(2);
    resultDiv.innerHTML = `Prediction: ${result.class} <br> Confidence: ${confidencePercentage}%`;
  }

}); // This closing bracket and parenthesis were added to correctly close the 'DOMContentLoaded' event listener.
