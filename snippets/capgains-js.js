function calculateCapGains() {
  // ── Inputs ──
  const assetType = document.getElementById('cg-asset-type').value;
  const year = document.getElementById('cg-year').value;
  const province = document.getElementById('cg-province').value;
  const salePrice = parseFloat(document.getElementById('cg-sale-price').value) || 0;
  const acb = parseFloat(document.getElementById('cg-acb').value) || 0;
  const expenses = parseFloat(document.getElementById('cg-expenses').value) || 0;
  const otherGains = parseFloat(document.getElementById('cg-other-gains').value) || 0;
  const capitalLosses = parseFloat(document.getElementById('cg-capital-losses').value) || 0;
  const otherIncome = parseFloat(document.getElementById('cg-other-income').value) || 0;
  const applyLCGE = document.getElementById('cg-lcge').checked;
  const principalRes = document.getElementById('cg-principal-res').checked;

  // Show/hide LCGE based on asset type
  const lcgeGroup = document.getElementById('cg-lcge-group');
  const lcgeEligible = (assetType === 'business' || assetType === 'farm');
  lcgeGroup.style.display = lcgeEligible ? '' : 'none';

  // ── Capital Gain ──
  let capitalGain = salePrice - acb - expenses;
  if (principalRes) capitalGain = 0;
  if (capitalGain < 0) capitalGain = 0;

  // Apply losses
  let netGain = Math.max(0, capitalGain - capitalLosses);

  // LCGE
  let lcgeAmount = 0;
  if (applyLCGE && lcgeEligible && netGain > 0) {
    const lcgeLimit = (year === '2023') ? 971190 : (year === '2024') ? 1016836 : 1250000;
    lcgeAmount = Math.min(netGain, lcgeLimit);
    netGain = Math.max(0, netGain - lcgeAmount);
  }

  // Total gains for threshold
  const totalGains = netGain + otherGains;

  // ── Inclusion Rate Logic ──
  function calcTaxableGain(gain, totalForThreshold, useNewRules) {
    if (!useNewRules || year === '2023') {
      return gain * 0.5; // Old rules: flat 50%
    }
    // New rules (2024+): 50% on first $250K of total gains, 66.67% above
    if (totalForThreshold <= 250000) {
      return gain * 0.5;
    }
    // Portion of THIS gain that falls above $250K threshold
    const gainBelowThreshold = Math.max(0, 250000 - (totalForThreshold - gain));
    const gainAboveThreshold = gain - gainBelowThreshold;
    return (Math.max(0, gainBelowThreshold) * 0.5) + (Math.max(0, gainAboveThreshold) * 2 / 3);
  }

  const taxableGainNew = calcTaxableGain(netGain, totalGains, true);
  const taxableGainOld = calcTaxableGain(netGain, totalGains, false);

  // ── Federal Tax Brackets 2025/2026 ──
  const fedBrackets = [
    { limit: 57375, rate: 0.15 },
    { limit: 114750, rate: 0.205 },
    { limit: 158468, rate: 0.26 },
    { limit: 221708, rate: 0.29 },
    { limit: Infinity, rate: 0.33 }
  ];

  // ── Provincial Brackets (2025 values) ──
  const provBrackets = {
    AB: [
      { limit: 148269, rate: 0.10 },
      { limit: 177922, rate: 0.12 },
      { limit: 237230, rate: 0.13 },
      { limit: 355845, rate: 0.14 },
      { limit: Infinity, rate: 0.15 }
    ],
    BC: [
      { limit: 47937, rate: 0.0506 },
      { limit: 95875, rate: 0.077 },
      { limit: 110076, rate: 0.105 },
      { limit: 133664, rate: 0.1229 },
      { limit: 181232, rate: 0.147 },
      { limit: 252752, rate: 0.168 },
      { limit: Infinity, rate: 0.205 }
    ],
    MB: [
      { limit: 47000, rate: 0.108 },
      { limit: 100000, rate: 0.1275 },
      { limit: Infinity, rate: 0.174 }
    ],
    NB: [
      { limit: 49958, rate: 0.094 },
      { limit: 99916, rate: 0.14 },
      { limit: 185064, rate: 0.16 },
      { limit: Infinity, rate: 0.195 }
    ],
    NL: [
      { limit: 43198, rate: 0.087 },
      { limit: 86395, rate: 0.145 },
      { limit: 154244, rate: 0.158 },
      { limit: 215943, rate: 0.178 },
      { limit: 275870, rate: 0.198 },
      { limit: 551739, rate: 0.208 },
      { limit: 1103478, rate: 0.213 },
      { limit: Infinity, rate: 0.218 }
    ],
    NS: [
      { limit: 29590, rate: 0.0879 },
      { limit: 59180, rate: 0.1495 },
      { limit: 93000, rate: 0.1667 },
      { limit: 150000, rate: 0.175 },
      { limit: Infinity, rate: 0.21 }
    ],
    NT: [
      { limit: 50597, rate: 0.059 },
      { limit: 101198, rate: 0.086 },
      { limit: 164525, rate: 0.122 },
      { limit: Infinity, rate: 0.1405 }
    ],
    NU: [
      { limit: 53268, rate: 0.04 },
      { limit: 106537, rate: 0.07 },
      { limit: 173205, rate: 0.09 },
      { limit: Infinity, rate: 0.115 }
    ],
    ON: [
      { limit: 51446, rate: 0.0505 },
      { limit: 102894, rate: 0.0915 },
      { limit: 150000, rate: 0.1116 },
      { limit: 220000, rate: 0.1216 },
      { limit: Infinity, rate: 0.1316 }
    ],
    PE: [
      { limit: 32656, rate: 0.098 },
      { limit: 64313, rate: 0.138 },
      { limit: 105000, rate: 0.167 },
      { limit: 140000, rate: 0.175 },
      { limit: Infinity, rate: 0.1875 }
    ],
    QC: [
      { limit: 51780, rate: 0.14 },
      { limit: 103545, rate: 0.19 },
      { limit: 126000, rate: 0.24 },
      { limit: Infinity, rate: 0.2575 }
    ],
    SK: [
      { limit: 52057, rate: 0.105 },
      { limit: 148734, rate: 0.125 },
      { limit: Infinity, rate: 0.145 }
    ],
    YT: [
      { limit: 55867, rate: 0.064 },
      { limit: 111733, rate: 0.09 },
      { limit: 154906, rate: 0.109 },
      { limit: 500000, rate: 0.128 },
      { limit: Infinity, rate: 0.15 }
    ]
  };

  // ── Bracket Tax Calculator ──
  function calcBracketTax(brackets, taxableIncome) {
    let tax = 0;
    let prev = 0;
    for (const b of brackets) {
      if (taxableIncome <= prev) break;
      const amt = Math.min(taxableIncome, b.limit) - prev;
      tax += amt * b.rate;
      prev = b.limit;
    }
    return tax;
  }

  // Tax on other income alone
  const fedTaxBase = calcBracketTax(fedBrackets, otherIncome);
  const provTaxBase = calcBracketTax(provBrackets[province] || provBrackets.ON, otherIncome);

  // Tax on other income + taxable gain (new rules)
  const fedTaxTotalNew = calcBracketTax(fedBrackets, otherIncome + taxableGainNew);
  const provTaxTotalNew = calcBracketTax(provBrackets[province] || provBrackets.ON, otherIncome + taxableGainNew);
  const fedTaxOnGainNew = fedTaxTotalNew - fedTaxBase;
  const provTaxOnGainNew = provTaxTotalNew - provTaxBase;
  const totalTaxNew = fedTaxOnGainNew + provTaxOnGainNew;

  // Tax on other income + taxable gain (old rules)
  const fedTaxTotalOld = calcBracketTax(fedBrackets, otherIncome + taxableGainOld);
  const provTaxTotalOld = calcBracketTax(provBrackets[province] || provBrackets.ON, otherIncome + taxableGainOld);
  const fedTaxOnGainOld = fedTaxTotalOld - fedTaxBase;
  const provTaxOnGainOld = provTaxTotalOld - provTaxBase;
  const totalTaxOld = fedTaxOnGainOld + provTaxOnGainOld;

  const additionalTax = totalTaxNew - totalTaxOld;
  const effectiveRate = netGain > 0 ? (totalTaxNew / netGain * 100) : 0;
  const effectiveRateOld = netGain > 0 ? (totalTaxOld / netGain * 100) : 0;
  const netProceeds = salePrice - expenses - totalTaxNew;
  const inclusionRate = netGain > 0 ? (taxableGainNew / netGain * 100) : 50;

  // Determine which tax applies
  const isNewRules = (year !== '2023');
  const activeTax = isNewRules ? totalTaxNew : totalTaxOld;
  const activeFedTax = isNewRules ? fedTaxOnGainNew : fedTaxOnGainOld;
  const activeProvTax = isNewRules ? provTaxOnGainNew : provTaxOnGainOld;
  const activeTaxableGain = isNewRules ? taxableGainNew : taxableGainOld;
  const activeEffRate = isNewRules ? effectiveRate : effectiveRateOld;

  // ── Render Results ──
  const resultsEl = document.getElementById('cg-results');
  const showComparison = isNewRules && totalGains > 250000;

  resultsEl.innerHTML = `
    <div class="result-card glass-card" style="border-left: 4px solid var(--brand-success);">
      <div class="result-label">Capital Gain</div>
      <div class="result-value mono">${fmtFull(capitalGain)}</div>
    </div>
    ${lcgeAmount > 0 ? `
    <div class="result-card glass-card" style="border-left: 4px solid var(--brand-warning);">
      <div class="result-label">LCGE Applied</div>
      <div class="result-value mono">−${fmtFull(lcgeAmount)}</div>
    </div>` : ''}
    ${capitalLosses > 0 ? `
    <div class="result-card glass-card">
      <div class="result-label">Capital Losses Applied</div>
      <div class="result-value mono">−${fmtFull(Math.min(capitalLosses, capitalGain))}</div>
    </div>` : ''}
    <div class="result-card glass-card">
      <div class="result-label">Net Capital Gain</div>
      <div class="result-value mono">${fmtFull(netGain)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Effective Inclusion Rate</div>
      <div class="result-value mono">${inclusionRate.toFixed(1)}%</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Taxable Capital Gain</div>
      <div class="result-value mono">${fmtFull(activeTaxableGain)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Federal Tax on Gain</div>
      <div class="result-value mono">${fmtFull(activeFedTax)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Provincial Tax on Gain</div>
      <div class="result-value mono">${fmtFull(activeProvTax)}</div>
    </div>
    <div class="result-card glass-card" style="border-left: 4px solid var(--brand-danger);">
      <div class="result-label">Total Tax</div>
      <div class="result-value mono" style="font-size: 1.5rem;">${fmtFull(activeTax)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Effective Tax Rate on Gain</div>
      <div class="result-value mono">${activeEffRate.toFixed(1)}%</div>
    </div>
    <div class="result-card glass-card" style="border-left: 4px solid var(--brand-success);">
      <div class="result-label">Net Proceeds After Tax</div>
      <div class="result-value mono" style="font-size: 1.3rem;">${fmtFull(netProceeds)}</div>
    </div>
    ${showComparison ? `
    <div class="result-card glass-card" style="border-left: 4px solid var(--brand-warning); background: rgba(255,193,7,0.05);">
      <div class="result-label">⚠️ New Rules Impact</div>
      <div style="margin-top: 0.5rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
          <span style="color:var(--text-secondary);">Tax under old rules (50%)</span>
          <span class="mono">${fmtFull(totalTaxOld)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
          <span style="color:var(--text-secondary);">Tax under new rules</span>
          <span class="mono">${fmtFull(totalTaxNew)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding-top:0.5rem;border-top:1px solid var(--border-primary);">
          <span style="font-weight:600;color:var(--brand-danger);">Additional tax from new rules</span>
          <span class="mono" style="font-weight:700;color:var(--brand-danger);">+${fmtFull(additionalTax)}</span>
        </div>
      </div>
    </div>` : ''}
  `;

  // ── Breakdown Section ──
  const breakdownEl = document.getElementById('cg-breakdown');

  // Bar chart: old vs new inclusion
  const barChartHTML = (showComparison) ? `
    <div style="margin-bottom: 2rem;">
      <h3 style="margin-bottom: 1rem;">📊 Inclusion Rate Comparison</h3>
      <div style="display:flex;gap:1.5rem;align-items:flex-end;height:160px;padding:0 1rem;">
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;">
          <span class="mono" style="font-weight:600;margin-bottom:0.5rem;">${fmtFull(taxableGainOld)}</span>
          <div style="width:100%;background:var(--brand-success);border-radius:8px 8px 0 0;height:${Math.max(10, (taxableGainOld / Math.max(taxableGainNew, 1)) * 120)}px;transition:height 0.3s;"></div>
          <span style="margin-top:0.5rem;font-size:0.85rem;color:var(--text-secondary);">Old Rules (50%)</span>
        </div>
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;">
          <span class="mono" style="font-weight:600;margin-bottom:0.5rem;">${fmtFull(taxableGainNew)}</span>
          <div style="width:100%;background:var(--brand-warning);border-radius:8px 8px 0 0;height:120px;transition:height 0.3s;"></div>
          <span style="margin-top:0.5rem;font-size:0.85rem;color:var(--text-secondary);">New Rules</span>
        </div>
      </div>
    </div>` : '';

  // Donut chart
  const donutData = [
    { label: 'Federal Tax', value: activeFedTax, color: '#3b82f6' },
    { label: 'Provincial Tax', value: activeProvTax, color: '#8b5cf6' },
    { label: 'Net Proceeds', value: Math.max(0, salePrice - expenses - activeTax), color: '#22c55e' }
  ].filter(d => d.value > 0);

  const donutHTML = (netGain > 0 && typeof svgDonut === 'function')
    ? `<div style="margin-bottom:2rem;"><h3 style="margin-bottom:1rem;">🍩 Tax Breakdown</h3>${svgDonut(donutData, 220)}</div>`
    : '';

  // Waterfall chart
  const waterfallSteps = [
    { label: 'Sale Price', value: salePrice, type: 'add' },
    { label: 'Cost Base', value: -acb, type: 'sub' },
    { label: 'Expenses', value: -expenses, type: 'sub' },
    ...(capitalLosses > 0 ? [{ label: 'Losses', value: -Math.min(capitalLosses, capitalGain), type: 'sub' }] : []),
    ...(lcgeAmount > 0 ? [{ label: 'LCGE', value: -lcgeAmount, type: 'sub' }] : []),
    { label: 'Fed Tax', value: -activeFedTax, type: 'sub' },
    { label: 'Prov Tax', value: -activeProvTax, type: 'sub' },
    { label: 'Net', value: netProceeds, type: 'total' }
  ];

  const waterfallHTML = (netGain > 0 && typeof svgWaterfall === 'function')
    ? `<div style="margin-bottom:2rem;"><h3 style="margin-bottom:1rem;">📉 Proceeds Waterfall</h3>${svgWaterfall(waterfallSteps)}</div>`
    : '';

  // Strategies
  const strategies = [];
  if (!principalRes && assetType === 'real-estate')
    strategies.push('🏠 If this was ever your principal residence, the <strong>Principal Residence Exemption</strong> could eliminate the entire gain.');
  if (netGain > 250000 && isNewRules)
    strategies.push('📅 Consider splitting the sale across two tax years to keep each year under the $250K threshold and stay at the 50% inclusion rate.');
  if (!applyLCGE && lcgeEligible)
    strategies.push('🏢 Qualified small business shares may be eligible for the <strong>Lifetime Capital Gains Exemption</strong> ($1.25M for 2025+).');
  if (capitalLosses === 0)
    strategies.push('📉 Harvest capital losses from other investments to offset this gain. Losses can be carried back 3 years or forward indefinitely.');
  if (otherIncome > 100000)
    strategies.push('💰 Consider <strong>spousal attribution planning</strong> — transferring assets to a lower-income spouse (with proper documentation) can reduce the marginal rate.');
  strategies.push('🏦 Maximize RRSP contributions to reduce other taxable income and lower the marginal rate applied to your capital gain.');
  if (assetType === 'crypto')
    strategies.push('🪙 Ensure accurate ACB tracking for crypto — each trade, swap, and DeFi transaction can trigger a taxable event.');
  if (assetType === 'real-estate')
    strategies.push('📋 Don\'t forget to include renovation costs, legal fees, and land transfer taxes in your adjusted cost base.');

  const strategiesHTML = strategies.length > 0 ? `
    <div style="margin-top: 2rem;">
      <h3 style="margin-bottom: 1rem;">💡 Tax-Saving Strategies</h3>
      <div style="display: grid; gap: 0.75rem;">
        ${strategies.map(s => `<div style="padding: 0.75rem 1rem; background: var(--bg-secondary); border-radius: var(--radius-lg); border: 1px solid var(--border-primary); font-size: 0.95rem; line-height: 1.5;">${s}</div>`).join('')}
      </div>
    </div>` : '';

  breakdownEl.innerHTML = barChartHTML + donutHTML + waterfallHTML + strategiesHTML;

  if (!netGain && !capitalGain) {
    resultsEl.innerHTML = `
      <div class="result-card glass-card" style="text-align:center;padding:2rem;">
        <div style="font-size:2rem;margin-bottom:0.5rem;">✅</div>
        <div class="result-label">No Capital Gain</div>
        <p style="color:var(--text-secondary);margin-top:0.5rem;">
          ${principalRes ? 'Principal Residence Exemption eliminates the entire gain.' : 'The sale price does not exceed your cost base and expenses.'}
        </p>
      </div>`;
    breakdownEl.innerHTML = '';
  }
}

// Auto-calculate on load
if (document.getElementById('cg-sale-price')) calculateCapGains();
