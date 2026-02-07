import { test, expect } from '@playwright/test';

test('ABRISK Conference UI Smoke Test', async ({ page }) => {
    // 1. Navigate to Mechanism Console
    await page.goto('http://localhost:3000/console/mechanism');

    // 2. Verify Page Title/Header
    await expect(page).toHaveTitle(/ABRISK/);

    // 3. Locate Mutation Impact Card
    const mutationCard = page.locator('text=Mutation Functional Impact');
    await expect(mutationCard).toBeVisible();

    // 4. Verify Dropdown Loading
    // Should initially show "Select a precomputed mutation variant"
    // Assuming NDM-1 is the default or we need to select it.
    // The card takes 'determinant' as prop. If the page defaults to NDM-1, it should load.
    // Note: We might need to select NDM-1 in a gene search box if it's not default.
    // Assuming the page handles a default or we simulate selection.

    // For this test, we assume the page state allows finding the select.
    const dropdown = page.locator('select');
    await expect(dropdown).toBeVisible();

    // 5. Select H122Y
    await dropdown.selectOption({ label: 'H122Y' });

    // 6. Click Run Impact Score
    const runBtn = page.locator('button:has-text("Run Impact Score")');
    await expect(runBtn).toBeEnabled();
    await runBtn.click();

    // 7. Verify Result
    await expect(page.locator('text=Impact score reflects embedding-space functional shift')).toBeVisible({ timeout: 10000 });

    // 8. Verify Structure Viewer Highlight
    // This is harder to verify structurally, but we can check if the canvas exists
    await expect(page.locator('canvas')).toBeVisible();

    console.log('Smoke Test Passed');
});
