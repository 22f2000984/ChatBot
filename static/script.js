// // async function ask() {
// //     const q = document.getElementById("q").value;

// //     const res = await fetch(`/ask?q=${encodeURIComponent(q)}`);
// //     const data = await res.json();

// //     document.getElementById("res").innerText = data.answer;
// // }

// const inputMessage = document.getElementById("inputMessage");
// const sendBtn = document.getElementById("sendBtn");
// const chatbox = document.getElementById("chatbox");


// function appendMessage(text,sender){
//     const msgDiv =document.createElement("div");
//     msgDiv.classList.add("message",sender);

//     const textBubble=document.createElement("span");
//     textBubble.classList.add("text-bubble");
//     textBubble.textContent=text;

//     if(sender=="bot"){
//         const iconImg=document.createElement("img");
//         iconImg.src="logo.jpg"
//         iconImg.classList.add("bot-chat-logo");
//         iconImg.alt="bot logo";
//         msgDiv.appendChild(iconImg);
//     }

//     msgDiv.appendChild(textBubble);
//     chatbox.appendChild(msgDiv);
//     chatbox.scrollTop=chatbox.scrollHeight;
// }



// async function sendMessage(){
//     const message=inputMessage.value.trim();

//     if(!message) return ; 
//     appendMessage(message,"user");
//     inputMessage.value = '';
//     sendBtn.disabled=true;
//     //  const res = await fetch(`/ask?q=${encodeURIComponent(q)}`);

//     try {
//         const response = await fetch(`/ask?q=${encodeURIComponent(q)}`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ message }),
//         });

//         if (!response.ok) throw new Error("Network response was not ok");

//         const data = await response.json();
//         // data.reply
//         appendMessage(data.reply,"bot")

//     } catch (error) {
//         appendMessage('Error: Could not reach the server.','bot');
//     } finally{
//         sendBtn.disabled=false;
//         inputMessage.focus();
//     }
    

// }

// // event
// sendBtn.addEventListener("click",sendMessage)
// inputMessage.addEventListener("keypress",function (e){
//     if (e.key === "Enter") sendMessage();
// })

async function ask() {
    const input = document.getElementById("q");
    const msgBox = document.getElementById("messages");

    const question = input.value.trim();
    if (!question) return;

    // Add user message
    msgBox.innerHTML += `<div class="msg user">${question}</div>`;
    input.value = "";

    // Scroll down
    msgBox.scrollTop = msgBox.scrollHeight;

    // Call backend
    const res = await fetch(`/ask?q=${encodeURIComponent(question)}`);
    const data = await res.json();

    // Add bot response
    msgBox.innerHTML += `<div class="msg bot">${data.answer}</div>`;

    msgBox.scrollTop = msgBox.scrollHeight;
}