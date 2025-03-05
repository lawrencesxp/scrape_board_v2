document.addEventListener('DOMContentLoaded', () => {
    const dataTable = document.getElementById('dataTable');
    
    // Parse data and replace NaN with null
    const parseScrapedData = (data) => {
        return data.map(row => {
            const parsedRow = {};
            for (const [key, value] of Object.entries(row)) {
                // Replace NaN with null, convert undefined to null
                parsedRow[key] = (value === 'NaN' || value === undefined) ? null : value;
            }
            return parsedRow;
        });
    };

    // Try to parse the data, handling potential errors
    let scrapedData;
    try {
        const storedData = localStorage.getItem('scrapedData');
        scrapedData = storedData ? parseScrapedData(JSON.parse(storedData)) : [];
    } catch (error) {
        console.error('Error parsing stored data:', error);
        scrapedData = [];
    }

    if (!scrapedData || scrapedData.length === 0) {
        dataTable.innerHTML = '<p class="text-center text-red-500">No data found</p>';
        return;
    }

    // Create table
    const table = document.createElement('table');
    table.className = 'w-full';

    // Create table header
    const thead = document.createElement('thead');
    thead.className = 'bg-gray-200';
    const headerRow = document.createElement('tr');
    
    // Get headers from first row
    const headers = Object.keys(scrapedData[0]);
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        th.className = 'p-3 text-left border';
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement('tbody');
    scrapedData.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'border-b hover:bg-gray-100';
        
        headers.forEach(header => {
            const td = document.createElement('td');
            // Handle null values
            td.textContent = row[header] === null ? 'N/A' : row[header];
            td.className = 'p-3 border';
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    dataTable.appendChild(table);
});