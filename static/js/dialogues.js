document.addEventListener('DOMContentLoaded', ()=>{
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  document.querySelector('#send-message').onclick = ()=>{
    const text = document.querySelector('#message').value;
    socket.send(text);
    document.querySelector('#message').value = '';
  }
  socket.on('connect', (data)=>{
    if (data){
      for (message in data.messages){
        document.querySelector('#messages-field').append('1')
      }
  }
  })
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
