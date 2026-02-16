document.getElementById('checkUrl').addEventListener('click', async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const resultDiv = document.getElementById('result');
  
  resultDiv.innerText = "Analyzing...";

  const response = await fetch('http://localhost:5000/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: tab.url })
  });

  const data = await response.json();
  resultDiv.innerText = `Result: ${data.label}`;
  resultDiv.style.color = data.prediction === 1 ? "red" : "green";
});