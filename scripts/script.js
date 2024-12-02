const dynamicText = document.getElementById("dyanmicText");

function updateText(message, result){
    dynamicText.innerHTML = `
    <p>${message}</p>
    <p>Deep Learning: ${result.deep_learning_prediction} Naive Bayes: ${result.naive_bayes_prediction}</p> 
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

