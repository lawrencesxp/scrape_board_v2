document.getElementById('scrapeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileUrl = document.getElementById('fileUrl').value;
    const resultDiv = document.getElementById('result');

    try {
        // Send URL to Python backend
        const response = await fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: fileUrl })
        });

        const data = await response.json();

        if (data[0].error) {
            resultDiv.innerHTML = `<p class="text-red-500">${data[0].error}</p>`;
        } else {
            // Store data in localStorage and redirect
            localStorage.setItem('scrapedData', JSON.stringify(data));
            window.location.href = 'results.html';
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
    }
});