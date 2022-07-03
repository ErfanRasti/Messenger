// user_id: id of the user
const user_id = JSON.parse(document.getElementById('json-username').textContent);

// message_username: message from the user
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

// Establishing a connection with the server
const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + user_id + '/'
);

// Opening the connection
socket.onopen = function (e) { console.log("CONNECTION ESTABLISHED"); }

// Closing the connection
socket.onclose = function (e) { console.log("CONNECTION LOST"); }

// Error handling
socket.onerror = function (e) { console.log(e); }

// Receiving a message
socket.onmessage = function (e) { console.log(e); }

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username
    }));

    message_input.value = '';
}