/* =============================================
   FiggyBank Affiliate Upgrade JS
   ============================================= */

const AFFILIATE_TAG = 'figgy0a0-20';

function amazonLink(asin) {
  return `https://www.amazon.ca/dp/${asin}?tag=${AFFILIATE_TAG}`;
}

// ── Product Database ──

const PRODUCTS = {
  wealthyBarber:  { title: 'The Wealthy Barber Returns', author: 'David Chilton', asin: '0143190008', pitch: 'The classic Canadian guide to building wealth simply.', stars: 5 },
  tfsa:           { title: 'Tax-Free Savings Accounts', author: 'Gordon Pape', asin: '1459721646', pitch: 'Maximize your TFSA — the most powerful savings tool in Canada.', stars: 4 },
  howNot:         { title: 'How NOT to Move Back in with Your Parents', author: 'Rob Chicken', asin: '0143191292', pitch: 'A young Canadian\'s guide to financial independence.', stars: 4 },
  millionaire:    { title: 'Millionaire Teacher', author: 'Andrew Hallam', asin: '1119356296', pitch: 'Nine rules of wealth you should have learned in school.', stars: 5 },
  wealthing:      { title: 'Wealthing Like Rabbits', author: 'Robert R. Brown', asin: '0993874177', pitch: 'An original introduction to personal finance.', stars: 5 },
  commonSense:    { title: 'The Little Book of Common Sense Investing', author: 'John C. Bogle', asin: '1119404509', pitch: 'The only way to guarantee your fair share of market returns.', stars: 5 },
  moneyMakeover:  { title: 'The Total Money Makeover', author: 'Dave Ramsey', asin: '1595555277', pitch: 'A proven plan for financial fitness.', stars: 5 },
  builtToSell:    { title: 'Built to Sell', author: 'John Warrillow', asin: '1591845823', pitch: 'Creating a business that can thrive without you.', stars: 5 },
  artOfSelling:   { title: 'The Art of Selling Your Business', author: 'John Warrillow', asin: '1733478159', pitch: 'Winning strategies for maximizing your exit.', stars: 4 },
};

const P = PRODUCTS;

const AFFILIATE_DB = {
  mortgage:   [P.wealthyBarber, P.millionaire, P.wealthing],
  tax:        [P.wealthyBarber, P.tfsa, P.howNot],
  capgains:   [P.millionaire, P.tfsa],
  tfsa:       [P.tfsa, P.wealthyBarber, P.howNot],
  rrsp:       [P.wealthyBarber, P.tfsa, P.howNot],
  retirement: [P.millionaire, P.wealthyBarber, P.wealthing],
  incometax:  [P.wealthyBarber, P.tfsa, P.howNot],
  investment: [P.millionaire, P.commonSense, P.wealthing],
  compound:   [P.millionaire, P.commonSense, P.wealthing],
  debt:       [P.moneyMakeover, P.wealthing],
  networth:   [P.wealthyBarber, P.millionaire, P.wealthing],
  valuation:  [P.builtToSell, P.artOfSelling],
  merger:     [P.builtToSell, P.artOfSelling],
  fhsa:       [P.wealthyBarber, P.millionaire, P.wealthing],
  resp:       [P.wealthyBarber, P.tfsa, P.howNot],
  rentbuy:    [P.wealthyBarber, P.millionaire, P.wealthing],
  gic:        [P.tfsa, P.wealthyBarber],
  cpp:        [P.wealthyBarber, P.millionaire],
  salary:     [P.wealthyBarber, P.howNot],
  runway:     [P.builtToSell, P.artOfSelling],
  lease:      [P.wealthyBarber, P.wealthing],
  compare:    [P.millionaire, P.commonSense],
  currency:   [P.commonSense, P.millionaire],
};

// ── Helpers ──

function starsHTML(n) {
  return '<span class="affiliate-inline__stars">' + '★'.repeat(n) + '☆'.repeat(5 - n) + '</span>';
}

function detectCalcId() {
  const path = window.location.pathname.replace(/\/$/, '').split('/').pop() || '';
  // try matching known IDs
  for (const id of Object.keys(AFFILIATE_DB)) {
    if (path.includes(id)) return id;
  }
  // fallback: check body class or id
  for (const id of Object.keys(AFFILIATE_DB)) {
    if (document.body.className.includes(id) || document.getElementById(id)) return id;
  }
  return null;
}

// ── A: Inline Result Affiliate Card ──

function injectAffiliateSuggestion(calcId, resultData) {
  // Remove previous
  document.querySelectorAll('.affiliate-inline-injected').forEach(el => el.remove());

  const product = getSmartRecommendation(calcId, resultData) || (AFFILIATE_DB[calcId] && AFFILIATE_DB[calcId][0]);
  if (!product) return;

  const card = document.createElement('a');
  card.href = amazonLink(product.asin);
  card.target = '_blank';
  card.rel = 'noopener noreferrer sponsored';
  card.className = 'affiliate-inline affiliate-inline-injected';
  card.innerHTML = `
    <div class="affiliate-inline__icon">📖</div>
    <div class="affiliate-inline__body">
      <div class="affiliate-inline__label">Sponsored</div>
      <div class="affiliate-inline__heading">📖 Want to learn more?</div>
      <div class="affiliate-inline__title">${product.title}</div>
      <div class="affiliate-inline__author">by ${product.author}</div>
      ${starsHTML(product.stars)}
      <div class="affiliate-inline__pitch">${product.pitch}</div>
    </div>
    <span class="affiliate-inline__cta">View on Amazon.ca →</span>
  `;

  // Insert after first result card area
  const results = document.querySelector('.calc-results, .results-section, [class*="result"]');
  if (results) {
    results.parentNode.insertBefore(card, results.nextSibling);
  } else {
    // fallback: append to main
    const main = document.querySelector('main, .calculator, .container');
    if (main) main.appendChild(card);
  }
}

// ── B: Floating Smart Tip ──

function showSmartTip(calcId) {
  if (!calcId || !AFFILIATE_DB[calcId]) return;

  const storageKey = `smarttip_dismissed_${calcId}`;
  const dismissed = localStorage.getItem(storageKey);
  if (dismissed && Date.now() - parseInt(dismissed, 10) < 86400000) return;

  // Remove existing
  document.querySelectorAll('.smart-tip').forEach(el => el.remove());

  const product = AFFILIATE_DB[calcId][Math.floor(Math.random() * AFFILIATE_DB[calcId].length)];

  const tip = document.createElement('div');
  tip.className = 'smart-tip';
  tip.innerHTML = `
    <div class="smart-tip__header">
      <span class="smart-tip__header-text">💡 Smart Tip</span>
      <button class="smart-tip__close" aria-label="Close">✕</button>
    </div>
    <div class="smart-tip__body">
      <div class="smart-tip__emoji">📚</div>
      <div class="smart-tip__info">
        <div class="smart-tip__title">${product.title}</div>
        <div class="smart-tip__author">by ${product.author}</div>
        <div class="smart-tip__stars">${'★'.repeat(product.stars)}${'☆'.repeat(5 - product.stars)}</div>
      </div>
    </div>
    <div class="smart-tip__footer">
      <a href="${amazonLink(product.asin)}" target="_blank" rel="noopener noreferrer sponsored" class="smart-tip__btn">View on Amazon.ca →</a>
      <div class="smart-tip__sponsored">Sponsored</div>
    </div>
  `;

  tip.querySelector('.smart-tip__close').addEventListener('click', function (e) {
    e.stopPropagation();
    localStorage.setItem(storageKey, String(Date.now()));
    tip.style.opacity = '0';
    tip.style.transform = 'translateY(20px)';
    setTimeout(() => tip.remove(), 300);
  });

  document.body.appendChild(tip);
}

// ── C: Results-Based Smart Recommendations ──

function getSmartRecommendation(calcId, metrics) {
  if (!metrics || typeof metrics !== 'object') return null;

  // RRSP refund > $3000 → tax planning
  if ((calcId === 'rrsp' || calcId === 'tax') && metrics.refund > 3000) {
    return P.wealthyBarber;
  }
  // Mortgage payment > $3000/mo → homebuying guide
  if ((calcId === 'mortgage' || calcId === 'rentbuy') && metrics.monthlyPayment > 3000) {
    return P.wealthing;
  }
  // Capital gains tax > $10000 → tax optimization
  if (calcId === 'capgains' && metrics.taxOwed > 10000) {
    return P.tfsa;
  }
  // Debt payoff > 5 years → debt-free book
  if (calcId === 'debt' && metrics.yearsToPayoff > 5) {
    return P.moneyMakeover;
  }
  // High investment return → investing book
  if ((calcId === 'investment' || calcId === 'compound') && metrics.totalReturn > 100000) {
    return P.commonSense;
  }
  // Business valuation high → built to sell
  if ((calcId === 'valuation' || calcId === 'merger') && metrics.valuation > 500000) {
    return P.builtToSell;
  }

  return null;
}

// ── E: Enhance Existing Affiliate Sections ──

function enhanceExistingAffiliates() {
  document.querySelectorAll('.affiliate-resources').forEach(section => {
    if (section.dataset.enhanced) return;
    section.dataset.enhanced = 'true';

    // Add NEW badge to heading
    const heading = section.querySelector('h2, h3, h4');
    if (heading && !heading.querySelector('.aff-new-badge')) {
      const badge = document.createElement('span');
      badge.className = 'aff-new-badge';
      badge.textContent = 'NEW';
      heading.appendChild(badge);
    }

    // Enhance links
    section.querySelectorAll('a[href*="amazon"]').forEach(link => {
      if (link.querySelector('.aff-enhanced-cta')) return;

      // Add star rating before link if not present
      const starsEl = document.createElement('span');
      starsEl.className = 'affiliate-inline__stars';
      starsEl.textContent = '★★★★★';
      starsEl.style.display = 'block';
      starsEl.style.marginBottom = '0.25rem';
      link.parentNode.insertBefore(starsEl, link);

      // Restyle link as CTA button
      link.classList.add('aff-enhanced-cta');
      if (!link.textContent.includes('→')) {
        link.textContent = 'View on Amazon.ca →';
      }
    });
  });
}

// ── Init ──

function initAffiliateUpgrade() {
  const calcId = detectCalcId();

  // Enhance existing affiliate sections immediately
  enhanceExistingAffiliates();

  // Smart tip after 15 seconds
  if (calcId) {
    setTimeout(() => showSmartTip(calcId), 15000);
  }

  // Watch for calculator result changes
  const resultEls = document.querySelectorAll('.calc-results, .results-section, [class*="calc-result"]');
  if (resultEls.length > 0) {
    const observer = new MutationObserver(() => {
      // Debounce
      clearTimeout(observer._timer);
      observer._timer = setTimeout(() => {
        // Try to extract metrics from result elements
        const metrics = {};
        resultEls.forEach(el => {
          const text = el.textContent || '';
          // Simple number extraction for known patterns
          const dollarMatch = text.match(/\$[\d,]+\.?\d*/g);
          if (dollarMatch) {
            const vals = dollarMatch.map(v => parseFloat(v.replace(/[$,]/g, '')));
            if (calcId === 'rrsp' || calcId === 'tax') metrics.refund = Math.max(...vals);
            if (calcId === 'mortgage') metrics.monthlyPayment = Math.min(...vals.filter(v => v > 100));
            if (calcId === 'capgains') metrics.taxOwed = Math.max(...vals);
            if (calcId === 'investment' || calcId === 'compound') metrics.totalReturn = Math.max(...vals);
            if (calcId === 'valuation' || calcId === 'merger') metrics.valuation = Math.max(...vals);
          }
          const yearMatch = text.match(/(\d+\.?\d*)\s*year/i);
          if (yearMatch && calcId === 'debt') metrics.yearsToPayoff = parseFloat(yearMatch[1]);
        });

        injectAffiliateSuggestion(calcId, metrics);
      }, 500);
    });

    resultEls.forEach(el => observer.observe(el, { childList: true, subtree: true, characterData: true }));
  }
}

// Auto-init on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAffiliateUpgrade);
} else {
  initAffiliateUpgrade();
}
