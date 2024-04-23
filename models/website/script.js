document.getElementById('predictButton').addEventListener('click', function() {
    const input = document.getElementById('fileInput');
    if (input.files.length > 0) {x
        const file = input.files[0];
        predictDisease(file);
    } else {
        alert('Please select an image file first.');
    }
});

async function predictDisease(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to predict the disease. Please try again.');
    }
}

function displayResult(result) {
    const resultDiv = document.getElementById('predictionResult');
    resultDiv.innerHTML = `Prediction: ${result.class} <br> Confidence: ${result.confidence.toFixed(2) * 100}%`;
}
