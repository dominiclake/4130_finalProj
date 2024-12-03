let dynamicText = document.getElementById("dynamicText");

function getPredictionLabel(value) {
    const labels = ['personal', 'spam', 'business', 'other'];
    return labels[value] || 'unknown';
}

function updateText(message, result){
    dynamicText.innerHTML = `
    <p>${message}</p>
    <p>Deep Learning: ${getPredictionLabel(result.deep_learning_prediction)} Naive Bayes: ${getPredictionLabel(result.naive_bayes_prediction)}</p> 
    `;
}


async function classifySMS() {
    const message = document.getElementById('message').value;
    const response = await fetch('https://four130-finalproj.onrender.com/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const result = await response.json();
    updateText(message, result);
}

