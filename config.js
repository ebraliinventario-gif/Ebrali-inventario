(function configureApiBase() {
  const LOCAL_FLASK = "http://localhost:3000";
  const LOCAL_FASTAPI = "http://localhost:8000";
  const DEFAULT_PROD = "https://ebrali-inventario.onrender.com";

  const hostname = window.location.hostname || "";
  const protocol = window.location.protocol;
  const runningFromFile = protocol === "file:";
  const isLocalHost = ["localhost", "127.0.0.1", ""].includes(hostname);

  // Quando abrir o index.html diretamente (file://) ou via localhost, usamos o Flask local (porta 3000).
  // Ainda deixamos exposto o endpoint FastAPI (porta 8000) para quem estiver testando essa variante.
  const apiBaseUrl = runningFromFile || isLocalHost ? LOCAL_FLASK : DEFAULT_PROD;

  window.APP_CONFIG = {
    apiBaseUrl,
    flaskApiUrl: LOCAL_FLASK,
    fastApiUrl: LOCAL_FASTAPI,
    prodApiUrl: DEFAULT_PROD,
  };
})();
