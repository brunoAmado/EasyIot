const { chromium } = require('playwright');
const { startServer, stopServer, getConfig } = require('./mock-server');
const http = require('http');

// Helper to fetch request logs from mock server
function getLogs() {
  return new Promise((resolve) => {
    http.get('http://localhost:3000/test/logs', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    });
  });
}

function resetLogs() {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: 'localhost',
      port: 3000,
      path: '/test/reset-logs',
      method: 'POST'
    }, (res) => {
      res.on('end', resolve);
    });
    req.end();
  });
}

async function runTests() {
  let browser;
  try {
    // 1. Start Mock Server
    const url = await startServer(3000);

    // 2. Launch headless browser
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    console.log('[TEST] Navigating to Web Panel...');
    await page.goto(url);
    await page.waitForLoadState('networkidle');

    // SCENARIO 1: Verify Initial Config Load
    console.log('[TEST] Verifying initial configuration populated in UI...');
    await page.click('#node-btn'); // Switch to system tab
    const nodeIdVal = await page.inputValue('#nodeId');
    const wifiSSIDVal = await page.inputValue('#wifiSSID');
    const mqttIpVal = await page.inputValue('#mqttIpDns');
    
    if (nodeIdVal !== 'test-node' || wifiSSIDVal !== 'Home_WiFi' || mqttIpVal !== '192.168.1.10') {
      throw new Error(`Config mismatch in UI: nodeId=${nodeIdVal}, wifiSSID=${wifiSSIDVal}, mqttIpDns=${mqttIpVal}`);
    }
    console.log('  -> Initial config load verified successfully.');

    // SCENARIO 2: Change Config and Save
    console.log('[TEST] Modifying System Configuration...');
    await page.fill('#nodeId', 'Living-Room-Module');
    await page.fill('#wifiSSID', 'My_New_WiFi');
    await page.fill('#mqttIpDns', '192.168.1.50');
    
    // Clear logs and save
    await resetLogs();
    console.log('[TEST] Saving changes...');
    await page.click('.btl-save-all');
    await page.waitForTimeout(500); // Wait for request to complete

    const saveLogs = await getLogs();
    const configSaveRequest = saveLogs.find(l => l.path === '/config' && l.method === 'POST');
    if (!configSaveRequest) {
      throw new Error('No POST /config request recorded on server.');
    }
    if (configSaveRequest.body.nodeId !== 'Living-Room-Module' || configSaveRequest.body.wifiSSID !== 'My_New_WiFi') {
      throw new Error(`Save payload mismatch: ${JSON.stringify(configSaveRequest.body)}`);
    }
    console.log('  -> Configuration save payload verified successfully.');

    // SCENARIO 3: Open Wizard and Add Virtual Feature
    console.log('[TEST] Navigating to Features tab and opening Wizard...');
    await page.click('#features-btn'); // Open features tab
    await page.click('.btn-add'); // Click "+" button to open wizard
    await page.waitForSelector('#wizard', { state: 'visible' });

    console.log('[TEST] Adding new Virtual Light feature...');
    await page.fill('#f-n-name', 'Sala de Estar');
    await page.selectOption('#f-n-driver', { value: '7' }); // Driver 7: Iluminação Pulsador Virtual
    
    await resetLogs();
    await page.click('#btn-create'); // Click ADD button
    await page.waitForTimeout(500);

    const featureLogs = await getLogs();
    const addFeatureRequest = featureLogs.find(l => l.path === '/features/add' && l.method === 'POST');
    if (!addFeatureRequest) {
      throw new Error('No POST /features/add request recorded on server.');
    }
    if (addFeatureRequest.body.name !== 'Sala de Estar' || addFeatureRequest.body.driver !== '7') {
      throw new Error(`Add feature payload mismatch: ${JSON.stringify(addFeatureRequest.body)}`);
    }
    console.log('  -> Virtual feature creation payload verified successfully.');

    // SCENARIO 4: Reboot system
    console.log('[TEST] Triggering system Reboot...');
    await page.click('#node-btn'); // Back to system tab
    await resetLogs();
    
    // Listen for dialog reboot confirmation box and accept it
    page.once('dialog', dialog => dialog.accept());
    await page.click('button:has-text("Reiniciar")');
    await page.waitForTimeout(500);

    const rebootLogs = await getLogs();
    const rebootRequest = rebootLogs.find(l => l.path === '/reboot' && l.method === 'POST');
    if (!rebootRequest) {
      throw new Error('No POST /reboot request recorded on server.');
    }
    console.log('  -> System reboot request verified successfully.');

    console.log('\n[SUCCESS] All Web E2E Integration tests passed successfully!');
    stopServer();
    if (browser) await browser.close();
    process.exit(0);

  } catch (error) {
    console.error('\n[FAILED] E2E Integration test failed:');
    console.error(error.message);
    stopServer();
    if (browser) await browser.close();
    process.exit(1);
  }
}

runTests();
