/**
 * FiggyBank Money Milestones - Gamification System
 * Tracks calculator usage and awards achievement badges
 * @version 1.0.0
 */

(function() {
  'use strict';

  // Configuration
  const STORAGE_KEY = 'figgybank_milestones';
  const COLORS = {
    primary: '#2C087D',
    accent: '#FF6B6B',
    background: '#FCFAF4',
    dark: '#1a0548',
    light: '#f8f6f1'
  };

  // Calculator page mappings
  const CALCULATORS = {
    mortgage: 'page-mortgage',
    rentVsBuy: 'page-rent-vs-buy',
    tax: 'page-tax',
    capitalGains: 'page-capital-gains',
    investment: 'page-investment',
    compound: 'page-compound',
    resp: 'page-resp',
    cpp: 'page-cpp',
    retirement: 'page-retirement',
    valuation: 'page-valuation',
    ma: 'page-ma',
    runway: 'page-runway',
    debt: 'page-debt',
    salary: 'page-salary',
    netWorth: 'page-net-worth',
    budgeting: 'page-budgeting',
    loan: 'page-loan',
    savings: 'page-savings',
    inflation: 'page-inflation',
    roi: 'page-roi'
  };

  // Badge definitions
  const BADGES = [
    {
      id: 'home-explorer',
      emoji: '🏠',
      title: 'Home Explorer',
      description: 'Used mortgage and rent vs buy calculators',
      requires: ['mortgage', 'rentVsBuy']
    },
    {
      id: 'tax-strategist',
      emoji: '💰',
      title: 'Tax Strategist',
      description: 'Used tax and capital gains calculators',
      requires: ['tax', 'capitalGains']
    },
    {
      id: 'investment-pro',
      emoji: '📈',
      title: 'Investment Pro',
      description: 'Used investment and compound calculators',
      requires: ['investment', 'compound']
    },
    {
      id: 'education-planner',
      emoji: '🎓',
      title: 'Education Planner',
      description: 'Used RESP and compound calculators',
      requires: ['resp', 'compound']
    },
    {
      id: 'retirement-ready',
      emoji: '🏦',
      title: 'Retirement Ready',
      description: 'Used CPP and retirement calculators',
      requires: ['cpp', 'retirement']
    },
    {
      id: 'business-mogul',
      emoji: '💼',
      title: 'Business Mogul',
      description: 'Used valuation, M&A, and runway calculators',
      requires: ['valuation', 'ma', 'runway']
    },
    {
      id: 'debt-destroyer',
      emoji: '🏆',
      title: 'Debt Destroyer',
      description: 'Used debt and salary calculators',
      requires: ['debt', 'salary']
    },
    {
      id: 'figgybank-master',
      emoji: '🌟',
      title: 'FiggyBank Master',
      description: 'Used 10 or more different calculators',
      requires: 10
    },
    {
      id: 'power-user',
      emoji: '🔥',
      title: 'Power User',
      description: 'Used 15 or more different calculators',
      requires: 15
    },
    {
      id: 'financial-guru',
      emoji: '👑',
      title: 'Financial Guru',
      description: 'Used all 20 calculators',
      requires: 20
    }
  ];

  // State management
  class MilestonesManager {
    constructor() {
      this.data = this.loadData();
      this.init();
    }

    loadData() {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch (e) {
          console.error('Failed to load milestones data:', e);
        }
      }
      return {
        calculatorsUsed: [],
        badges: [],
        lastUpdated: null
      };
    }

    saveData() {
      this.data.lastUpdated = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
    }

    init() {
      this.createUI();
      this.trackCurrentPage();
      this.setupPageTracking();
    }

    trackCurrentPage() {
      // Check current page on load
      const currentPageId = document.body.id;
      if (currentPageId) {
        this.trackCalculator(currentPageId);
      }
    }

    setupPageTracking() {
      // Track when user navigates to calculator pages
      // Listen for hash changes and navigation events
      window.addEventListener('hashchange', () => this.checkForCalculatorPage());
      
      // Observer for dynamic page changes
      const observer = new MutationObserver(() => this.checkForCalculatorPage());
      observer.observe(document.body, { attributes: true, attributeFilter: ['id', 'class'] });
      
      // Track button clicks that might trigger calculator usage
      document.addEventListener('click', (e) => {
        const button = e.target.closest('button');
        if (button && (button.textContent.includes('Calculate') || button.id.includes('calc'))) {
          this.checkForCalculatorPage();
        }
      });
    }

    checkForCalculatorPage() {
      const bodyId = document.body.id;
      if (bodyId) {
        this.trackCalculator(bodyId);
      }
    }

    trackCalculator(pageId) {
      // Find which calculator this corresponds to
      const calculatorKey = Object.keys(CALCULATORS).find(key => CALCULATORS[key] === pageId);
      
      if (calculatorKey && !this.data.calculatorsUsed.includes(calculatorKey)) {
        this.data.calculatorsUsed.push(calculatorKey);
        this.saveData();
        this.checkForNewBadges(calculatorKey);
      }
    }

    checkForNewBadges(newCalculator) {
      const newBadges = [];
      
      BADGES.forEach(badge => {
        // Skip if already earned
        if (this.data.badges.includes(badge.id)) return;
        
        let earned = false;
        
        if (Array.isArray(badge.requires)) {
          // Check if all required calculators have been used
          earned = badge.requires.every(calc => this.data.calculatorsUsed.includes(calc));
        } else if (typeof badge.requires === 'number') {
          // Check if count threshold is met
          earned = this.data.calculatorsUsed.length >= badge.requires;
        }
        
        if (earned) {
          this.data.badges.push(badge.id);
          newBadges.push(badge);
        }
      });
      
      if (newBadges.length > 0) {
        this.saveData();
        newBadges.forEach(badge => this.showToast(badge));
      }
    }

    showToast(badge) {
      const toast = document.createElement('div');
      toast.className = 'figgy-milestone-toast';
      toast.innerHTML = `
        <div class="toast-content">
          <div class="toast-emoji">${badge.emoji}</div>
          <div class="toast-text">
            <div class="toast-title">Badge Unlocked!</div>
            <div class="toast-badge">${badge.title}</div>
          </div>
        </div>
      `;
      
      document.body.appendChild(toast);
      
      // Trigger animation
      setTimeout(() => toast.classList.add('show'), 10);
      
      // Auto-hide after 4 seconds
      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    createUI() {
      // Create floating trophy button
      const button = document.createElement('button');
      button.className = 'figgy-milestone-button';
      button.innerHTML = '🏆';
      button.setAttribute('aria-label', 'View achievements');
      button.onclick = () => this.togglePanel();
      
      // Add badge count indicator if any badges earned
      if (this.data.badges.length > 0) {
        const badge = document.createElement('span');
        badge.className = 'milestone-badge-count';
        badge.textContent = this.data.badges.length;
        button.appendChild(badge);
      }
      
      document.body.appendChild(button);
      
      // Create panel (hidden by default)
      this.createPanel();
    }

    createPanel() {
      const panel = document.createElement('div');
      panel.className = 'figgy-milestone-panel';
      panel.id = 'figgyMilestonePanel';
      
      const totalCalcs = Object.keys(CALCULATORS).length;
      const usedCalcs = this.data.calculatorsUsed.length;
      const progressPercent = (usedCalcs / totalCalcs) * 100;
      
      panel.innerHTML = `
        <div class="milestone-panel-content">
          <div class="milestone-header">
            <h2>🏆 Your Money Milestones</h2>
            <button class="milestone-close" aria-label="Close">&times;</button>
          </div>
          
          <div class="milestone-progress">
            <div class="progress-text">
              <span>Calculators Used</span>
              <span class="progress-count">${usedCalcs}/${totalCalcs}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${progressPercent}%"></div>
            </div>
          </div>
          
          <div class="milestone-badges">
            ${this.renderBadges()}
          </div>
          
          <div class="milestone-actions">
            <button class="milestone-share-btn" onclick="window.figgyMilestones.share()">
              📤 Share Your Progress
            </button>
          </div>
        </div>
      `;
      
      document.body.appendChild(panel);
      
      // Close button handler
      panel.querySelector('.milestone-close').onclick = () => this.togglePanel();
      
      // Close on outside click
      panel.onclick = (e) => {
        if (e.target === panel) this.togglePanel();
      };
    }

    renderBadges() {
      return BADGES.map(badge => {
        const earned = this.data.badges.includes(badge.id);
        return `
          <div class="milestone-badge ${earned ? 'earned' : 'locked'}">
            <div class="badge-emoji">${badge.emoji}</div>
            <div class="badge-info">
              <div class="badge-title">${badge.title}</div>
              <div class="badge-description">${badge.description}</div>
            </div>
            ${earned ? '<div class="badge-checkmark">✓</div>' : ''}
          </div>
        `;
      }).join('');
    }

    togglePanel() {
      const panel = document.getElementById('figgyMilestonePanel');
      if (panel) {
        panel.classList.toggle('open');
      }
    }

    share() {
      const usedCalcs = this.data.calculatorsUsed.length;
      const totalCalcs = Object.keys(CALCULATORS).length;
      const badgeCount = this.data.badges.length;
      
      const text = `I've used ${usedCalcs}/${totalCalcs} calculators on FiggyBank and earned ${badgeCount} achievement badges! 🏆 Track your money milestones at figgybank.ca`;
      
      if (navigator.share) {
        navigator.share({
          title: 'My FiggyBank Milestones',
          text: text,
          url: 'https://figgybank.ca'
        }).catch(err => console.log('Share cancelled:', err));
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
          alert('Progress copied to clipboard! 📋');
        });
      }
    }
  }

  // Styles
  const styles = `
    .figgy-milestone-button {
      position: fixed;
      bottom: 24px;
      left: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: linear-gradient(135deg, ${COLORS.primary} 0%, ${COLORS.dark} 100%);
      border: none;
      font-size: 28px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(44, 8, 125, 0.3);
      transition: all 0.3s ease;
      z-index: 999;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .figgy-milestone-button:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 20px rgba(44, 8, 125, 0.4);
    }

    .milestone-badge-count {
      position: absolute;
      top: -4px;
      right: -4px;
      background: ${COLORS.accent};
      color: white;
      font-size: 12px;
      font-weight: bold;
      padding: 2px 6px;
      border-radius: 10px;
      min-width: 18px;
      text-align: center;
    }

    .figgy-milestone-panel {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(4px);
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }

    .figgy-milestone-panel.open {
      opacity: 1;
      pointer-events: all;
    }

    .milestone-panel-content {
      background: ${COLORS.background};
      border-radius: 16px;
      max-width: 600px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    @media (prefers-color-scheme: dark) {
      .milestone-panel-content {
        background: #1a1a1a;
        color: ${COLORS.background};
      }
    }

    .milestone-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 24px;
      border-bottom: 2px solid ${COLORS.primary}20;
    }

    .milestone-header h2 {
      margin: 0;
      font-size: 24px;
      color: ${COLORS.primary};
    }

    @media (prefers-color-scheme: dark) {
      .milestone-header h2 {
        color: ${COLORS.accent};
      }
    }

    .milestone-close {
      background: none;
      border: none;
      font-size: 32px;
      cursor: pointer;
      color: #666;
      line-height: 1;
      padding: 0;
      width: 32px;
      height: 32px;
    }

    .milestone-close:hover {
      color: ${COLORS.accent};
    }

    .milestone-progress {
      padding: 20px 24px;
      background: ${COLORS.primary}08;
    }

    @media (prefers-color-scheme: dark) {
      .milestone-progress {
        background: ${COLORS.dark}40;
      }
    }

    .progress-text {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 14px;
      font-weight: 500;
    }

    .progress-count {
      color: ${COLORS.primary};
      font-weight: 700;
    }

    .progress-bar {
      height: 12px;
      background: #e0e0e0;
      border-radius: 6px;
      overflow: hidden;
    }

    @media (prefers-color-scheme: dark) {
      .progress-bar {
        background: #333;
      }
    }

    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, ${COLORS.primary} 0%, ${COLORS.accent} 100%);
      border-radius: 6px;
      transition: width 0.5s ease;
    }

    .milestone-badges {
      padding: 16px 24px;
      display: grid;
      gap: 12px;
    }

    .milestone-badge {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px;
      border-radius: 12px;
      border: 2px solid #e0e0e0;
      transition: all 0.3s ease;
    }

    @media (prefers-color-scheme: dark) {
      .milestone-badge {
        border-color: #333;
      }
    }

    .milestone-badge.earned {
      background: linear-gradient(135deg, ${COLORS.primary}10 0%, ${COLORS.accent}10 100%);
      border-color: ${COLORS.primary};
    }

    .milestone-badge.locked {
      opacity: 0.4;
    }

    .badge-emoji {
      font-size: 36px;
      flex-shrink: 0;
    }

    .badge-info {
      flex: 1;
    }

    .badge-title {
      font-weight: 700;
      font-size: 16px;
      margin-bottom: 4px;
      color: ${COLORS.primary};
    }

    @media (prefers-color-scheme: dark) {
      .badge-title {
        color: ${COLORS.accent};
      }
    }

    .badge-description {
      font-size: 13px;
      color: #666;
    }

    @media (prefers-color-scheme: dark) {
      .badge-description {
        color: #aaa;
      }
    }

    .badge-checkmark {
      color: ${COLORS.accent};
      font-size: 24px;
      font-weight: bold;
    }

    .milestone-actions {
      padding: 16px 24px 24px;
      border-top: 1px solid #e0e0e0;
    }

    @media (prefers-color-scheme: dark) {
      .milestone-actions {
        border-top-color: #333;
      }
    }

    .milestone-share-btn {
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, ${COLORS.primary} 0%, ${COLORS.dark} 100%);
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s ease;
      font-family: 'Inter', sans-serif;
    }

    .milestone-share-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(44, 8, 125, 0.3);
    }

    .figgy-milestone-toast {
      position: fixed;
      top: 24px;
      right: 24px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
      padding: 16px 20px;
      z-index: 1001;
      transform: translateX(400px);
      transition: transform 0.3s ease;
      border-left: 4px solid ${COLORS.accent};
    }

    @media (prefers-color-scheme: dark) {
      .figgy-milestone-toast {
        background: #1a1a1a;
        color: ${COLORS.background};
      }
    }

    .figgy-milestone-toast.show {
      transform: translateX(0);
    }

    .toast-content {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .toast-emoji {
      font-size: 32px;
    }

    .toast-title {
      font-size: 12px;
      font-weight: 600;
      color: ${COLORS.primary};
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    @media (prefers-color-scheme: dark) {
      .toast-title {
        color: ${COLORS.accent};
      }
    }

    .toast-badge {
      font-size: 16px;
      font-weight: 700;
      color: #333;
    }

    @media (prefers-color-scheme: dark) {
      .toast-badge {
        color: #fff;
      }
    }
  `;

  // Initialize
  function init() {
    // Inject styles
    const styleEl = document.createElement('style');
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);
    
    // Create manager instance
    window.figgyMilestones = new MilestonesManager();
  }

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
