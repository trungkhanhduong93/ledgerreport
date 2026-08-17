/**
 * iPOS Accounting Report - Landing Page Client Logic
 * Handles GitHub Releases Live Sync, Clipboard Copying, Modals, FAQs, and Tabs
 */

// Fallback configuration based on current latest verified release (v1.8.6)
const CONFIG = {
  repoOwner: 'trungkhanhduong93',
  repoName: 'ledgerreport',
  defaultVersion: 'v1.8.6',
  defaultFileName: 'iPOS_Accounting_Report.exe',
  defaultFileSize: '12.38 MB',
  defaultDate: '16/08/2026',
  defaultChecksum: 'aaf468a578b23060a85d1bf6e0ae95e3e4dd8878ddfe4aee5f7dfbb7a62ddbce',
  latestDownloadUrl: 'https://github.com/trungkhanhduong93/ledgerreport/releases/latest/download/iPOS_Accounting_Report.exe',
  releasesApiUrl: 'https://api.github.com/repos/trungkhanhduong93/ledgerreport/releases/latest'
};

document.addEventListener('DOMContentLoaded', () => {
  initLiveReleaseData();
  initCopyActions();
  initFaqAccordion();
  initReportTabs();
  initDownloadModal();
  initHeaderScroll();
  initMobileMenu();
});

/**
 * Fetch latest release data dynamically from GitHub REST API
 */
async function initLiveReleaseData() {
  const versionEl = document.getElementById('latestVersionTag');
  const sizeEl = document.getElementById('latestFileSize');
  const dateEl = document.getElementById('latestReleaseDate');
  const checksumShortEl = document.getElementById('checksumShort');
  const navVersionEl = document.getElementById('navVersionBadge');

  try {
    const response = await fetch(CONFIG.releasesApiUrl);
    if (!response.ok) throw new Error(`GitHub API error: ${response.status}`);
    
    const release = await response.json();
    const tag = release.tag_name || CONFIG.defaultVersion;
    const publishedDate = release.published_at ? formatDate(release.published_at) : CONFIG.defaultDate;
    
    // Find the exe asset
    const exeAsset = release.assets ? release.assets.find(a => a.name.endsWith('.exe')) : null;
    let formattedSize = CONFIG.defaultFileSize;
    let checksum = CONFIG.defaultChecksum;

    if (exeAsset) {
      if (exeAsset.size) {
        formattedSize = (exeAsset.size / (1024 * 1024)).toFixed(2) + ' MB';
      }
      if (exeAsset.digest && exeAsset.digest.startsWith('sha256:')) {
        checksum = exeAsset.digest.replace('sha256:', '');
      }
    }

    // Update DOM
    if (versionEl) versionEl.textContent = tag;
    if (navVersionEl) navVersionEl.textContent = tag;
    if (sizeEl) sizeEl.textContent = formattedSize;
    if (dateEl) dateEl.textContent = publishedDate;
    if (checksumShortEl) checksumShortEl.textContent = checksum.substring(0, 10) + '...';
    
    // Store full checksum for copy
    window.currentChecksum = checksum;

  } catch (error) {
    console.warn('Using default release fallback information:', error);
    // Apply default fallback data
    if (versionEl) versionEl.textContent = CONFIG.defaultVersion;
    if (navVersionEl) navVersionEl.textContent = CONFIG.defaultVersion;
    if (sizeEl) sizeEl.textContent = CONFIG.defaultFileSize;
    if (dateEl) dateEl.textContent = CONFIG.defaultDate;
    if (checksumShortEl) checksumShortEl.textContent = CONFIG.defaultChecksum.substring(0, 10) + '...';
    window.currentChecksum = CONFIG.defaultChecksum;
  }
}

/**
 * Format ISO date string into DD/MM/YYYY
 */
function formatDate(isoString) {
  try {
    const date = new Date(isoString);
    const d = String(date.getDate()).padStart(2, '0');
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const y = date.getFullYear();
    return `${d}/${m}/${y}`;
  } catch {
    return CONFIG.defaultDate;
  }
}

/**
 * Clipboard copy actions for checksum and powershell command
 */
function initCopyActions() {
  const copyChecksumBtn = document.getElementById('btnCopyChecksum');
  if (copyChecksumBtn) {
    copyChecksumBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const textToCopy = window.currentChecksum || CONFIG.defaultChecksum;
      copyToClipboard(textToCopy, 'Đã sao chép mã SHA-256 vào bộ nhớ tạm!');
    });
  }

  const copyCodeBtns = document.querySelectorAll('.btn-copy-code');
  copyCodeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const codeTarget = btn.getAttribute('data-code');
      if (codeTarget) {
        copyToClipboard(codeTarget, 'Đã sao chép lệnh cài đặt Driver!');
      }
    });
  });
}

function copyToClipboard(text, successMsg) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => showToast(successMsg));
  } else {
    // Fallback
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      showToast(successMsg);
    } catch {
      showToast('Không thể sao chép tự động!');
    }
    document.body.removeChild(textArea);
  }
}

/**
 * Lightweight Toast Notification
 */
function showToast(message) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

/**
 * FAQ Accordion handling
 */
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    questionBtn.addEventListener('click', () => {
      const isActive = item.classList.contains('active');

      // Close all others
      faqItems.forEach(other => {
        if (other !== item) {
          other.classList.remove('active');
          const otherAns = other.querySelector('.faq-answer');
          if (otherAns) otherAns.style.maxHeight = null;
        }
      });

      // Toggle current
      if (!isActive) {
        item.classList.add('active');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      } else {
        item.classList.remove('active');
        answer.style.maxHeight = null;
      }
    });
  });
}

/**
 * Report Catalog Tab Filtering
 */
function initReportTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const reportCards = document.querySelectorAll('.report-item-card');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-tab');

      reportCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/**
 * Download Modal Interaction with Auto-Trigger
 */
function initDownloadModal() {
  const modal = document.getElementById('downloadModal');
  const closeBtn = document.getElementById('closeModalBtn');
  const downloadBtns = document.querySelectorAll('.trigger-download-modal');

  downloadBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // Allow the actual download to proceed
      if (modal) {
        modal.classList.add('open');
      }
    });
  });

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => modal.classList.remove('open'));
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('open');
    });
  }
}

/**
 * Header shadow on scroll
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  });
}

/**
 * Mobile Drawer Menu
 */
function initMobileMenu() {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', () => {
      const isExpanded = navLinks.style.display === 'flex';
      if (isExpanded) {
        navLinks.style.display = '';
      } else {
        navLinks.style.display = 'flex';
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '72px';
        navLinks.style.left = '0';
        navLinks.style.width = '100%';
        navLinks.style.background = '#FFFFFF';
        navLinks.style.padding = '24px';
        navLinks.style.boxShadow = '0 10px 15px -3px rgba(0,0,0,0.1)';
        navLinks.style.borderBottom = '1px solid #E2E8F0';
        navLinks.style.zIndex = '99';
      }
    });
  }
}
