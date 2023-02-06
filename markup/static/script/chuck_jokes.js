const chatMessages = document.body.querySelector('#chat-messages');
const roomsList = document.body.querySelector('#chat-rooms');
const messageForm = document.body.querySelector('#message-form');
const discussionRoom = document.body.querySelector('#discussion-room');
const activeRoomName = document.body.querySelector("#active-room-name");

function getCookie(name) {
    let cookie = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return cookie ? cookie[2] : null;
}

async function sendMessage(url, data, csrfToken, roomId) {
    try {
        let response = await fetch(url, {
            method: "POST", body: data, 
            headers:{"X-CSRFToken": csrfToken},
            dataType:'json',
        });
        if (response.status === 200) {    
            response = await response.json();
            createMessageComponent(response);
            setTimeout(addAnswerFromChuck, 15000, chatMessages.getAttribute("data-urlJokes"), roomId);
            const content = document.body.querySelector("input[name='content']");
            content.value = '';
        }
    } catch (error) {
        console.log(error);
    }
}

messageForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const csrfToken = document.body.querySelector("input[name='csrfmiddlewaretoken']").value;
    const roomId = document.body.querySelector("input[name='roomId']").value;
    const content = document.body.querySelector("input[name='content']").value;
    const createMessageUrl = messageForm.getAttribute('action');
    const data = new FormData();
    data.append('room', roomId);
    data.append('content', content);
    sendMessage(createMessageUrl, data, csrfToken, roomId);
})

async function addAnswerFromChuck(url, roomId) {
    const data = new FormData();
    data.append('roomId', roomId);
    try {
        let response = await fetch(url, { 
            method: "POST" ,
            headers: {"X-CSRFToken": getCookie("csrftoken")}, 
            body: data
        });
        if (response.status === 200) {
            const data = await response.json();
            createMessageComponent(data);
        }
    } catch (error) {
        console.log(error);
    }
}

function createMessageComponent(message) {
    const messageComponent = document.createElement('p'); 
    const br = document.createElement('br');
    const time = document.createElement('span');
    time.innerText = message.updated;
    time.classList.add('small');
    messageComponent.innerText = message.content;
    messageComponent.appendChild(br);
    messageComponent.appendChild(time);
    if (message.author) {
        messageComponent.classList.add('text-end');
    }
    chatMessages.appendChild(messageComponent);
}

async function getMessagesList(url) {
    try {
        let response = await fetch(url, {method: "GET"});
        if (response.status === 200) {    
            response = await response.json();
            chatMessages.innerHTML = '';
            for (let message of response.messagesList) {
                createMessageComponent(message) 
            }
        }
    } catch (error) {
        console.log(error);
    }
}

roomsList.addEventListener('click', (event) => {
    let target = event.target

    if (target.classList.contains('room-names')) {
        event.preventDefault();
        const activeRoom = document.body.querySelector("p.room-names.bg-info")

        if (activeRoom) {
            activeRoom.classList.remove('bg-info')
        }

        target.classList.add('bg-info');
        
        const roomName = target.getAttribute("data-name");
        const roomPrivate = target.getAttribute("data-private");
        const hiddenInputId = document.querySelector("input[name='roomId']");
        const roomId = target.getAttribute('data-pk')

        hiddenInputId.value = roomId;
        activeRoomName.innerHTML = target.innerHTML 
        discussionRoom.style.display = ''

        getMessagesList(target.getAttribute('data-urlMessages'))
    }
});