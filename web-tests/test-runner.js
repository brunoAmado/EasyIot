const { chromium, devices } = require('playwright');
const { startServer, stopServer } = require('./mock-server');
const http = require('http');

// Helper to fetch request logs from mock server
async function getLogs() {
  const res = await fetch('http://localhost:3000/test/logs');
  return res.json();
}

async function resetLogs() {
  await fetch('http://localhost:3000/test/reset-logs', { method: 'POST' });
}

async function resetAll() {
  await fetch('http://localhost:3000/test/reset-all', { method: 'POST' });
}

async function runTests() {
  let browser;
  try {
    // 1. Start Mock Server
    const url = await startServer(3000);

    // 2. Launch headless browser
    browser = await chromium.launch({ headless: true });

    // Devices list to test (Desktop, iPhone, and Android)
    const devicesToTest = [
      { name: 'Desktop Chrome', use: {} },
      { name: 'iPhone 13 (iOS)', use: devices['iPhone 13'] },
      { name: 'Pixel 5 (Android)', use: devices['Pixel 5'] }
    ];

    for (const dev of devicesToTest) {
      console.log(`\n[TEST] Running E2E Suite on device: ${dev.name}...`);
      
      // Reset the mock server state before each run
      await resetAll();
      
      // Create a context emulating the device configurations (viewport, user agent)
      const context = await browser.newContext(dev.use);
      const page = await context.newPage();
      page.on('console', msg => console.log(`    [BROWSER CONSOLE] ${msg.text()}`));
      page.on('pageerror', err => console.error(`    [BROWSER ERROR] ${err.message}`));

      console.log(`  -> Navigating to Web Panel on ${dev.name}...`);
      await page.goto(url);
      await page.waitForLoadState('load');
      await page.waitForSelector('#node-btn', { timeout: 10000 });

      // SCENARIO 1: Verify Initial Config Load
      console.log('  -> Verifying initial configuration populated in UI...');
      await page.click('#node-btn'); // Switch to system tab
      const nodeIdVal = await page.inputValue('#nodeId');
      const wifiSSIDVal = await page.inputValue('#wifiSSID');
      const mqttIpVal = await page.inputValue('#mqttIpDns');
      
      if (nodeIdVal !== 'test-node' || wifiSSIDVal !== 'Home_WiFi' || mqttIpVal !== '192.168.1.10') {
        throw new Error(`Config mismatch in UI on ${dev.name}: nodeId=${nodeIdVal}, wifiSSID=${wifiSSIDVal}`);
      }

      // SCENARIO 2: Change Config and Save
      console.log('  -> Modifying System Configuration...');
      // Make nodeId safe for URL params mapping
      const safeNodeId = `Living-Room-${dev.name.replace(/[^a-zA-Z0-9]/g, '-')}`;
      await page.fill('#nodeId', safeNodeId);
      await page.fill('#wifiSSID', 'My_New_WiFi');
      await page.fill('#mqttIpDns', '192.168.1.50');
      
      await resetLogs();
      console.log('  -> Saving changes...');
      await page.click('.btl-save-all');
      await page.waitForTimeout(500); // Wait for request to complete

      const saveLogs = await getLogs();
      const configSaveRequest = saveLogs.find(l => l.path === '/config' && l.method === 'POST');
      if (!configSaveRequest) {
        throw new Error(`No POST /config request recorded on ${dev.name}`);
      }
      if (configSaveRequest.body.nodeId !== safeNodeId || configSaveRequest.body.wifiSSID !== 'My_New_WiFi') {
        throw new Error(`Save payload mismatch on ${dev.name}: ${JSON.stringify(configSaveRequest.body)}`);
      }

      // SCENARIO 3: Open Wizard and Add Virtual Feature
      console.log('  -> Opening Wizard and adding virtual feature...');
      await page.click('#features-btn'); // Open features tab
      await page.click('.btn-add'); // Click "+" button to open wizard
      await page.waitForSelector('#wizard', { state: 'visible' });

      await page.fill('#f-n-name', `Luz ${dev.name}`);
      await page.selectOption('#f-n-driver', { value: '7' }); // Driver 7: Iluminação Pulsador Virtual
      
      await resetLogs();
      await page.click('#btn-create'); // Click ADD button
      await page.waitForTimeout(500);

      const featureLogs = await getLogs();
      const addFeatureRequest = featureLogs.find(l => l.path === '/features' && l.method === 'POST');
      if (!addFeatureRequest) {
        throw new Error(`No POST /features request recorded on ${dev.name}`);
      }
      if (addFeatureRequest.body.name !== `Luz ${dev.name}` || parseInt(addFeatureRequest.body.driver) !== 7) {
        throw new Error(`Add feature payload mismatch on ${dev.name}: ${JSON.stringify(addFeatureRequest.body)}`);
      }

      // SCENARIO 4: Reboot system
      console.log('  -> Triggering system reboot...');
      await page.click('#node-btn'); // Back to system tab
      await resetLogs();
      
      // Listen for dialog reboot confirmation box and accept it
      page.once('dialog', dialog => dialog.accept());
      await page.click('button[onclick="reboot()"]');
      await page.waitForTimeout(500);

      const rebootLogs = await getLogs();
      const rebootRequest = rebootLogs.find(l => l.path === '/reboot');
      if (!rebootRequest) {
        throw new Error(`No /reboot request recorded on ${dev.name}`);
      }

      await context.close();
      console.log(`[SUCCESS] E2E Suite passed on device: ${dev.name}`);
    }

    console.log('\n[SUCCESS] All multi-device Web E2E Integration tests passed successfully!');
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
