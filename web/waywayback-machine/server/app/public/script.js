function clearForm() {
    document.getElementById('urlInput').value = '';
    document.getElementById('result').style.display = 'none';
}

document.getElementById('snapshotForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const resultDiv = document.getElementById('result');
    const url = document.getElementById('urlInput').value;

    if (!url.trim()) {
        showResult('error', 'Please enter a URL');
        return;
    }

    try {
        new URL(url);
    } catch (e) {
        showResult('error', 'Please enter a valid URL (must start with http:// or https://)');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Creating Snapshot...';
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('/api/snapshot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (data.success) {
            showResult('success', `
                <h3>Snapshot Queued Successfully!</h3>
                <p><strong>Snapshot ID:</strong> ${data.snapshotId}</p>
                <p><strong>Target URL:</strong> ${data.targetUrl}</p>
                <p><strong>Archive URL:</strong> <a href="${data.url}" target="_blank">${window.location.origin}${data.url}</a></p>
                <p>${data.message}</p>
                <p id="statusMessage" style="margin-top: 10px; color: #666;"><em><span class="loading"></span> The waywayback machine is visiting your URL now...</em></p>
            `);

            pollSnapshotStatus(data.snapshotId, data.url);
        } else {
            showResult('error', `<h3>Error</h3><p>${data.error}</p>`);
        }
    } catch (error) {
        showResult('error', `<h3>Error</h3><p>Failed to create snapshot: ${error.message}</p>`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Archive This URL';
    }
});

async function pollSnapshotStatus(snapshotId, archiveUrl) {
    const maxAttempts = 20;
    const intervalMs = 3000;
    let attempts = 0;

    const interval = setInterval(async () => {
        attempts++;

        try {
            const response = await fetch(`/api/snapshot/${snapshotId}/status`);
            const data = await response.json();
            const statusEl = document.getElementById('statusMessage');

            if (!statusEl) {
                clearInterval(interval);
                return;
            }

            if (data.status === 'complete') {
                clearInterval(interval);
                statusEl.innerHTML = `<strong>Snapshot saved!</strong> Your page has been archived. <a href="${archiveUrl}" target="_blank">View it here</a>`;
                statusEl.style.color = '#2e7d32';

            } else if (data.status === 'failed') {
                clearInterval(interval);
                statusEl.innerHTML = `Snapshot failed: ${data.error || 'Unknown error'}`;
                statusEl.style.color = '#c62828';

            } else if (attempts >= maxAttempts) {
                clearInterval(interval);
                statusEl.innerHTML = `Still processing... check back later at <a href="${archiveUrl}" target="_blank">your archive link</a>.`;
                statusEl.style.color = '#666';
            }

        } catch (err) {
            clearInterval(interval);
            const statusEl = document.getElementById('statusMessage');
            if (statusEl) {
                statusEl.innerHTML = `Snapshot failed. Try inputting URL again.`;
                statusEl.style.color = '#c62828';
            }
        }
    }, intervalMs);
}

function showResult(type, message) {
    const resultDiv = document.getElementById('result');
    resultDiv.className = `result ${type}`;
    resultDiv.innerHTML = message;
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}