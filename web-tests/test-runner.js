const { chromium, devices } = require('playwright');
const { startServer, stopServer } = require('./mock-server');

async function getLogs() {
  const res = await fetch('http://localhost:3000/test/logs');
  return res.json();
}

async function resetAll() {
  await fetch('http://localhost:3000/test/reset-all', { method: 'POST' });
}

async function runTests() {
  let browser;
  try {
    const url = await startServer(3000);
    browser = await chromium.launch({ headless: true });

    const devicesToTest = [
      { name: 'Desktop Chrome', use: {} },
      { name: 'Pixel 5 (Mobile)', use: devices['Pixel 5'] }
    ];

    for (const dev of devicesToTest) {
      console.log(`\n[TEST] Running E2E Suite on device: ${dev.name}...`);
      await resetAll();

      const context = await browser.newContext(dev.use);
      const page = await context.newPage();
      page.on('console', msg => console.log(`    [BROWSER CONSOLE] ${msg.text()}`));
      page.on('pageerror', err => console.error(`    [BROWSER ERROR] ${err.message}`));

      console.log(`  -> Navigating to Web Panel on ${dev.name}...`);
      await page.goto(url);
      await page.waitForLoadState('networkidle');

      // 1. Verify Top Navigation Tabs exist
      console.log('  -> Verifying navigation tabs...');
      await page.waitForSelector('.tabs', { timeout: 10000 });
      await page.waitForSelector('button[data-view="overview"]');
      await page.waitForSelector('button[data-view="system"]');
      await page.waitForSelector('button[data-view="features"]');

      // 2. Switch to System Tab and Verify Config Form
      console.log('  -> Verifying System configuration tab...');
      await page.click('button[data-view="system"]');
      await page.waitForSelector('#nodeId', { state: 'visible' });

      const nodeIdVal = await page.inputValue('#nodeId');
      const wifiSSIDVal = await page.inputValue('#wifiSSID');
      if (nodeIdVal !== 'test-node' || wifiSSIDVal !== 'Home_WiFi') {
        throw new Error(`Config mismatch in UI on ${dev.name}: nodeId=${nodeIdVal}, wifiSSID=${wifiSSIDVal}`);
      }

      // 3. Switch to Features Tab
      console.log('  -> Verifying Features tab...');
      await page.click('button[data-view="features"]');
      await page.waitForSelector('#v-features', { state: 'visible' });

      // 4. Switch to AquaDance Tab (under Irrigation)
      console.log('  -> Verifying AquaDance / Fontaine mode...');
      await page.click('button[data-view="irrigation"]');
      await page.waitForSelector('#v-irrigation', { state: 'visible' });

      // Click sub-tab for AquaDance if present
      const aquadanceBtn = await page.$('button[data-subview="aquadance"]');
      if (aquadanceBtn) {
        await aquadanceBtn.click();
        await page.waitForSelector('#aquadance-canvas', { state: 'visible' });
        console.log('  -> 2D Basin Canvas loaded successfully!');
      }

      await context.close();
      console.log(`[SUCCESS] E2E Suite passed on device: ${dev.name}`);
    }

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
