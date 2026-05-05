async function sendMessage() {
    let input = document.getElementById("input");
    let message = input.value;
    if (message.trim() === "") return;
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
    document.getElementById("messages").scrollTop =
        document.getElementById("messages").scrollHeight;
    return div;
}