let authHeader = "";

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;
    authHeader = 'Basic ' + btoa(user + ":" + pass);
    document.getElementById("login-form").style.display = "none";
    document.getElementById("main").style.display = "block";
    loadOperations();
});

async function startOperation() {
    const data = {
        worker_id: document.getElementById("worker_id").value,
        order_number: document.getElementById("order_number").value
    };
    await fetch('/operations/start', {
        method: 'POST',
        headers: {
            'Authorization': authHeader,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    loadOperations();
}

async function stopOperation(id) {
    await fetch(`/operations/stop/${id}`, {
        method: 'POST',
        headers: { 'Authorization': authHeader }
    });
    loadOperations();
}

async function loadOperations() {
    const from = document.getElementById("filter_from").value;
    const to = document.getElementById("filter_to").value;
    let url = '/operations';
    if (from || to) {
        url += `?from=${from}&to=${to}`;
    }
    const res = await fetch(url, {
        headers: { 'Authorization': authHeader }
    });
    const data = await res.json();
    const tbody = document.querySelector("#operation-table tbody");
    tbody.innerHTML = "";
    data.forEach(op => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${op.id}</td>
            <td>${op.worker_id}</td>
            <td>${op.order_number}</td>
            <td>${formatTime(op.start_time)}</td>
            <td>${op.end_time ? formatTime(op.end_time) : "-"}</td>
            <td>${!op.end_time ? `<button onclick="stopOperation(${op.id})">STOP</button>` : ""}</td>
        `;
        tbody.appendChild(row);
    });
}

function formatTime(isoStr) {
    const date = new Date(isoStr);
    return date.toLocaleString();
}

function exportCSV() {
    const from = document.getElementById("filter_from").value;
    const to = document.getElementById("filter_to").value;
    let url = '/export';
    if (from || to) {
        url += `?from=${from}&to=${to}`;
    }
    fetch(url, {
        headers: { 'Authorization': authHeader }
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "operacie.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
}
