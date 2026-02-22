function calculateTFSA() {
  const ANNUAL_LIMITS = {
    2009: 5000, 2010: 5000, 2011: 5000, 2012: 5000,
    2013: 5500, 2014: 5500,
    2015: 10000,
    2016: 5500, 2017: 5500, 2018: 5500,
    2019: 6000, 2020: 6000, 2021: 6000, 2022: 6000, 2023: 6000,
    2024: 7000, 2025: 7000, 2026: 7000
  };

  const CURRENT_YEAR = 2026;
  const birthYear = parseInt(document.getElementById('tfsa-birth-year').value) || 1990;
  const bornInCanada = document.getElementById('tfsa-resident-check').checked;
  const residencyYear = bornInCanada ? 2009 : (parseInt(document.getElementById('tfsa-residency-year').value) || 2015);
  const totalContributions = parseFloat(document.getElementById('tfsa-contributions').value) || 0;

  // TFSA starts accumulating from the year you turn 18 OR 2009, whichever is later
  const year18 = birthYear + 18;
  const eligibleFrom = Math.max(2009, year18, residencyYear);

  // Build year-by-year breakdown
  const breakdown = [];
  let cumulative = 0;
  for (let y = eligibleFrom; y <= CURRENT_YEAR; y++) {
    const limit = ANNUAL_LIMITS[y] || 0;
    cumulative += limit;
    breakdown.push({ year: y, limit, cumulative });
  }

  const totalRoom = cumulative;
  const currentYearLimit = ANNUAL_LIMITS[CURRENT_YEAR] || 0;
  const remainingRoom = totalRoom - totalContributions;
  const overContribution = Math.max(0, totalContributions - totalRoom);
  const monthlyPenalty = Math.floor(overContribution / 100) * 1;

  // Render results
  const resultsEl = document.getElementById('tfsa-results');
  let statusHTML = '';
  if (overContribution > 0) {
    statusHTML = `
      <div class="result-card" style="border-left: 4px solid var(--brand-danger);">
        <div class="result-label">⚠️ Over-Contribution</div>
        <div class="result-value mono" style="color: var(--brand-danger);">${fmtFull(overContribution)}</div>
      </div>
      <div class="result-card" style="border-left: 4px solid var(--brand-warning);">
        <div class="result-label">Estimated Monthly Penalty</div>
        <div class="result-value mono" style="color: var(--brand-warning);">${fmtFull(monthlyPenalty)}/mo</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">CRA charges 1% per month on the highest excess amount in each month</div>
      </div>`;
  } else {
    statusHTML = `
      <div class="result-card" style="border-left: 4px solid var(--brand-success);">
        <div class="result-label">Remaining Room</div>
        <div class="result-value mono" style="color: var(--brand-success);">${fmtFull(remainingRoom)}</div>
      </div>`;
  }

  resultsEl.innerHTML = `
    <div class="result-card">
      <div class="result-label">Total Cumulative Room</div>
      <div class="result-value mono">${fmtFull(totalRoom)}</div>
      <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">From ${eligibleFrom} to ${CURRENT_YEAR} (${breakdown.length} years)</div>
    </div>
    <div class="result-card">
      <div class="result-label">${CURRENT_YEAR} Annual Limit</div>
      <div class="result-value mono">${fmtFull(currentYearLimit)}</div>
    </div>
    <div class="result-card">
      <div class="result-label">Your Total Contributions</div>
      <div class="result-value mono">${fmtFull(totalContributions)}</div>
    </div>
    ${statusHTML}
  `;

  // Render SVG bar chart
  const chartEl = document.getElementById('tfsa-chart');
  if (breakdown.length > 0) {
    const svgW = 700, svgH = 300, pad = { t: 20, r: 20, b: 50, l: 60 };
    const plotW = svgW - pad.l - pad.r;
    const plotH = svgH - pad.t - pad.b;
    const maxVal = breakdown[breakdown.length - 1].cumulative;
    const barW = Math.max(4, Math.min(30, plotW / breakdown.length - 2));
    const gap = (plotW - barW * breakdown.length) / (breakdown.length + 1);

    let bars = '', labels = '';
    breakdown.forEach((d, i) => {
      const x = pad.l + gap + i * (barW + gap);
      const h = (d.cumulative / maxVal) * plotH;
      const y = pad.t + plotH - h;
      const fill = d.cumulative <= totalContributions ? 'var(--brand-danger)' : 'var(--brand-success)';
      bars += `<rect x="${x}" y="${y}" width="${barW}" height="${h}" fill="${fill}" rx="2"><title>${d.year}: ${fmtFull(d.cumulative)} cumulative</title></rect>`;
      if (breakdown.length <= 18 || i % 2 === 0) {
        labels += `<text x="${x + barW / 2}" y="${svgH - 10}" text-anchor="middle" fill="var(--text-muted)" font-size="10">${d.year}</text>`;
      }
    });

    // Y-axis labels
    let yLabels = '';
    for (let i = 0; i <= 4; i++) {
      const val = (maxVal / 4) * i;
      const y = pad.t + plotH - (val / maxVal) * plotH;
      yLabels += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" fill="var(--text-muted)" font-size="10">${(val / 1000).toFixed(0)}k</text>`;
      yLabels += `<line x1="${pad.l}" y1="${y}" x2="${svgW - pad.r}" y2="${y}" stroke="var(--border-primary)" stroke-dasharray="3,3"/>`;
    }

    // Contribution line
    let contribLine = '';
    if (totalContributions > 0 && totalContributions <= maxVal * 1.1) {
      const cy = pad.t + plotH - (Math.min(totalContributions, maxVal) / maxVal) * plotH;
      contribLine = `<line x1="${pad.l}" y1="${cy}" x2="${svgW - pad.r}" y2="${cy}" stroke="var(--brand-warning)" stroke-width="2" stroke-dasharray="6,4"/>
        <text x="${svgW - pad.r}" y="${cy - 6}" text-anchor="end" fill="var(--brand-warning)" font-size="11" font-weight="600">Your contributions</text>`;
    }

    chartEl.innerHTML = `
      <div class="glass-card" style="padding: 1.5rem; overflow-x: auto;">
        <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">📊 Cumulative TFSA Room by Year</h3>
        <svg viewBox="0 0 ${svgW} ${svgH}" style="width: 100%; max-width: ${svgW}px; height: auto;">
          ${yLabels}${bars}${labels}${contribLine}
        </svg>
      </div>`;
  } else {
    chartEl.innerHTML = '';
  }

  // Render breakdown table
  const breakdownEl = document.getElementById('tfsa-breakdown');
  if (breakdown.length > 0) {
    let rows = breakdown.map(d => `
      <tr>
        <td style="padding: 0.5rem 0.75rem;" class="mono">${d.year}</td>
        <td style="padding: 0.5rem 0.75rem; text-align: right;" class="mono">${fmtFull(d.limit)}</td>
        <td style="padding: 0.5rem 0.75rem; text-align: right; font-weight: 600;" class="mono">${fmtFull(d.cumulative)}</td>
      </tr>`).join('');

    breakdownEl.innerHTML = `
      <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">📋 Year-by-Year Breakdown</h3>
      <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
          <thead>
            <tr style="border-bottom: 2px solid var(--border-primary);">
              <th style="padding: 0.5rem 0.75rem; text-align: left;">Year</th>
              <th style="padding: 0.5rem 0.75rem; text-align: right;">Annual Limit</th>
              <th style="padding: 0.5rem 0.75rem; text-align: right;">Cumulative Room</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <p style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted);">
        Note: This calculator does not account for withdrawals (which restore room the following year) or carry-forward adjustments from the CRA. Check your My CRA Account for your official TFSA room.
      </p>`;
  } else {
    breakdownEl.innerHTML = `<p style="color: var(--text-muted);">You are not yet eligible for TFSA contribution room. Eligibility begins the year you turn 18 (and no earlier than 2009).</p>`;
  }
}

// Auto-calculate on load
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('tfsa-birth-year')) calculateTFSA();
});
