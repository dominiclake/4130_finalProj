async function classifySMS() {
    const message = document.getElementById('message').value;
    const response = await fetch('https://four130-finalproj.onrender.com/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const result = await response.json();
    document.getElementById('result').innerText = 
        `Deep Learning: ${result.deep_learning_prediction}\nNaive Bayes: ${result.naive_bayes_prediction}`;
}