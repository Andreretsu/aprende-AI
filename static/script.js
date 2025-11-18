document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btn-gravar");
  const btnTexto = document.getElementById("btn-texto");
  const statusTexto = document.getElementById("status-texto");
  const resultadoContainer = document.getElementById("resultado-container");
  const textoOuvido = document.getElementById("texto-ouvido");
  const mensagemFeedback = document.getElementById("mensagem-feedback");

  let mediaRecorder;
  let audioChunks = [];

  // --- NOVA FUNÇÃO: O NAVEGADOR FALA! 🗣️ ---
  function falarTexto(texto) {
    // Cancela se já estiver falando algo
    window.speechSynthesis.cancel();

    const sentenca = new SpeechSynthesisUtterance(texto);
    sentenca.lang = "pt-BR"; // Importante para não falar com sotaque gringo
    sentenca.rate = 1.8; // Velocidade (1 é normal, 1.2 é um pouco mais dinâmico)
    sentenca.pitch = 1; // Tom de voz

    window.speechSynthesis.speak(sentenca);
  }
  // -------------------------------------------

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = enviarAudio;
      })
      .catch((err) => {
        console.error("Erro:", err);
        statusTexto.innerText = "Erro: Microfone bloqueado!";
      });
  }

  const iniciarGravacao = (e) => {
    e.preventDefault();
    if (!mediaRecorder || mediaRecorder.state === "recording") return;

    // Para a voz da IA se ela estiver falando quando você for gravar
    window.speechSynthesis.cancel();

    audioChunks = [];
    mediaRecorder.start();

    btn.classList.add("gravando");
    btnTexto.innerText = "Ouvindo...";
    statusTexto.innerText = "Estou te ouvindo...";
    resultadoContainer.classList.add("hidden");
  };

  const pararGravacao = (e) => {
    e.preventDefault();
    if (!mediaRecorder || mediaRecorder.state === "inactive") return;

    mediaRecorder.stop();

    btn.classList.remove("gravando");
    btnTexto.innerText = "Segure para Gravar";
    statusTexto.innerText = "Enviando para o Tutor...";
  };

  btn.addEventListener("mousedown", iniciarGravacao);
  btn.addEventListener("mouseup", pararGravacao);
  btn.addEventListener("touchstart", iniciarGravacao);
  btn.addEventListener("touchend", pararGravacao);

  function enviarAudio() {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("audio_data", audioBlob, "gravacao.wav");

    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("/processar-audio/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        textoOuvido.innerText = `Você disse: "${data.texto}"`;
        mensagemFeedback.innerText = data.mensagem;

        statusTexto.innerText = "Resposta recebida!";
        resultadoContainer.classList.remove("hidden");

        // 👇 AQUI ESTÁ A MÁGICA! 👇
        // Assim que o texto chega, a gente manda ler
        if (data.mensagem) {
          falarTexto(data.mensagem);
        }
      })
      .catch((erro) => {
        console.error("Erro:", erro);
        statusTexto.innerText = "Erro ao conectar.";
      });
  }
});
