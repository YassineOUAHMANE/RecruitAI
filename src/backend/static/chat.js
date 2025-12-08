let conversationId = null;

/* ---------------------------------------------------
   Charger historique si ?id=xxx
----------------------------------------------------*/
function getQueryParam(name) {
    return new URLSearchParams(window.location.search).get(name);
}

window.addEventListener("DOMContentLoaded", async () => {
    const convId = getQueryParam("id");

    if (!convId) return;

    conversationId = convId;

    const res = await fetch(`/api/conversation/${convId}`);
    const data = await res.json();

    if (!data.message || !data.message.content) return;

    let box = document.getElementById("chatbox");

    // Charger anciens messages
    data.message.content.reverse().forEach(msg => {
        box.innerHTML += `
            <div class="message ${msg.sent_by_AI ? "bot" : "user"}">
                ${msg.sent_by_AI ? "🤖" : "👤"} ${msg.text}
            </div>
        `;
    });

    box.scrollTop = box.scrollHeight;
});

/* ---------------------------------------------------
   Créer une nouvelle conversation
----------------------------------------------------*/
async function startConversation(firstMessage) {
    const res = await fetch("/api/conversation/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: firstMessage })
    });

    const data = await res.json();
    conversationId = data.message.id;

    return data.message.response.text;
}

/* ---------------------------------------------------
   Envoi message
----------------------------------------------------*/
async function sendMessage() {
    let box = document.getElementById("chatbox");
    let input = document.getElementById("userInput");
    let msg = input.value.trim();
    if (!msg) return;

    // Message utilisateur (toujours même style)
    box.innerHTML += `
        <div class="message user">👤 ${msg}</div>
    `;
    box.scrollTop = box.scrollHeight;
    input.value = "";

    // Première interaction → création conversation
    if (conversationId === null) {
        const reply = await startConversation(msg);
        box.innerHTML += `
            <div class="message bot">🤖 ${reply}</div>
        `;
        box.scrollTop = box.scrollHeight;
        return;
    }

    // Envoi normal
    const res = await fetch(`/api/conversation/${conversationId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: msg })
    });

    const data = await res.json();

    const reply = data.message.text || "⚠ Aucun texte reçu";

    box.innerHTML += `
        <div class="message bot">🤖 ${reply}</div>
    `;
    box.scrollTop = box.scrollHeight;
}
