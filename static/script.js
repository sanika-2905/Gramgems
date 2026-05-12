async function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const btn = document.getElementById('genBtn');
    const resBox = document.getElementById('result-box');

    if (!fileInput.files[0]) return alert("Select a photo first! ✨");

    btn.innerText = "💎 Polishing Gems...";
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        const data = await response.json();

        btn.innerText = "Reveal More";
        resBox.innerHTML = `<span class="category-pill">${data.category}</span>`;
        
        data.captions.forEach(text => {
            const div = document.createElement('div');
            div.className = 'caption-gem';
            div.innerText = text;
            div.onclick = () => {
                navigator.clipboard.writeText(text);
                const oldText = div.innerText;
                div.innerText = "Saved to Palette! ✅";
                setTimeout(() => div.innerText = oldText, 1200);
            };
            resBox.appendChild(div);
        });
    } catch (e) {
        btn.innerText = "Try Again";
        alert("Server error. Check app.py!");
    }
}

document.getElementById('fileInput').onchange = (e) => {
    const img = document.getElementById('preview');
    const drop = document.getElementById('drop-text');
    img.src = URL.createObjectURL(e.target.files[0]);
    img.style.display = 'block';
    drop.style.display = 'none';
};