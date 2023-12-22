const messageIcon = document.getElementById('message-icon');
let chatWindow = document.getElementById('chat_widget');

// Прослушиватель для клика по иконке. Видимым делается окно с сообщениями
messageIcon.addEventListener('click', function() {
  messageIcon.style.animation = 'none';
  if (chatWindow.style.display === 'none') {
    chatWindow.style.display = 'block';
  } else {
    chatWindow.style.display = 'none';
  }
});

function checkUnreadMessages() {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_unread_messages_api");
  xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
          const responseText = xhr.responseText;
          if (responseText === "") {
            return;
          }
          const idsData = JSON.parse(responseText);
          console.log(idsData);
          // const messageIcon = document.getElementById('message-icon');
          messageIcon.classList.remove('hidden');
          let root = document.getElementById('chat_widget');
          let divChat = document.createElement('div');
          let ulChat = document.createElement('ul');
          ulChat.classList.add('contacts_widget');
          const unreadsChatIds = idsData.unread_chats_ids;
          delete idsData.unread_chats_ids;
          root.innerHTML = '';
          for (const userId in idsData) {
              const data = idsData[userId];
              const chatElem = `
                  <a href="${userId}/chat" class="chat-action">
                      <li class="user_widget" id="${userId}">
                          <div class="d-flex">
                              <div>
                                  <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_widget">
                              </div>
                              <div class="user_info_widget">
                                  <span>${data.username}</span>
                              </div>
                              <div class="msg_icon_widget">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-left-text" viewBox="0 0 16 16">
                                  <path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4.414A2 2 0 0 0 3 11.586l-2 2V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12.793a.5.5 0 0 0 .854.353l2.853-2.853A1 1 0 0 1 4.414 12H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                                  <path d="M3 3.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5M3 6a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 6m0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
                                </svg>
                              </div>
                          </div>
                      </li>
                  </a>
              `
              ulChat.innerHTML += chatElem;
              }
          divChat.appendChild(ulChat);
          console.log(unreadsChatIds);
          root.appendChild(divChat);
      }
  };
  xhr.send();
}

checkUnreadMessages();
setInterval(checkUnreadMessages, 100 * 1000);