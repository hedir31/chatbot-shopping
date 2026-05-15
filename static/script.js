let isFirstMessage = true;

async function sendMessage() {
    let input = document.getElementById("input");
    let message = input.value;
    if (message.trim() === "") return;

    if (isFirstMessage) {
        addToHistory(message);
        isFirstMessage = false;
    }

    addMessage(message, "user");
    input.value = "";
    
    let loading = addMessage("Typing...", "bot");
    
    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });
    let data = await res.json();
    loading.innerText = data.reply;
}

function addMessage(text, sender) {
    let div = document.createElement("div");
    div.className = "msg " + sender;
    div.innerText = text;
    document.getElementById("messages").appendChild(div);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
    return div;
}

function addToHistory(text) {
    let historyList = document.getElementById("history-list");
    
    let activeItem = document.querySelector(".history-item.active");
    if (activeItem) activeItem.classList.remove("active");

    let div = document.createElement("div");
    div.className = "history-item active";
    div.innerHTML = `<i class="far fa-comment"></i> ${text}`;
    historyList.insertBefore(div, historyList.firstChild);
}

function createNewChat() {
    document.getElementById("messages").innerHTML = `<div class="msg bot">welcome to chicbot, how can i help u today !🛍️🛍️</div>`;
    isFirstMessage = true;
}