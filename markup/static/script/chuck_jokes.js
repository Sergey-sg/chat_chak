const chatMessages = document.body.querySelector('#chat-messages');
const roomsList = document.body.querySelector('#chat-rooms');
const allRooms = document.body.querySelectorAll('.room-names')

async function addAnswerFromChuck(url) {
    try {
        let response = await fetch(url, {method: "GET"});
        if (response.status === 200) {
            return response;
        }
    } catch (error) {
        console.log(error);
    }
}

roomsList.addEventListener('click', (event) => {
    let target = event.target

    if (target.classList.contains('room-names')) {
        event.preventDefault();

        for (let i = 0; i < allRooms.length; i++) {
            if (allRooms[i].classList.contains('bg-danger')) {
                allRooms[i].classList.remove('bg-danger')
            }
        }
        
        target.classList.add('bg-danger');
    }
});

<script src="{{ static ('script/chuck_jokes.js') }}"></script>