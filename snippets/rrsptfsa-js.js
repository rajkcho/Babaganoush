function calculateRRSPvsTFSA() {
  // ── Inputs ──
  const age = parseInt(document.getElementById('rvt-age').value) || 30;
  const retireAge = parseInt(document.getElementById('rvt-retire-age').value) || 65;
  const income = parseFloat(document.getElementById('rvt-income').value) || 0;
  const province = document.getElementById('rvt-province').value;
  const retireIncome = parseFloat(document.getElementById('rvt-retire-income').value) || 0;
  const contribution = parseFloat(document.getElementById('rvt-contribution').value) || 0;
  const returnRate = (parseFloat(document.getElementById('rvt-return').value) || 6) / 100;
  const inflation = (parseFloat(document.getElementById('rvt-inflation').value) ?? 2) / 100;
  const years = Math.max(1, retireAge - age);

  // ── 2026 Federal Tax Brackets ──
  const federalBrackets = [
    { max: 57375, rate: 0.15 },
    { max: 114750, rate: 0.205 },
    { max: 158468, rate: 0.26 },
    { max: 220000, rate: 0.29 },
    { max: Infinity, rate: 0.33 }
  ];

  // ── 2026 Provincial/Territorial Tax Brackets ──
  const provincialBrackets = {
    AB: [
      { max: 148269, rate: 0.10 },
      { max: 177922, rate: 0.12 },
      { max: 237230, rate: 0.13 },
      { max: 355845, rate: 0.14 },
      { max: Infinity, rate: 0.15 }
    ],
    BC: [
      { max: 47937, rate: 0.0506 },
      { max: 95875, rate: 0.077 },
      { max: 110076, rate: 0.105 },
      { max: 133664, rate: 0.1229 },
      { max: 181232, rate: 0.147 },
      { max: 252752, rate: 0.168 },
      { max: Infinity, rate: 0.205 }
    ],
    MB: [
      { max: 47000, rate: 0.108 },
      { max: 100000, rate: 0.1275 },
      { max: Infinity, rate: 0.174 }
    ],
    NB: [
      { max: 49958, rate: 0.094 },
      { max: 99916, rate: 0.14 },
      { max: 185064, rate: 0.16 },
      { max: Infinity, rate: 0.195 }
    ],
    NL: [
      { max: 43198, rate: 0.087 },
      { max: 86395, rate: 0.145 },
      { max: 154244, rate: 0.158 },
      { max: 215943, rate: 0.178 },
      { max: 275870, rate: 0.198 },
      { max: 551739, rate: 0.208 },
      { max: 1103478, rate: 0.213 },
      { max: Infinity, rate: 0.218 }
    ],
    NS: [
      { max: 29590, rate: 0.0879 },
      { max: 59180, rate: 0.1495 },
      { max: 93000, rate: 0.1667 },
      { max: 150000, rate: 0.175 },
      { max: Infinity, rate: 0.21 }
    ],
    NT: [
      { max: 50597, rate: 0.059 },
      { max: 101198, rate: 0.086 },
      { max: 164525, rate: 0.122 },
      { max: Infinity, rate: 0.1405 }
    ],
    NU: [
      { max: 53268, rate: 0.04 },
      { max: 106537, rate: 0.07 },
      { max: 173205, rate: 0.09 },
      { max: Infinity, rate: 0.115 }
    ],
    ON: [
      { max: 51446, rate: 0.0505 },
      { max: 102894, rate: 0.0915 },
      { max: 150000, rate: 0.1116 },
      { max: 220000, rate: 0.1216 },
      { max: Infinity, rate: 0.1316 }
    ],
    PE: [
      { max: 32656, rate: 0.095 },
      { max: 64313, rate: 0.1347 },
      { max: 105000, rate: 0.166 },
      { max: 140000, rate: 0.176 },
      { max: Infinity, rate: 0.19 }
    ],
    QC: [
      { max: 51780, rate: 0.14 },
      { max: 103545, rate: 0.19 },
      { max: 126000, rate: 0.24 },
      { max: Infinity, rate: 0.2575 }
    ],
    SK: [
      { max: 52057, rate: 0.105 },
      { max: 148734, rate: 0.125 },
      { max: Infinity, rate: 0.145 }
    ],
    YT: [
      { max: 57375, rate: 0.064 },
      { max: 114750, rate: 0.09 },
      { max: 158468, rate: 0.109 },
      { max: 220000, rate: 0.128 },
      { max: 500000, rate: 0.15 },
      { max: Infinity, rate: 0.15 }
    ]
  };

  // ── Tax calculation helpers ──
  function calcTaxOnIncome(taxableIncome, brackets) {
    let tax = 0, prev = 0;
    for (const b of brackets) {
      if (taxableIncome <= prev) break;
      const taxable = Math.min(taxableIncome, b.max) - prev;
      tax += taxable * b.rate;
      prev = b.max;
    }
    return tax;
  }

  function combinedTax(taxableIncome, prov) {
    return calcTaxOnIncome(taxableIncome, federalBrackets) +
           calcTaxOnIncome(taxableIncome, provincialBrackets[prov] || provincialBrackets.ON);
  }

  function marginalRate(taxableIncome, prov) {
    // Marginal rate = combined rate at this income level
    let fedRate = 0, provRate = 0, prev = 0;
    for (const b of federalBrackets) {
      if (taxableIncome <= b.max) { fedRate = b.rate; break; }
      prev = b.max;
    }
    prev = 0;
    const provBr = provincialBrackets[prov] || provincialBrackets.ON;
    for (const b of provBr) {
      if (taxableIncome <= b.max) { provRate = b.rate; break; }
      prev = b.max;
    }
    return fedRate + provRate;
  }

  // ── Core calculation ──
  const currentMarginal = marginalRate(income, province);
  const retireMarginal = marginalRate(retireIncome, province);

  // RRSP: contribution is tax-deductible. Refund = contribution × marginal rate. Refund is reinvested.
  // At retirement, full withdrawal is taxed at retirement marginal rate.
  const rrspRefundPerYear = contribution * currentMarginal;
  const rrspTotalContribPerYear = contribution + rrspRefundPerYear; // contribution + reinvested refund

  // TFSA: contribution from after-tax dollars. No tax on withdrawal.
  const tfsaContribPerYear = contribution; // same dollar amount contributed

  // Project growth year by year
  const rrspGrowth = []; // nominal balances
  const tfsaGrowth = [];
  let rrspBal = 0, tfsaBal = 0;
  let totalRRSPContrib = 0, totalTFSAContrib = 0;
  let totalRefundReinvested = 0;

  for (let y = 0; y < years; y++) {
    // Contribute at start of year, grow for the year
    rrspBal = (rrspBal + rrspTotalContribPerYear) * (1 + returnRate);
    tfsaBal = (tfsaBal + tfsaContribPerYear) * (1 + returnRate);
    totalRRSPContrib += rrspTotalContribPerYear;
    totalTFSAContrib += tfsaContribPerYear;
    totalRefundReinvested += rrspRefundPerYear;
    rrspGrowth.push(rrspBal);
    tfsaGrowth.push(tfsaBal);
  }

  // ── Final values ──
  const inflationFactor = Math.pow(1 + inflation, years);
  const rrspNominal = rrspBal;
  const tfsaNominal = tfsaBal;
  const rrspReal = rrspNominal / inflationFactor;
  const tfsaReal = tfsaNominal / inflationFactor;

  // Tax on RRSP withdrawal (effective tax on full amount at retirement income level)
  const rrspWithdrawalTax = rrspNominal * retireMarginal;
  const rrspAfterTax = rrspNominal - rrspWithdrawalTax;

  // TFSA: tax was already paid upfront on contributions
  // The "tax paid" for TFSA is the opportunity cost — the tax on original contributions
  const tfsaTaxPaidUpfront = contribution * years * currentMarginal;
  const tfsaAfterTax = tfsaNominal; // no withdrawal tax

  // Total lifetime tax comparison
  // RRSP: saved tax now (refunds), pays tax later
  const rrspTaxSavedNow = totalRefundReinvested;
  const rrspTaxPaidLater = rrspWithdrawalTax;
  const rrspNetTax = rrspTaxPaidLater - rrspTaxSavedNow;

  // TFSA: paid tax now, no tax later
  const tfsaNetTax = tfsaTaxPaidUpfront;

  const winner = rrspAfterTax > tfsaAfterTax ? 'RRSP' : 'TFSA';
  const advantage = Math.abs(rrspAfterTax - tfsaAfterTax);

  // ── Breakeven retirement income ──
  // Find the retirement income where RRSP after-tax = TFSA after-tax
  // RRSP wins when retirement marginal < current marginal, so breakeven is where they equal
  let breakevenIncome = null;
  for (let testIncome = 0; testIncome <= 500000; testIncome += 500) {
    const testMarginal = marginalRate(testIncome, province);
    const testRRSPTax = rrspNominal * testMarginal;
    const testRRSPNet = rrspNominal - testRRSPTax;
    if (testRRSPNet <= tfsaAfterTax) {
      breakevenIncome = testIncome;
      break;
    }
  }

  // ── Sensitivity table data ──
  const sensitivityLevels = [20000, 35000, 50000, 65000, 80000, 100000, 125000, 150000, 200000];
  const sensitivityData = sensitivityLevels.map(ri => {
    const mr = marginalRate(ri, province);
    const rrspTx = rrspNominal * mr;
    const rrspNet = rrspNominal - rrspTx;
    const w = rrspNet > tfsaAfterTax ? 'RRSP' : 'TFSA';
    const adv = Math.abs(rrspNet - tfsaAfterTax);
    return { income: ri, marginal: mr, rrspNet, tfsaNet: tfsaAfterTax, winner: w, advantage: adv };
  });

  // ── Why explanation ──
  let whyText = '';
  if (winner === 'RRSP') {
    whyText = `Your current marginal rate (${(currentMarginal * 100).toFixed(1)}%) is <strong>higher</strong> than your expected retirement rate (${(retireMarginal * 100).toFixed(1)}%). The RRSP tax deduction now is worth more than the tax you'll pay on withdrawals later.`;
  } else {
    whyText = `Your expected retirement marginal rate (${(retireMarginal * 100).toFixed(1)}%) is <strong>equal to or higher</strong> than your current rate (${(currentMarginal * 100).toFixed(1)}%). With a TFSA, you pay tax now at the lower rate and withdraw tax-free.`;
  }

  // ── Render Results ──
  const resultsEl = document.getElementById('rrsptfsa-results');
  const winColor = winner === 'RRSP' ? 'var(--fg-purple)' : 'var(--brand-success)';

  resultsEl.innerHTML = `
    <div class="result-card" style="border: 3px solid ${winColor}; background: linear-gradient(135deg, ${winColor}11, ${winColor}05); padding: 1.5rem;">
      <div style="font-size: 2.2rem; font-weight: 800; color: ${winColor}; margin-bottom: 0.25rem;">🏆 ${winner} Wins!</div>
      <div style="font-size: 1.3rem; font-weight: 600; color: ${winColor};" class="mono">by ${fmtFull(advantage)}</div>
      <div style="margin-top: 0.75rem; font-size: 0.95rem; color: var(--text-secondary); line-height: 1.5;">${whyText}</div>
    </div>
    <div class="result-card">
      <div class="result-label">RRSP — Net After-Tax at Retirement</div>
      <div class="result-value mono" style="color: var(--fg-purple);">${fmtFull(rrspAfterTax)}</div>
      <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.25rem;">Nominal: ${fmtFull(rrspNominal)} · Real: ${fmtFull(rrspReal)}</div>
    </div>
    <div class="result-card">
      <div class="result-label">TFSA — Net After-Tax at Retirement</div>
      <div class="result-value mono" style="color: var(--brand-success);">${fmtFull(tfsaAfterTax)}</div>
      <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.25rem;">Nominal: ${fmtFull(tfsaNominal)} · Real: ${fmtFull(tfsaReal)}</div>
    </div>
    <div class="result-card">
      <div class="result-label">RRSP Lifetime Tax</div>
      <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 0.25rem;">
        <span style="font-size: 0.85rem; color: var(--brand-success);">Saved now: ${fmtFull(rrspTaxSavedNow)}</span>
        <span style="font-size: 0.85rem; color: var(--brand-danger);">Paid later: ${fmtFull(rrspTaxPaidLater)}</span>
      </div>
      <div class="result-value mono" style="margin-top: 0.25rem;">Net tax: ${fmtFull(rrspNetTax)}</div>
    </div>
    <div class="result-card">
      <div class="result-label">TFSA Lifetime Tax</div>
      <div style="font-size: 0.85rem; color: var(--brand-danger); margin-top: 0.25rem;">Paid upfront: ${fmtFull(tfsaTaxPaidUpfront)}</div>
      <div class="result-value mono" style="margin-top: 0.25rem;">Net tax: ${fmtFull(tfsaNetTax)}</div>
    </div>
    <div class="result-card">
      <div class="result-label">Your Marginal Rates</div>
      <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
        <div style="text-align: center;">
          <div style="font-size: 0.8rem; color: var(--text-secondary);">Now</div>
          <div class="mono" style="font-size: 1.3rem; font-weight: 700;">${(currentMarginal * 100).toFixed(1)}%</div>
        </div>
        <div style="font-size: 1.5rem; align-self: center;">→</div>
        <div style="text-align: center;">
          <div style="font-size: 0.8rem; color: var(--text-secondary);">Retirement</div>
          <div class="mono" style="font-size: 1.3rem; font-weight: 700;">${(retireMarginal * 100).toFixed(1)}%</div>
        </div>
      </div>
    </div>
    ${breakevenIncome !== null ? `
    <div class="result-card" style="border-left: 4px solid var(--brand-warning);">
      <div class="result-label">⚖️ Breakeven Retirement Income</div>
      <div class="result-value mono">${fmtFull(breakevenIncome)}</div>
      <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.25rem;">Above this, TFSA wins. Below this, RRSP wins.</div>
    </div>` : `
    <div class="result-card" style="border-left: 4px solid var(--brand-success);">
      <div class="result-label">⚖️ Breakeven</div>
      <div style="font-size: 0.9rem; color: var(--text-secondary);">RRSP wins at all tested retirement income levels up to $500k — your current rate is very low.</div>
    </div>`}
  `;

  // ── Breakdown: Charts + Sensitivity Table ──
  const breakdownEl = document.getElementById('rrsptfsa-breakdown');

  // Dual line chart
  const svgW = 700, svgH = 320, pad = { t: 30, r: 30, b: 50, l: 70 };
  const plotW = svgW - pad.l - pad.r;
  const plotH = svgH - pad.t - pad.b;
  const maxBal = Math.max(rrspGrowth[rrspGrowth.length - 1], tfsaGrowth[tfsaGrowth.length - 1]) * 1.05;

  function linePoints(data) {
    return data.map((v, i) => {
      const x = pad.l + (i / (data.length - 1)) * plotW;
      const y = pad.t + plotH - (v / maxBal) * plotH;
      return `${x},${y}`;
    }).join(' ');
  }

  // Y-axis labels
  let yLabels = '';
  for (let i = 0; i <= 4; i++) {
    const val = (maxBal / 4) * i;
    const y = pad.t + plotH - (val / maxBal) * plotH;
    yLabels += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" fill="var(--text-muted)" font-size="10">$${(val / 1000).toFixed(0)}k</text>`;
    yLabels += `<line x1="${pad.l}" y1="${y}" x2="${svgW - pad.r}" y2="${y}" stroke="var(--border-primary)" stroke-dasharray="3,3"/>`;
  }

  // X-axis labels
  let xLabels = '';
  const labelInterval = Math.max(1, Math.floor(years / 6));
  for (let i = 0; i < years; i += labelInterval) {
    const x = pad.l + (i / (years - 1)) * plotW;
    xLabels += `<text x="${x}" y="${svgH - 10}" text-anchor="middle" fill="var(--text-muted)" font-size="10">Age ${age + i + 1}</text>`;
  }
  // Always show last
  const lastX = pad.l + plotW;
  xLabels += `<text x="${lastX}" y="${svgH - 10}" text-anchor="middle" fill="var(--text-muted)" font-size="10">Age ${retireAge}</text>`;

  const lineChart = `
    <svg viewBox="0 0 ${svgW} ${svgH}" style="width: 100%; max-width: ${svgW}px; height: auto;">
      ${yLabels}${xLabels}
      <polyline points="${linePoints(rrspGrowth)}" fill="none" stroke="#2C087D" stroke-width="2.5"/>
      <polyline points="${linePoints(tfsaGrowth)}" fill="none" stroke="var(--brand-success)" stroke-width="2.5"/>
      <rect x="${pad.l + 10}" y="${pad.t}" width="12" height="12" rx="2" fill="#2C087D"/>
      <text x="${pad.l + 28}" y="${pad.t + 10}" fill="var(--text-secondary)" font-size="11">RRSP (pre-tax)</text>
      <rect x="${pad.l + 140}" y="${pad.t}" width="12" height="12" rx="2" fill="var(--brand-success)"/>
      <text x="${pad.l + 158}" y="${pad.t + 10}" fill="var(--text-secondary)" font-size="11">TFSA</text>
    </svg>`;

  // Stacked bar: tax now vs tax later
  const barW = 300, barH = 180, barPad = 40;
  const maxTax = Math.max(rrspTaxPaidLater, tfsaTaxPaidUpfront, rrspTaxSavedNow) * 1.1 || 1;
  const bw = 60;

  function taxBarH(val) { return (val / maxTax) * (barH - barPad * 2); }

  const taxChart = `
    <svg viewBox="0 0 ${barW} ${barH}" style="width: 100%; max-width: ${barW}px; height: auto;">
      <!-- RRSP -->
      <rect x="50" y="${barH - barPad - taxBarH(rrspTaxSavedNow)}" width="${bw}" height="${taxBarH(rrspTaxSavedNow)}" fill="var(--brand-success)" rx="4">
        <title>RRSP tax saved now: ${fmtFull(rrspTaxSavedNow)}</title></rect>
      <rect x="50" y="${barH - barPad - taxBarH(rrspTaxSavedNow) - taxBarH(rrspTaxPaidLater)}" width="${bw}" height="${taxBarH(rrspTaxPaidLater)}" fill="var(--brand-danger)" rx="4">
        <title>RRSP tax paid later: ${fmtFull(rrspTaxPaidLater)}</title></rect>
      <text x="80" y="${barH - 10}" text-anchor="middle" fill="var(--text-secondary)" font-size="12" font-weight="600">RRSP</text>
      <!-- TFSA -->
      <rect x="190" y="${barH - barPad - taxBarH(tfsaTaxPaidUpfront)}" width="${bw}" height="${taxBarH(tfsaTaxPaidUpfront)}" fill="var(--brand-warning)" rx="4">
        <title>TFSA tax paid upfront: ${fmtFull(tfsaTaxPaidUpfront)}</title></rect>
      <text x="220" y="${barH - 10}" text-anchor="middle" fill="var(--text-secondary)" font-size="12" font-weight="600">TFSA</text>
      <!-- Legend -->
      <rect x="30" y="5" width="10" height="10" rx="2" fill="var(--brand-success)"/><text x="44" y="14" font-size="9" fill="var(--text-muted)">Tax saved</text>
      <rect x="110" y="5" width="10" height="10" rx="2" fill="var(--brand-danger)"/><text x="124" y="14" font-size="9" fill="var(--text-muted)">Tax paid later</text>
      <rect x="200" y="5" width="10" height="10" rx="2" fill="var(--brand-warning)"/><text x="214" y="14" font-size="9" fill="var(--text-muted)">Tax paid now</text>
    </svg>`;

  // Sensitivity table
  let sensRows = sensitivityData.map(d => `
    <tr style="${d.income === retireIncome ? 'background: ' + winColor + '11; font-weight: 600;' : ''}">
      <td style="padding: 0.4rem 0.6rem;" class="mono">${fmtFull(d.income)}</td>
      <td style="padding: 0.4rem 0.6rem; text-align: center;" class="mono">${(d.marginal * 100).toFixed(1)}%</td>
      <td style="padding: 0.4rem 0.6rem; text-align: right;" class="mono">${fmtFull(d.rrspNet)}</td>
      <td style="padding: 0.4rem 0.6rem; text-align: right;" class="mono">${fmtFull(d.tfsaNet)}</td>
      <td style="padding: 0.4rem 0.6rem; text-align: center; font-weight: 700; color: ${d.winner === 'RRSP' ? 'var(--fg-purple)' : 'var(--brand-success)'};">${d.winner} +${fmtFull(d.advantage)}</td>
    </tr>`).join('');

  breakdownEl.innerHTML = `
    <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">📈 Account Growth Over Time</h3>
    <div class="glass-card" style="padding: 1.5rem; overflow-x: auto;">
      ${lineChart}
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem;">
      <div>
        <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">💰 Tax: Now vs Later</h3>
        <div class="glass-card" style="padding: 1.5rem; overflow-x: auto;">
          ${taxChart}
        </div>
      </div>
      <div>
        <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">📊 Key Assumptions</h3>
        <div class="glass-card" style="padding: 1.5rem; font-size: 0.9rem; line-height: 1.8;">
          <div>📅 <strong>${years}</strong> years to retirement</div>
          <div>💵 <strong>${fmtFull(contribution)}</strong>/yr contribution</div>
          <div>🔄 RRSP refund of <strong>${fmtFull(rrspRefundPerYear)}</strong>/yr reinvested</div>
          <div>📈 <strong>${(returnRate * 100).toFixed(1)}%</strong> nominal return</div>
          <div>📉 <strong>${(inflation * 100).toFixed(1)}%</strong> inflation</div>
          <div>🏛️ Province: <strong>${province}</strong></div>
        </div>
      </div>
    </div>
    <h3 style="margin-top: 2rem; margin-bottom: 1rem; font-size: 1.1rem;">🔍 Sensitivity: Winner at Different Retirement Incomes</h3>
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-primary);">
            <th style="padding: 0.5rem 0.6rem; text-align: left;">Retirement Income</th>
            <th style="padding: 0.5rem 0.6rem; text-align: center;">Marginal Rate</th>
            <th style="padding: 0.5rem 0.6rem; text-align: right;">RRSP After-Tax</th>
            <th style="padding: 0.5rem 0.6rem; text-align: right;">TFSA After-Tax</th>
            <th style="padding: 0.5rem 0.6rem; text-align: center;">Winner</th>
          </tr>
        </thead>
        <tbody>${sensRows}</tbody>
      </table>
    </div>
    <p style="margin-top: 1.5rem; font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
      ⚠️ This calculator uses simplified assumptions: flat marginal rates on full withdrawal, no OAS clawback, no pension income splitting, no CPP/EI considerations, and no RRSP HBP/LLP. 
      RRSP refund reinvestment assumes full refund is contributed to RRSP each year. Actual results depend on your complete financial picture. Consult a financial advisor for personalized advice.
    </p>
  `;
}

// Auto-calculate on load
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('rvt-age')) calculateRRSPvsTFSA();
});
