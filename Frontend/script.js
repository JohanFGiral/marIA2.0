const espacioChat = document.querySelector('.espacio-de-chat'); 
const btnMicro  = document.getElementById('btn-micro');     

function loaderHTML() {
  return `
    <div class="puntos-carga" aria-hidden="true">
      <span></span><span></span><span></span>
    </div>
  `;
}

function reproducirAudio(url) {
  setTimeout(() => {
    try {
      const audio = new Audio(url);
      audio.play().catch(err => 
        console.warn("No se pudo reproducir audio automáticamente:", err)
      );
      audio.onended = () => {
        audio.src = ""; // libera memoria
      };
    } catch (e) {
      console.error("Error creando audio:", e);
    }
  }, 2000);
}


function crearMensajeOptimista() {
  const nuevoMensaje = document.createElement('div');
  nuevoMensaje.classList.add('message', 'mensaje-usuario'); 
  nuevoMensaje.innerHTML = loaderHTML();

  espacioChat.appendChild(nuevoMensaje);
  espacioChat.scrollTop = espacioChat.scrollHeight;

  return nuevoMensaje;
}

function crearMensajeBot(texto) {
  const nuevoMensaje = document.createElement('div');
  nuevoMensaje.classList.add('message', 'mensaje-bot'); 
  nuevoMensaje.textContent = texto;

  espacioChat.appendChild(nuevoMensaje);
  espacioChat.scrollTop = espacioChat.scrollHeight;
}

// 🎙️ SPEECHRECOGNITION
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = "es-ES";
recognition.continuous = false;
recognition.interimResults = false;

let timeoutSeguridad = null;

btnMicro.addEventListener('click', (e) => {
  e.preventDefault();
  btnMicro.disabled = true;

  const burbuja = crearMensajeOptimista();
  recognition._burbujaActual = burbuja;

  timeoutSeguridad = setTimeout(() => {
    if (burbuja.innerHTML.includes("puntos-carga")) {
      burbuja.innerHTML = "❗ No se detectó audio. Intenta de nuevo.";
      btnMicro.disabled = false;
      recognition.stop();
    }
  }, 6000);

  recognition.start();
});

recognition.onstart = () => {
  console.log("Grabando...");
};

recognition.onresult = (event) => {
  const texto = event.results[0][0].transcript;
  const burbuja = recognition._burbujaActual;

  if (burbuja) {
    burbuja.textContent = texto;
  }

  clearTimeout(timeoutSeguridad);

  // 🔥 ENVIAR AL BACKEND
  fetch("http://127.0.0.1:5000/send", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ mensaje: texto })
  })
  .then(async res => {
    const data = await res.json();

    crearMensajeBot(data.respuesta);

    if (data.audio_url) {
      reproducirAudio(data.audio_url + "?t=" + Date.now());
    }
  })
  .catch(() => {
    crearMensajeBot("⚠️ Error enviando al servidor.");
  });
};

recognition.onend = () => {
  console.log("Grabación terminada");

  const burbuja = recognition._burbujaActual;

  if (burbuja && burbuja.innerHTML.includes("puntos-carga")) {
    burbuja.innerHTML = "❗ No se escuchó nada.";
  }

  clearTimeout(timeoutSeguridad);
  btnMicro.disabled = false;
};

recognition.onerror = (event) => {
  console.warn("Error:", event.error);

  const burbuja = recognition._burbujaActual;

  if (burbuja) {
    burbuja.innerHTML = "⚠️ Error con el micrófono.";
  }

  clearTimeout(timeoutSeguridad);
  btnMicro.disabled = false;
  recognition.stop();
};
