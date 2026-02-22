function calculateRRSP() {
  const income = parseFloat(document.getElementById('rrsp-income').value) || 0;
  const otherIncome = parseFloat(document.getElementById('rrsp-other-income').value) || 0;
  const province = document.getElementById('rrsp-province').value;
  const contribution = parseFloat(document.getElementById('rrsp-contribution').value) || 0;

  const resultsEl = document.getElementById('rrsp-results');
  const breakdownEl = document.getElementById('rrsp-breakdown');

  if (income <= 0) {
    resultsEl.innerHTML = '<div class="result-card glass-card" style="padding:2rem;text-align:center;color:var(--text-secondary);">Enter your income to see your RRSP tax refund.</div>';
    breakdownEl.innerHTML = '';
    return;
  }

  const totalIncome = income + otherIncome;
  const maxRoom = Math.min(totalIncome * 0.18, 32490);
  document.getElementById('rrsp-room-hint').textContent = `2026 max: 18% of earned income, up to $32,490 — Your room: ${fmtFull(maxRoom)}`;

  const effectiveContribution = Math.min(contribution, maxRoom, totalIncome);
  const taxableWithout = Math.max(totalIncome, 0);
  const taxableWith = Math.max(totalIncome - effectiveContribution, 0);

  // Federal brackets 2026
  const fedBrackets = [
    { min: 0, max: 57375, rate: 0.15 },
    { min: 57375, max: 114750, rate: 0.205 },
    { min: 114750, max: 158468, rate: 0.26 },
    { min: 158468, max: 220000, rate: 0.29 },
    { min: 220000, max: Infinity, rate: 0.33 }
  ];

  // Provincial brackets 2025/2026
  const provBrackets = {
    AB: [
      { min: 0, max: 148269, rate: 0.10 },
      { min: 148269, max: 177922, rate: 0.12 },
      { min: 177922, max: 237230, rate: 0.13 },
      { min: 237230, max: 355845, rate: 0.14 },
      { min: 355845, max: Infinity, rate: 0.15 }
    ],
    BC: [
      { min: 0, max: 47937, rate: 0.0506 },
      { min: 47937, max: 95875, rate: 0.077 },
      { min: 95875, max: 110076, rate: 0.105 },
      { min: 110076, max: 133664, rate: 0.1229 },
      { min: 133664, max: 181232, rate: 0.147 },
      { min: 181232, max: 252752, rate: 0.168 },
      { min: 252752, max: Infinity, rate: 0.205 }
    ],
    MB: [
      { min: 0, max: 47000, rate: 0.108 },
      { min: 47000, max: 100000, rate: 0.1275 },
      { min: 100000, max: Infinity, rate: 0.174 }
    ],
    NB: [
      { min: 0, max: 49958, rate: 0.094 },
      { min: 49958, max: 99916, rate: 0.14 },
      { min: 99916, max: 185064, rate: 0.16 },
      { min: 185064, max: Infinity, rate: 0.195 }
    ],
    NL: [
      { min: 0, max: 43198, rate: 0.087 },
      { min: 43198, max: 86395, rate: 0.145 },
      { min: 86395, max: 154244, rate: 0.158 },
      { min: 154244, max: 215943, rate: 0.178 },
      { min: 215943, max: 275870, rate: 0.198 },
      { min: 275870, max: 551739, rate: 0.208 },
      { min: 551739, max: 1103478, rate: 0.213 },
      { min: 1103478, max: Infinity, rate: 0.218 }
    ],
    NS: [
      { min: 0, max: 29590, rate: 0.0879 },
      { min: 29590, max: 59180, rate: 0.1495 },
      { min: 59180, max: 93000, rate: 0.1667 },
      { min: 93000, max: 150000, rate: 0.175 },
      { min: 150000, max: Infinity, rate: 0.21 }
    ],
    NT: [
      { min: 0, max: 50597, rate: 0.059 },
      { min: 50597, max: 101198, rate: 0.086 },
      { min: 101198, max: 164525, rate: 0.122 },
      { min: 164525, max: Infinity, rate: 0.1405 }
    ],
    NU: [
      { min: 0, max: 53268, rate: 0.04 },
      { min: 53268, max: 106537, rate: 0.07 },
      { min: 106537, max: 173205, rate: 0.09 },
      { min: 173205, max: Infinity, rate: 0.115 }
    ],
    ON: [
      { min: 0, max: 52886, rate: 0.0505 },
      { min: 52886, max: 105775, rate: 0.0915 },
      { min: 105775, max: 150000, rate: 0.1116 },
      { min: 150000, max: 220000, rate: 0.1216 },
      { min: 220000, max: Infinity, rate: 0.1316 }
    ],
    PE: [
      { min: 0, max: 32656, rate: 0.0965 },
      { min: 32656, max: 64313, rate: 0.1363 },
      { min: 64313, max: 105000, rate: 0.1665 },
      { min: 105000, max: 140000, rate: 0.18 },
      { min: 140000, max: Infinity, rate: 0.1875 }
    ],
    QC: [
      { min: 0, max: 51780, rate: 0.14 },
      { min: 51780, max: 103545, rate: 0.19 },
      { min: 103545, max: 126000, rate: 0.24 },
      { min: 126000, max: Infinity, rate: 0.2575 }
    ],
    SK: [
      { min: 0, max: 52057, rate: 0.105 },
      { min: 52057, max: 148734, rate: 0.125 },
      { min: 148734, max: Infinity, rate: 0.145 }
    ],
    YT: [
      { min: 0, max: 57375, rate: 0.064 },
      { min: 57375, max: 114750, rate: 0.09 },
      { min: 114750, max: 158468, rate: 0.109 },
      { min: 158468, max: 220000, rate: 0.128 },
      { min: 220000, max: 500000, rate: 0.15 },
      { min: 500000, max: Infinity, rate: 0.15 }
    ]
  };

  function calcTax(taxableIncome, brackets) {
    let tax = 0;
    for (const b of brackets) {
      if (taxableIncome <= b.min) break;
      const taxable = Math.min(taxableIncome, b.max) - b.min;
      tax += taxable * b.rate;
    }
    return tax;
  }

  function getMarginalRate(taxableIncome, brackets) {
    let rate = brackets[0].rate;
    for (const b of brackets) {
      if (taxableIncome > b.min) rate = b.rate;
    }
    return rate;
  }

  function getOptimalContribution(taxableIncome, brackets) {
    // Find current bracket threshold and how much to contribute to drop to next lower bracket
    for (let i = brackets.length - 1; i >= 0; i--) {
      if (taxableIncome > brackets[i].min) {
        const amountInBracket = taxableIncome - brackets[i].min;
        return { amount: amountInBracket, bracketRate: brackets[i].rate, nextThreshold: brackets[i].min };
      }
    }
    return { amount: 0, bracketRate: 0, nextThreshold: 0 };
  }

  const prov = provBrackets[province] || provBrackets.ON;

  const fedTaxWithout = calcTax(taxableWithout, fedBrackets);
  const fedTaxWith = calcTax(taxableWith, fedBrackets);
  const provTaxWithout = calcTax(taxableWithout, prov);
  const provTaxWith = calcTax(taxableWith, prov);

  const totalTaxWithout = fedTaxWithout + provTaxWithout;
  const totalTaxWith = fedTaxWith + provTaxWith;
  const refund = totalTaxWithout - totalTaxWith;

  const fedMarginal = getMarginalRate(taxableWithout, fedBrackets);
  const provMarginal = getMarginalRate(taxableWithout, prov);
  const combinedMarginal = fedMarginal + provMarginal;
  const effectiveRate = taxableWithout > 0 ? totalTaxWithout / taxableWithout : 0;

  // Optimal contribution to drop federal bracket
  const fedOptimal = getOptimalContribution(taxableWithout, fedBrackets);
  const provOptimal = getOptimalContribution(taxableWithout, prov);
  const optimalContrib = Math.min(fedOptimal.amount, maxRoom);

  // Bar chart max
  const barMax = Math.max(totalTaxWithout, 1);

  resultsEl.innerHTML = `
    <div class="result-card glass-card" style="padding: 1.5rem; text-align: center; background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(59,130,246,0.1));">
      <div class="result-label">Your RRSP Tax Refund</div>
      <div class="result-value mono" style="font-size: 2.5rem; color: var(--brand-success);">${fmtFull(refund)}</div>
      <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.25rem;">
        from a ${fmtFull(effectiveContribution)} contribution
      </div>
    </div>
    <div class="result-card glass-card" style="padding: 1.25rem;">
      <div class="result-label">Combined Marginal Rate</div>
      <div class="result-value mono" style="font-size: 1.5rem;">${(combinedMarginal * 100).toFixed(2)}%</div>
      <div style="color: var(--text-secondary); font-size: 0.8rem;">Federal ${(fedMarginal * 100).toFixed(1)}% + Provincial ${(provMarginal * 100).toFixed(1)}%</div>
    </div>
    <div class="result-card glass-card" style="padding: 1.25rem;">
      <div class="result-label">Effective Tax Rate</div>
      <div class="result-value mono" style="font-size: 1.5rem;">${(effectiveRate * 100).toFixed(2)}%</div>
      <div style="color: var(--text-secondary); font-size: 0.8rem;">On total income of ${fmtFull(taxableWithout)}</div>
    </div>
    <div class="result-card glass-card" style="padding: 1.25rem;">
      <div class="result-label">Optimal Contribution</div>
      <div class="result-value mono" style="font-size: 1.5rem; color: var(--brand-warning);">${fmtFull(optimalContrib)}</div>
      <div style="color: var(--text-secondary); font-size: 0.8rem;">To drop to next federal bracket (${(fedOptimal.bracketRate * 100).toFixed(1)}% → ${fedOptimal.nextThreshold > 0 ? (getMarginalRate(fedOptimal.nextThreshold, fedBrackets) * 100).toFixed(1) : '0'}%)</div>
    </div>
    <div class="result-card glass-card" style="padding: 1.25rem;">
      <div class="result-label" style="margin-bottom: 1rem;">Tax Comparison</div>
      <div style="display: flex; gap: 1.5rem; align-items: flex-end; height: 120px; margin-bottom: 0.75rem;">
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%;">
          <div class="mono" style="font-size:0.8rem; margin-bottom:0.25rem; color:var(--brand-danger);">${fmtFull(totalTaxWithout)}</div>
          <div style="width:100%; background:var(--brand-danger); border-radius:var(--radius-lg) var(--radius-lg) 0 0; min-height:8px; height:${(totalTaxWithout / barMax * 100).toFixed(1)}%;"></div>
          <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.35rem;">Without RRSP</div>
        </div>
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%;">
          <div class="mono" style="font-size:0.8rem; margin-bottom:0.25rem; color:var(--brand-success);">${fmtFull(totalTaxWith)}</div>
          <div style="width:100%; background:var(--brand-success); border-radius:var(--radius-lg) var(--radius-lg) 0 0; min-height:8px; height:${(totalTaxWith / barMax * 100).toFixed(1)}%;"></div>
          <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.35rem;">With RRSP</div>
        </div>
      </div>
      <div style="text-align:center; font-size:0.85rem; color:var(--brand-success); font-weight:600;">You save ${fmtFull(refund)}</div>
    </div>
  `;

  // Breakdown section — bracket visualization + federal/provincial split
  const fedBracketRows = fedBrackets.map(b => {
    const lo = b.min;
    const hi = b.max === Infinity ? '∞' : fmtFull(b.max);
    const inBracket = Math.max(0, Math.min(taxableWithout, b.max === Infinity ? taxableWithout : b.max) - b.min);
    const taxInBracket = inBracket * b.rate;
    const active = taxableWithout > b.min;
    return `<tr style="opacity:${active ? 1 : 0.4};">
      <td style="padding:0.4rem 0.75rem;">${fmtFull(lo)} – ${hi}</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${(b.rate * 100).toFixed(1)}%</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${fmtFull(inBracket)}</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${fmtFull(taxInBracket)}</td>
    </tr>`;
  }).join('');

  const provBracketRows = prov.map(b => {
    const lo = b.min;
    const hi = b.max === Infinity ? '∞' : fmtFull(b.max);
    const inBracket = Math.max(0, Math.min(taxableWithout, b.max === Infinity ? taxableWithout : b.max) - b.min);
    const taxInBracket = inBracket * b.rate;
    const active = taxableWithout > b.min;
    return `<tr style="opacity:${active ? 1 : 0.4};">
      <td style="padding:0.4rem 0.75rem;">${fmtFull(lo)} – ${hi}</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${(b.rate * 100).toFixed(1)}%</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${fmtFull(inBracket)}</td>
      <td style="padding:0.4rem 0.75rem; text-align:right;" class="mono">${fmtFull(taxInBracket)}</td>
    </tr>`;
  }).join('');

  const provName = document.getElementById('rrsp-province').selectedOptions[0].text;

  // Bracket position visualization
  const allBracketThresholds = fedBrackets.filter(b => b.max !== Infinity).map(b => b.max);
  const vizMax = Math.max(taxableWithout * 1.2, 250000);
  const incomePos = (taxableWithout / vizMax * 100).toFixed(1);
  const bracketMarkers = allBracketThresholds.map(t => {
    const pos = (t / vizMax * 100).toFixed(1);
    return `<div style="position:absolute; left:${pos}%; top:0; bottom:0; width:1px; background:var(--border-primary);"></div>
            <div style="position:absolute; left:${pos}%; bottom:-1.4rem; font-size:0.65rem; color:var(--text-secondary); transform:translateX(-50%);">${(t/1000).toFixed(0)}k</div>`;
  }).join('');

  breakdownEl.innerHTML = `
    <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">📊 Where Your Income Falls</h3>
    <div style="position:relative; height:28px; background:var(--bg-secondary); border-radius:14px; overflow:visible; margin-bottom:2.5rem; border:1px solid var(--border-primary);">
      <div style="position:absolute; left:0; top:0; bottom:0; width:${incomePos}%; background:linear-gradient(90deg, var(--brand-success), var(--brand-warning)); border-radius:14px; transition:width 0.4s ease;"></div>
      ${bracketMarkers}
      <div style="position:absolute; left:${incomePos}%; top:-6px; width:3px; height:40px; background:var(--brand-danger); border-radius:2px; transform:translateX(-50%);"></div>
      <div style="position:absolute; left:${incomePos}%; top:-1.8rem; font-size:0.75rem; font-weight:600; color:var(--brand-danger); transform:translateX(-50%); white-space:nowrap;">${fmtFull(taxableWithout)}</div>
    </div>

    <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
      <div>
        <h4 style="margin: 0 0 0.75rem 0; font-size: 0.95rem;">🇨🇦 Federal Brackets</h4>
        <table style="width:100%; font-size:0.8rem; border-collapse:collapse;">
          <thead><tr style="border-bottom:1px solid var(--border-primary);">
            <th style="padding:0.4rem 0.75rem; text-align:left;">Range</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Rate</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Income</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Tax</th>
          </tr></thead>
          <tbody>${fedBracketRows}</tbody>
          <tfoot><tr style="border-top:1px solid var(--border-primary); font-weight:600;">
            <td colspan="3" style="padding:0.5rem 0.75rem;">Total Federal Tax</td>
            <td style="padding:0.5rem 0.75rem; text-align:right;" class="mono">${fmtFull(fedTaxWithout)}</td>
          </tr></tfoot>
        </table>
      </div>
      <div>
        <h4 style="margin: 0 0 0.75rem 0; font-size: 0.95rem;">🏠 ${provName} Brackets</h4>
        <table style="width:100%; font-size:0.8rem; border-collapse:collapse;">
          <thead><tr style="border-bottom:1px solid var(--border-primary);">
            <th style="padding:0.4rem 0.75rem; text-align:left;">Range</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Rate</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Income</th>
            <th style="padding:0.4rem 0.75rem; text-align:right;">Tax</th>
          </tr></thead>
          <tbody>${provBracketRows}</tbody>
          <tfoot><tr style="border-top:1px solid var(--border-primary); font-weight:600;">
            <td colspan="3" style="padding:0.5rem 0.75rem;">Total Provincial Tax</td>
            <td style="padding:0.5rem 0.75rem; text-align:right;" class="mono">${fmtFull(provTaxWithout)}</td>
          </tr></tfoot>
        </table>
      </div>
    </div>

    <div style="margin-top:1.5rem; padding:1rem; background:rgba(16,185,129,0.08); border-radius:var(--radius-lg); border:1px solid rgba(16,185,129,0.2);">
      <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:1rem; text-align:center;">
        <div>
          <div style="font-size:0.8rem; color:var(--text-secondary);">Federal Savings</div>
          <div class="mono" style="font-size:1.1rem; font-weight:600; color:var(--brand-success);">${fmtFull(fedTaxWithout - fedTaxWith)}</div>
        </div>
        <div>
          <div style="font-size:0.8rem; color:var(--text-secondary);">Provincial Savings</div>
          <div class="mono" style="font-size:1.1rem; font-weight:600; color:var(--brand-success);">${fmtFull(provTaxWithout - provTaxWith)}</div>
        </div>
        <div>
          <div style="font-size:0.8rem; color:var(--text-secondary);">Total Refund</div>
          <div class="mono" style="font-size:1.1rem; font-weight:700; color:var(--brand-success);">${fmtFull(refund)}</div>
        </div>
      </div>
    </div>
  `;
}
