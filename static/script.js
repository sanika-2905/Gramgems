let selectedFile = null;

const fileInput = document.getElementById("fileInput");
const previewImg = document.getElementById("preview");
const noImageText = document.getElementById("noImageText");
const generateBtn = document.querySelector("button");
const captionText = document.getElementById("caption");
const tagsText = document.getElementById("tags");

fileInput.addEventListener("change", function() {
    selectedFile = this.files[0];
    if (selectedFile) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = "block";
            noImageText.style.display = "none";
            captionText.innerText = "Ready to generate...";
        };
        reader.readAsDataURL(selectedFile);
    }
});

function generateCaption() {
    if (!selectedFile) {
        alert("Please upload a photo first! 📸");
        return;
    }

    const originalBtnText = generateBtn.innerHTML;
    generateBtn.innerHTML = "Lumina is thinking... ✨";
    generateBtn.disabled = true;

    // Grab optional inputs (Assuming these IDs or placeholders exist in your HTML)
    const customTags = document.querySelector('input[placeholder*="tags"]')?.value || "";
    const customLink = document.querySelector('input[placeholder*="link"]')?.value || "";

    let formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("custom_tags", customTags);
    formData.append("custom_link", customLink);

    fetch("/generate", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            captionText.innerText = data.caption;
            tagsText.innerText = data.hashtags;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Server failed. Check your terminal!");
    })
    .finally(() => {
        generateBtn.innerHTML = originalBtnText;
        generateBtn.disabled = false;
    });
}

generateBtn.addEventListener("click", generateCaption);