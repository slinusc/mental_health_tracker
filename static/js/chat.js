
// Funktion, um die initiale Nachricht hinzuzufügen
function addInitialMessage(username) {
    var li = document.createElement('li');
    li.classList.add('clearfix');
    var timeNow = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    li.innerHTML = `<div class="message-data">
                        <span class="message-data-time">${timeNow}, Today</span>
                    </div>
                    <div class="message other-message float-right">Hallo ${username}, wie geht es Dir heute?</div>`;
    document.getElementById('chat-messages').appendChild(li);
}

document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault(); // Verhindert, dass das Formular die Seite neu lädt
    var input = document.getElementById('chat-input');
    var message = input.value.trim();

    if(message) {
        // Erstellen Sie das Listenelement für die Nachricht und fügen Sie es dem Chat-Verlauf hinzu
        var li = document.createElement('li');
        li.classList.add('clearfix');
        li.innerHTML = '<div class="message-data"><span class="message-data-time">' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ', Today</span></div><div class="message my-message">' + message + '</div>';
        document.querySelector('.chat-history ul').appendChild(li);

        // Sende die Nachricht an das Backend
        try {
            var response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({user_message: message})
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            var data = await response.json(); // Erwarte die Antwort als JSON

            // Zeige die Antwort des Servers im Chat-Fenster, wenn erforderlich
            var liResponse = document.createElement('li');
            liResponse.classList.add('clearfix');
            liResponse.innerHTML = '<div class="message-data"><span class="message-data-time">' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ', Today</span></div><div class="message other-message float-right">' + data.response + '</div>';
            document.querySelector('#chat-messages').appendChild(liResponse);
        } catch (error) {
            console.error('Fetch error:', error);
        }

        // Setzen Sie das Eingabefeld zurück
        input.value = '';
    }
});


// Fügen Sie die initiale Nachricht hinzu, wenn das DOM vollständig geladen ist
document.addEventListener('DOMContentLoaded', function() {
    var benutzername = document.getElementById('benutzername').textContent;
    addInitialMessage(benutzername); // Verwenden Sie den Benutzernamen, um die initiale Nachricht hinzuzufügen
});

