const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static webpanel assets from the root webpanel folder
app.use('/', express.static(path.join(__dirname, '../webpanel')));

// Initial mockup configuration matching ConfigOnofre structure
let config = {
  nodeId: "test-node",
  chipId: "123456",
  wifiSSID: "Home_WiFi",
  wifiSecret: "hide_password",
  dhcp: true,
  wifiIp: "192.168.1.100",
  wifiMask: "255.255.255.0",
  wifiGw: "192.168.1.254",
  mqttIpDns: "192.168.1.10",
  mqttPort: 1883,
  mqttUsername: "admin",
  mqttPassword: "hide_password",
  features: [
    {
      group: "ACTUATOR",
      driver: 1, // LIGHT_PUSH
      id: "light1",
      name: "Cozinha",
      typeControl: 0,
      state: 0,
      inputs: [12],
      outputs: [13]
    }
  ]
};

// Requests log so the test runner can verify actions
let requestsLog = [];

app.use((req, res, next) => {
  if (req.path !== '/config' || req.method !== 'GET') {
    requestsLog.push({
      method: req.method,
      path: req.path,
      body: req.body,
      query: req.query
    });
  }
  next();
});

// REST API Endpoints
app.get('/config', (req, res) => {
  res.json(config);
});

app.post('/config', (req, res) => {
  config = { ...config, ...req.body };
  res.json({ status: "success", config });
});

app.post('/reboot', (req, res) => {
  res.json({ status: "rebooting" });
});

app.post('/load-defaults', (req, res) => {
  config.features = [];
  res.json({ status: "defaults_loaded" });
});

app.post('/templates/change', (req, res) => {
  res.json({ status: "template_changed" });
});

app.post('/features/add', (req, res) => {
  const newFeature = {
    id: req.body.id || `feature_${Date.now()}`,
    name: req.body.name,
    driver: parseInt(req.body.driver),
    group: parseInt(req.body.driver) >= 60 ? "SENSOR" : "ACTUATOR",
    inputs: req.body.inputs ? req.body.inputs.split(',').map(Number) : [],
    outputs: req.body.outputs ? req.body.outputs.split(',').map(Number) : [],
    state: 0
  };
  config.features.push(newFeature);
  res.json({ status: "added", features: config.features });
});

app.post('/features/delete', (req, res) => {
  const { id } = req.body;
  config.features = config.features.filter(f => f.id !== id);
  res.json({ status: "deleted", features: config.features });
});

// Endpoint to retrieve request logs for test validation
app.get('/test/logs', (req, res) => {
  res.json(requestsLog);
});

app.post('/test/reset-logs', (req, res) => {
  requestsLog = [];
  res.json({ status: "logs_reset" });
});

let server;
function startServer(port = 3000) {
  return new Promise((resolve) => {
    server = app.listen(port, () => {
      console.log(`[MOCK] ESP WebServer running at http://localhost:${port}`);
      resolve(`http://localhost:${port}`);
    });
  });
}

function stopServer() {
  if (server) {
    server.close();
    console.log('[MOCK] Server stopped.');
  }
}

module.exports = { startServer, stopServer, getConfig: () => config };
