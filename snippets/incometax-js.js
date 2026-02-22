function calculateIncomeTax() {
  const v = id => parseFloat(document.getElementById(id)?.value) || 0;
  const province = document.getElementById('incometax-province').value;
  const employment = v('incometax-employment');
  const selfEmploy = v('incometax-selfemploy');
  const capitalGainsTotal = v('incometax-capitalgains');
  const eligibleDiv = v('incometax-eligible-div');
  const ineligibleDiv = v('incometax-ineligible-div');
  const rental = v('incometax-rental');
  const rrspDeduction = v('incometax-rrsp');
  const otherDeductions = v('incometax-other-deductions');

  const resultsEl = document.getElementById('incometax-results');
  const breakdownEl = document.getElementById('incometax-breakdown');

  if (employment + selfEmploy + capitalGainsTotal + eligibleDiv + ineligibleDiv + rental <= 0) {
    resultsEl.innerHTML = '';
    breakdownEl.innerHTML = '';
    return;
  }

  // ── 2026 Constants ──
  const CPP_RATE = 0.0595;
  const CPP_MAX_PENSIONABLE = 71300;
  const CPP_EXEMPTION = 3500;
  const CPP_MAX_CONTRIB = 4034.10; // employee portion
  const CPP2_RATE = 0.04;
  const CPP2_CEILING = 81200;
  const CPP2_MAX_CONTRIB = 396.00;
  const EI_RATE = 0.0164;
  const EI_MAX_INSURABLE = 65700;
  const EI_MAX_PREMIUM = 1077.48;
  const FEDERAL_BPA = 16129;

  // QPP for Quebec
  const QPP_RATE = 0.0640;
  const QPP_MAX_CONTRIB = 4340.80;
  const QPIP_RATE_EE = 0.00494;
  const QPIP_MAX_INSURABLE = 98000;
  const QPIP_MAX_PREMIUM = 484.12;
  const EI_RATE_QC = 0.01312; // reduced EI for Quebec
  const EI_MAX_QC = 862.62;

  // ── Capital gains inclusion ──
  const capitalGainsTaxable = capitalGainsTotal * 0.5;

  // ── Dividend gross-up ──
  const eligibleGrossUp = eligibleDiv * 1.38;
  const ineligibleGrossUp = ineligibleDiv * 1.15;

  // ── Total & taxable income ──
  const totalIncome = employment + selfEmploy + capitalGainsTaxable + eligibleGrossUp + ineligibleGrossUp + rental;
  const taxableIncome = Math.max(0, totalIncome - rrspDeduction - otherDeductions);

  // ── CPP / QPP ──
  const earnedIncome = employment + selfEmploy;
  const isQuebec = province === 'QC';
  let cppContrib = 0, cpp2Contrib = 0, eiPremium = 0, qpipPremium = 0;

  if (isQuebec) {
    // QPP
    const qppPensionable = Math.min(earnedIncome, CPP_MAX_PENSIONABLE);
    const qppBase = Math.max(0, qppPensionable - CPP_EXEMPTION);
    cppContrib = Math.min(qppBase * QPP_RATE, QPP_MAX_CONTRIB);
    // QPP2
    if (earnedIncome > CPP_MAX_PENSIONABLE) {
      const qpp2Base = Math.min(earnedIncome, CPP2_CEILING) - CPP_MAX_PENSIONABLE;
      cpp2Contrib = Math.min(Math.max(0, qpp2Base) * CPP2_RATE, CPP2_MAX_CONTRIB);
    }
    // Self-employed pays both portions
    if (selfEmploy > 0 && employment === 0) {
      cppContrib *= 2;
      cpp2Contrib *= 2;
    } else if (selfEmploy > 0 && employment > 0) {
      // Additional self-employ CPP on self-employ portion
      const empCpp = Math.min(Math.max(0, Math.min(employment, CPP_MAX_PENSIONABLE) - CPP_EXEMPTION) * QPP_RATE, QPP_MAX_CONTRIB);
      const totalCpp = Math.min(Math.max(0, Math.min(earnedIncome, CPP_MAX_PENSIONABLE) - CPP_EXEMPTION) * QPP_RATE, QPP_MAX_CONTRIB);
      const selfCpp = totalCpp - empCpp;
      cppContrib = empCpp + selfCpp * 2;
    }
    // QPIP
    qpipPremium = Math.min(earnedIncome * QPIP_RATE_EE, QPIP_MAX_PREMIUM);
    // EI (reduced)
    eiPremium = Math.min(employment * EI_RATE_QC, EI_MAX_QC);
  } else {
    // CPP
    const cppPensionable = Math.min(earnedIncome, CPP_MAX_PENSIONABLE);
    const cppBase = Math.max(0, cppPensionable - CPP_EXEMPTION);
    cppContrib = Math.min(cppBase * CPP_RATE, CPP_MAX_CONTRIB);
    // CPP2
    if (earnedIncome > CPP_MAX_PENSIONABLE) {
      const cpp2Base = Math.min(earnedIncome, CPP2_CEILING) - CPP_MAX_PENSIONABLE;
      cpp2Contrib = Math.min(Math.max(0, cpp2Base) * CPP2_RATE, CPP2_MAX_CONTRIB);
    }
    // Self-employed pays both portions
    if (selfEmploy > 0 && employment === 0) {
      cppContrib *= 2;
      cpp2Contrib *= 2;
    } else if (selfEmploy > 0 && employment > 0) {
      const empCpp = Math.min(Math.max(0, Math.min(employment, CPP_MAX_PENSIONABLE) - CPP_EXEMPTION) * CPP_RATE, CPP_MAX_CONTRIB);
      const totalCpp = Math.min(Math.max(0, Math.min(earnedIncome, CPP_MAX_PENSIONABLE) - CPP_EXEMPTION) * CPP_RATE, CPP_MAX_CONTRIB);
      const selfCpp = totalCpp - empCpp;
      cppContrib = empCpp + selfCpp * 2;
    }
    // EI (employees only)
    eiPremium = Math.min(employment * EI_RATE, EI_MAX_PREMIUM);
  }

  // ── Federal tax brackets 2026 ──
  const fedBrackets = [
    [57375, 0.15],
    [114750 - 57375, 0.205],
    [158468 - 114750, 0.26],
    [220000 - 158468, 0.29],
    [Infinity, 0.33]
  ];

  // ── Provincial brackets 2026 ──
  const provData = {
    AB: {
      name: 'Alberta', bpa: 22323,
      brackets: [[148269, 0.10], [177922 - 148269, 0.12], [237230 - 177922, 0.13], [355845 - 237230, 0.14], [Infinity, 0.15]],
      eligDTC: 0.10, ineligDTC: 0.10
    },
    BC: {
      name: 'British Columbia', bpa: 12580,
      brackets: [[47937, 0.0506], [95875 - 47937, 0.077], [110076 - 95875, 0.105], [133664 - 110076, 0.1229], [181232 - 133664, 0.147], [252752 - 181232, 0.168], [Infinity, 0.205]],
      eligDTC: 0.10, ineligDTC: 0.0196
    },
    MB: {
      name: 'Manitoba', bpa: 15780,
      brackets: [[47000, 0.108], [100000 - 47000, 0.1275], [Infinity, 0.174]],
      eligDTC: 0.08, ineligDTC: 0.007
    },
    NB: {
      name: 'New Brunswick', bpa: 13044,
      brackets: [[49958, 0.094], [99916 - 49958, 0.14], [185064 - 99916, 0.16], [Infinity, 0.195]],
      eligDTC: 0.0314, ineligDTC: 0.0291
    },
    NL: {
      name: 'Newfoundland & Labrador', bpa: 10818,
      brackets: [[43198, 0.087], [86395 - 43198, 0.145], [154244 - 86395, 0.158], [215943 - 154244, 0.178], [275870 - 215943, 0.198], [551739 - 275870, 0.208], [1103478 - 551739, 0.213], [Infinity, 0.218]],
      eligDTC: 0.056, ineligDTC: 0.032
    },
    NS: {
      name: 'Nova Scotia', bpa: 8481,
      brackets: [[29590, 0.0879], [59180 - 29590, 0.1495], [93000 - 59180, 0.1667], [150000 - 93000, 0.175], [Infinity, 0.21]],
      eligDTC: 0.0885, ineligDTC: 0.0299
    },
    NT: {
      name: 'Northwest Territories', bpa: 17373,
      brackets: [[50597, 0.059], [101198 - 50597, 0.086], [164525 - 101198, 0.122], [Infinity, 0.1405]],
      eligDTC: 0.0601, ineligDTC: 0.028
    },
    NU: {
      name: 'Nunavut', bpa: 18767,
      brackets: [[53268, 0.04], [106537 - 53268, 0.07], [173205 - 106537, 0.09], [Infinity, 0.115]],
      eligDTC: 0.0551, ineligDTC: 0.0261
    },
    ON: {
      name: 'Ontario', bpa: 11865,
      brackets: [[51446, 0.0505], [102894 - 51446, 0.0915], [150000 - 102894, 0.1116], [220000 - 150000, 0.1216], [Infinity, 0.1316]],
      surtax: true, surtaxThresholds: [4991, 0.20, 6387, 0.36],
      eligDTC: 0.10, ineligDTC: 0.029863
    },
    PE: {
      name: 'Prince Edward Island', bpa: 13500,
      brackets: [[32656, 0.095], [64313 - 32656, 0.1325], [105000 - 64313, 0.166], [140000 - 105000, 0.1763], [Infinity, 0.19]],
      surtax: true, surtaxThresholds: [12500, 0.10],
      eligDTC: 0.105, ineligDTC: 0.028
    },
    QC: {
      name: 'Quebec', bpa: 18056,
      brackets: [[51780, 0.14], [103545 - 51780, 0.19], [126000 - 103545, 0.24], [Infinity, 0.2575]],
      eligDTC: 0.1132, ineligDTC: 0.0347,
      abatement: 0.165
    },
    SK: {
      name: 'Saskatchewan', bpa: 18491,
      brackets: [[52057, 0.105], [148734 - 52057, 0.125], [Infinity, 0.145]],
      eligDTC: 0.105, ineligDTC: 0.02105
    },
    YT: {
      name: 'Yukon', bpa: 16129,
      brackets: [[57375, 0.064], [114750 - 57375, 0.09], [158468 - 114750, 0.109], [500000 - 158468, 0.128], [Infinity, 0.15]],
      eligDTC: 0.0512, ineligDTC: 0.0241
    }
  };

  // ── Tax calculation helper ──
  function calcBracketTax(income, brackets) {
    let tax = 0, remaining = income;
    for (const [width, rate] of brackets) {
      const taxable = Math.min(remaining, width);
      tax += taxable * rate;
      remaining -= taxable;
      if (remaining <= 0) break;
    }
    return tax;
  }

  function getMarginalRate(income, brackets) {
    let remaining = income;
    let rate = 0;
    for (const [width, r] of brackets) {
      rate = r;
      remaining -= width;
      if (remaining <= 0) break;
    }
    return rate;
  }

  // ── Federal tax ──
  let fedTaxGross = calcBracketTax(taxableIncome, fedBrackets);
  const fedBPACredit = FEDERAL_BPA * 0.15;
  const fedCPPCredit = (cppContrib + cpp2Contrib) * 0.15;
  const fedEICredit = eiPremium * 0.15;
  const fedEligDTC = eligibleGrossUp * 0.150198;
  const fedIneligDTC = ineligibleGrossUp * 0.090301;
  let federalTax = Math.max(0, fedTaxGross - fedBPACredit - fedCPPCredit - fedEICredit - fedEligDTC - fedIneligDTC);

  // Quebec abatement
  if (isQuebec) {
    federalTax *= (1 - provData.QC.abatement);
  }

  // ── Provincial tax ──
  const prov = provData[province];
  let provTaxGross = calcBracketTax(taxableIncome, prov.brackets);
  const provBPACredit = prov.bpa * (prov.brackets[0][1]);
  const provEligDTC = eligibleGrossUp * (prov.eligDTC || 0);
  const provIneligDTC = ineligibleGrossUp * (prov.ineligDTC || 0);
  let provincialTax = Math.max(0, provTaxGross - provBPACredit - provEligDTC - provIneligDTC);

  // Ontario surtax
  if (province === 'ON' && prov.surtax) {
    const baseTax = provincialTax;
    let surtax = 0;
    if (baseTax > 6387) surtax += (baseTax - 6387) * 0.36;
    if (baseTax > 4991) surtax += (baseTax - 4991) * 0.20;
    provincialTax += surtax;
  }

  // PEI surtax
  if (province === 'PE' && prov.surtax) {
    if (provincialTax > 12500) {
      provincialTax += (provincialTax - 12500) * 0.10;
    }
  }

  // Quebec: QPIP premium
  let qpipDisplay = 0;
  if (isQuebec) {
    qpipDisplay = qpipPremium;
  }

  // ── Totals ──
  const totalTax = federalTax + provincialTax;
  const totalPayrollDeductions = cppContrib + cpp2Contrib + eiPremium + qpipDisplay;
  const totalDeductions = totalTax + totalPayrollDeductions;
  const grossIncome = employment + selfEmploy + capitalGainsTotal + eligibleDiv + ineligibleDiv + rental;
  const netIncome = grossIncome - totalDeductions;
  const effectiveRate = grossIncome > 0 ? (totalDeductions / grossIncome * 100) : 0;
  const fedMarginal = getMarginalRate(taxableIncome, fedBrackets);
  const provMarginal = getMarginalRate(taxableIncome, prov.brackets);
  const marginalRate = (fedMarginal + provMarginal) * 100;
  const monthly = netIncome / 12;
  const biweekly = netIncome / 26;
  const weekly = netIncome / 52;

  // ── Render results ──
  resultsEl.innerHTML = `
    <div class="result-card glass-card">
      <div class="result-label">Total Income</div>
      <div class="result-value mono">${fmtFull(grossIncome)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Taxable Income</div>
      <div class="result-value mono">${fmtFull(taxableIncome)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Federal Tax</div>
      <div class="result-value mono" style="color: var(--brand-danger)">${fmtFull(federalTax)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Provincial Tax (${prov.name})</div>
      <div class="result-value mono" style="color: var(--brand-danger)">${fmtFull(provincialTax)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">${isQuebec ? 'QPP' : 'CPP'} Contributions</div>
      <div class="result-value mono">${fmtFull(cppContrib)}${cpp2Contrib > 0 ? ` <span style="font-size:0.8rem;color:var(--text-secondary)">+ ${fmtFull(cpp2Contrib)} CPP2</span>` : ''}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">EI Premiums${isQuebec ? ' + QPIP' : ''}</div>
      <div class="result-value mono">${fmtFull(eiPremium)}${isQuebec ? ` <span style="font-size:0.8rem;color:var(--text-secondary)">+ ${fmtFull(qpipDisplay)} QPIP</span>` : ''}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Total Deductions</div>
      <div class="result-value mono" style="color: var(--brand-danger)">${fmtFull(totalDeductions)}</div>
    </div>
    <div class="result-card glass-card" style="border: 2px solid var(--brand-success);">
      <div class="result-label" style="font-size: 1.1rem;">💰 Net Take-Home Pay</div>
      <div class="result-value mono" style="color: var(--brand-success); font-size: 1.6rem;">${fmtFull(netIncome)}</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Effective Tax Rate</div>
      <div class="result-value mono">${effectiveRate.toFixed(1)}%</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Marginal Tax Rate</div>
      <div class="result-value mono" style="color: var(--brand-warning)">${marginalRate.toFixed(1)}%</div>
    </div>
    <div class="result-card glass-card">
      <div class="result-label">Monthly / Biweekly / Weekly</div>
      <div class="result-value mono" style="font-size: 0.95rem;">
        ${fmtFull(monthly)} / ${fmtFull(biweekly)} / ${fmtFull(weekly)}
      </div>
    </div>
  `;

  // ── Breakdown charts ──
  const donutData = [
    { label: 'Federal Tax', value: federalTax, color: '#ef4444' },
    { label: 'Provincial Tax', value: provincialTax, color: '#f97316' },
    { label: `${isQuebec ? 'QPP' : 'CPP'}`, value: cppContrib + cpp2Contrib, color: '#eab308' },
    { label: `EI${isQuebec ? '/QPIP' : ''}`, value: eiPremium + qpipDisplay, color: '#6366f1' },
    { label: 'Take-Home', value: Math.max(0, netIncome), color: '#22c55e' }
  ].filter(d => d.value > 0);

  const waterfallData = [
    { label: 'Gross Income', value: grossIncome, color: '#3b82f6' },
    { label: 'RRSP + Deductions', value: -(rrspDeduction + otherDeductions), color: '#a855f7' },
    { label: 'Federal Tax', value: -federalTax, color: '#ef4444' },
    { label: 'Provincial Tax', value: -provincialTax, color: '#f97316' },
    { label: `${isQuebec ? 'QPP' : 'CPP'}/EI`, value: -(totalPayrollDeductions), color: '#eab308' },
    { label: 'Take-Home', value: Math.max(0, netIncome), color: '#22c55e' }
  ];

  breakdownEl.innerHTML = `
    <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">📊 Tax Breakdown</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; align-items: start;">
      <div>
        <h4 style="margin: 0 0 0.75rem; color: var(--text-secondary); font-size: 0.9rem;">Income Allocation</h4>
        ${svgDonut(donutData, 220)}
      </div>
      <div>
        <h4 style="margin: 0 0 0.75rem; color: var(--text-secondary); font-size: 0.9rem;">Income Waterfall</h4>
        ${svgWaterfall(waterfallData, 400, 220)}
      </div>
    </div>
    <div style="margin-top: 1.5rem;">
      <h4 style="margin: 0 0 0.75rem; color: var(--text-secondary); font-size: 0.9rem;">💵 Monthly Cash Flow</h4>
      <div style="display: flex; gap: 0.5rem; align-items: end; height: 120px;">
        ${[
          { label: 'Gross', val: grossIncome / 12, color: '#3b82f6' },
          { label: 'Fed Tax', val: federalTax / 12, color: '#ef4444' },
          { label: 'Prov Tax', val: provincialTax / 12, color: '#f97316' },
          { label: isQuebec ? 'QPP' : 'CPP', val: (cppContrib + cpp2Contrib) / 12, color: '#eab308' },
          { label: 'EI', val: (eiPremium + qpipDisplay) / 12, color: '#6366f1' },
          { label: 'Net', val: Math.max(0, netIncome) / 12, color: '#22c55e' }
        ].map(b => {
          const maxVal = grossIncome / 12;
          const h = maxVal > 0 ? Math.max(4, (b.val / maxVal) * 100) : 4;
          return `<div style="flex:1;text-align:center;">
            <div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:2px;">${fmtFull(b.val)}</div>
            <div style="height:${h}px;background:${b.color};border-radius:4px 4px 0 0;"></div>
            <div style="font-size:0.65rem;color:var(--text-secondary);margin-top:2px;">${b.label}</div>
          </div>`;
        }).join('')}
      </div>
    </div>
    <div style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: var(--radius-lg); border: 1px solid var(--border-primary);">
      <h4 style="margin: 0 0 0.5rem; font-size: 0.9rem;">📋 Detailed Breakdown</h4>
      <table style="width:100%;font-size:0.85rem;border-collapse:collapse;">
        <tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Employment Income</td><td style="text-align:right" class="mono">${fmtFull(employment)}</td></tr>
        ${selfEmploy > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Self-Employment Income</td><td style="text-align:right" class="mono">${fmtFull(selfEmploy)}</td></tr>` : ''}
        ${capitalGainsTotal > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Capital Gains (taxable: ${fmtFull(capitalGainsTaxable)})</td><td style="text-align:right" class="mono">${fmtFull(capitalGainsTotal)}</td></tr>` : ''}
        ${eligibleDiv > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Eligible Dividends (grossed-up: ${fmtFull(eligibleGrossUp)})</td><td style="text-align:right" class="mono">${fmtFull(eligibleDiv)}</td></tr>` : ''}
        ${ineligibleDiv > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Ineligible Dividends (grossed-up: ${fmtFull(ineligibleGrossUp)})</td><td style="text-align:right" class="mono">${fmtFull(ineligibleDiv)}</td></tr>` : ''}
        ${rental > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Rental Income</td><td style="text-align:right" class="mono">${fmtFull(rental)}</td></tr>` : ''}
        <tr style="border-bottom:2px solid var(--border-primary);font-weight:600"><td style="padding:4px 0">Total Income</td><td style="text-align:right" class="mono">${fmtFull(grossIncome)}</td></tr>
        ${rrspDeduction > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">RRSP Deduction</td><td style="text-align:right;color:var(--brand-success)" class="mono">-${fmtFull(rrspDeduction)}</td></tr>` : ''}
        ${otherDeductions > 0 ? `<tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Other Deductions</td><td style="text-align:right;color:var(--brand-success)" class="mono">-${fmtFull(otherDeductions)}</td></tr>` : ''}
        <tr style="border-bottom:2px solid var(--border-primary);font-weight:600"><td style="padding:4px 0">Taxable Income</td><td style="text-align:right" class="mono">${fmtFull(taxableIncome)}</td></tr>
        <tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Federal Tax</td><td style="text-align:right;color:var(--brand-danger)" class="mono">-${fmtFull(federalTax)}</td></tr>
        <tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">Provincial Tax (${prov.name})</td><td style="text-align:right;color:var(--brand-danger)" class="mono">-${fmtFull(provincialTax)}</td></tr>
        <tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">${isQuebec ? 'QPP' : 'CPP'} Contributions</td><td style="text-align:right" class="mono">-${fmtFull(cppContrib + cpp2Contrib)}</td></tr>
        <tr style="border-bottom:1px solid var(--border-primary)"><td style="padding:4px 0">EI Premiums${isQuebec ? ' + QPIP' : ''}</td><td style="text-align:right" class="mono">-${fmtFull(eiPremium + qpipDisplay)}</td></tr>
        <tr style="font-weight:700;font-size:1rem;"><td style="padding:8px 0">Net Take-Home Pay</td><td style="text-align:right;color:var(--brand-success)" class="mono">${fmtFull(netIncome)}</td></tr>
      </table>
    </div>
  `;
}
