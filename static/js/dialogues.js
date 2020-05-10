document.addEventListener('DOMContentLoaded', ()=>{
  if (typeof messages !== 'undefined') {
  console.log('exist')
  messages.forEach(message => {
    const p = document.createElement('p');
    const br = document.createElement('br');
    const span_username = document.createElement('span');
    const time_span = document.createElement('span');
    span_username.innerHTML = message['username'];
    time_span.innerHTML = message['time'];
    p.innerHTML = span_username.outerHTML+ br.outerHTML +time_span.outerHTML + br.outerHTML +message['text'];
    document.querySelector('#messages-field').append(p);
  })
} else {
  console.log('not exist')
}
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  document.querySelector('#send-message').onclick = ()=>{
    const text = document.querySelector('#message').value;
    socket.send(text);
    document.querySelector('#message').value = '';
  }

  socket.on('message', data => {
    const p = document.createElement('p');
    const br = document.createElement('br');
    const span_username = document.createElement('span');
    const time_span = document.createElement('span');
    span_username.innerHTML = data.username;
    time_span.innerHTML = data.time;
    p.innerHTML = span_username.outerHTML+ br.outerHTML +time_span.outerHTML + br.outerHTML +data.message;

    document.querySelector('#messages-field').append(p);
  })
})
