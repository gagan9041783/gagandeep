/**
 * Gagandeep Kaur — Professional Portfolio
 * Core Interactivity, Canvas Network, Filtering, Modals & Form Handling
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initHeroCanvas();
  initPortfolioFilters();
  initCaseStudyModals();
  initContactForm();
  initScrollReveal();
  initAiConversation();
});

/* ==========================================================================
   1. NAVBAR & SCROLL SPY
   ========================================================================== */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  // Scroll effect on header
  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Scroll Spy active state
    let current = '';
    const scrollPosition = window.pageYOffset + 120;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });

  // Mobile menu toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('open');
      navToggle.classList.toggle('open', isOpen);
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu on nav link click
    navLinks.forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close mobile menu if clicked outside
    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target) && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
}

/* ==========================================================================
   2. HERO INTERACTIVE CANVAS (Governance & Data Nodes)
   ========================================================================== */
function initHeroCanvas() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = canvas.parentElement.offsetWidth);
  let height = (canvas.height = canvas.parentElement.offsetHeight);

  window.addEventListener('resize', () => {
    if (!canvas.parentElement) return;
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
  }, { passive: true });

  const numParticles = Math.min(Math.floor((width * height) / 18000), 55);
  const particles = [];

  const colors = [
    'rgba(16, 185, 129, 0.45)', // Emerald
    'rgba(27, 61, 112, 0.35)',  // Deep Navy
    'rgba(245, 158, 11, 0.35)',  // Warm Gold
  ];

  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      radius: Math.random() * 2.2 + 1.2,
      color: colors[Math.floor(Math.random() * colors.length)],
    });
  }

  let mouse = { x: -1000, y: -1000 };
  const heroSection = document.getElementById('hero');
  if (heroSection) {
    heroSection.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }, { passive: true });

    heroSection.addEventListener('mouseleave', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    // Draw connecting lines between close particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(16, 185, 129, ${0.18 * (1 - dist / 130)})`;
          ctx.lineWidth = 0.9;
          ctx.stroke();
        }
      }

      // Draw line to mouse if nearby
      const mdx = particles[i].x - mouse.x;
      const mdy = particles[i].y - mouse.y;
      const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
      if (mdist < 140) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.strokeStyle = `rgba(245, 158, 11, ${0.28 * (1 - mdist / 140)})`;
        ctx.lineWidth = 1.2;
        ctx.stroke();
      }
    }

    // Draw and update particles
    particles.forEach((p) => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();

      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;
    });

    requestAnimationFrame(draw);
  }

  draw();
}

/* ==========================================================================
   3. PORTFOLIO FILTERING
   ========================================================================== */
function initPortfolioFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  if (!filterBtns.length || !projectCards.length) return;

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      // Toggle active button
      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach((card) => {
        const cardCategory = card.getAttribute('data-category');

        if (filter === 'all' || cardCategory === filter) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(12px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 200);
        }
      });
    });
  });
}

/* ==========================================================================
   4. CASE STUDY DETAIL MODALS
   ========================================================================== */
function initCaseStudyModals() {
  const openButtons = document.querySelectorAll('.open-case-study-btn');
  const modals = document.querySelectorAll('.modal-backdrop');

  function openModal(modalId) {
    const targetModal = document.getElementById(modalId);
    if (!targetModal) return;

    targetModal.classList.add('open');
    targetModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Lock background scroll
  }

  function closeModal(modal) {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = ''; // Unlock background scroll
  }

  openButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const modalId = btn.getAttribute('data-modal');
      openModal(modalId);
    });
  });

  modals.forEach((modal) => {
    // Close button click
    const closeBtn = modal.querySelector('.modal-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => closeModal(modal));
    }

    // Backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });

  // ESC key to close any open modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModalElem = document.querySelector('.modal-backdrop.open');
      if (openModalElem) {
        closeModal(openModalElem);
      }
    }
  });
}

/* ==========================================================================
   5. CONTACT FORM VALIDATION & FEEDBACK
   ========================================================================== */
function initContactForm() {
  const form = document.getElementById('portfolio-contact-form');
  const successAlert = document.getElementById('form-success-message');

  if (!form || !successAlert) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const nameInput = document.getElementById('contact-name');
    const emailInput = document.getElementById('contact-email');
    const messageInput = document.getElementById('contact-message');

    let isValid = true;

    [nameInput, emailInput, messageInput].forEach((input) => {
      if (!input.value.trim()) {
        input.style.borderColor = '#ef4444';
        isValid = false;
      } else {
        input.style.borderColor = '';
      }
    });

    // Basic email format check
    if (emailInput.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim())) {
      emailInput.style.borderColor = '#ef4444';
      isValid = false;
    }

    if (!isValid) return;

    // Simulate successful submission
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span>Sending...</span> <i class="ri-loader-4-line ri-spin"></i>`;

    setTimeout(() => {
      successAlert.classList.add('show');
      form.reset();
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;

      // Smooth scroll alert into view
      successAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

      // Automatically hide alert after 10 seconds
      setTimeout(() => {
        successAlert.classList.remove('show');
      }, 10000);
    }, 800);
  });
}

/* ==========================================================================
   6. SCROLL REVEAL ANIMATIONS
   ========================================================================== */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal-on-scroll');

  if (!('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    },
    {
      root: null,
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  reveals.forEach((el) => observer.observe(el));
}

/* ==========================================================================
   7. AI CONVERSATION (LangChain Model Integration)
   ========================================================================== */
function initAiConversation() {
  const modal = document.getElementById('ai-chat-modal');
  const openButtons = document.querySelectorAll('.btn-start-conversation');
  const closeBtn = document.getElementById('ai-chat-close-btn');
  const chatForm = document.getElementById('ai-chat-form');
  const chatInput = document.getElementById('ai-chat-input');
  const chatBody = document.getElementById('ai-chat-body');
  const suggestionChips = document.querySelectorAll('.suggestion-chip');

  if (!modal || !chatForm || !chatInput || !chatBody) return;

  const conversationHistory = [];

  function openConversation() {
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => chatInput.focus(), 250);
  }

  function closeConversation() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
  }

  openButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openConversation();
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeConversation);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeConversation();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeConversation();
    }
  });

  // Helper to format basic markdown (bold, lists, links)
  function formatMarkdown(text) {
    let formatted = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" style="color:#059669; text-decoration:underline;">$1</a>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n• (.*?)(?=(\n|$))/g, '<br>• $1')
      .replace(/\n1\. (.*?)(?=(\n|$))/g, '<br>1. $1')
      .replace(/\n2\. (.*?)(?=(\n|$))/g, '<br>2. $1')
      .replace(/\n3\. (.*?)(?=(\n|$))/g, '<br>3. $1')
      .replace(/\n4\. (.*?)(?=(\n|$))/g, '<br>4. $1')
      .replace(/\n5\. (.*?)(?=(\n|$))/g, '<br>5. $1')
      .replace(/\n/g, '<br>');

    return `<p>${formatted}</p>`;
  }

  function appendMessage(sender, text) {
    const msgEl = document.createElement('div');
    msgEl.className = `chat-message ${sender === 'user' ? 'user-message' : 'assistant-message'}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'You' : 'GK';

    const content = document.createElement('div');
    content.className = 'message-content';

    if (sender === 'user') {
      const p = document.createElement('p');
      p.textContent = text;
      content.appendChild(p);
    } else {
      content.innerHTML = formatMarkdown(text);
    }

    msgEl.appendChild(avatar);
    msgEl.appendChild(content);
    chatBody.appendChild(msgEl);
    chatBody.scrollTop = chatBody.scrollHeight;

    conversationHistory.push({ sender: sender === 'user' ? 'User' : 'Assistant', text });
  }

  function showTypingIndicator() {
    const typingEl = document.createElement('div');
    typingEl.className = 'chat-message assistant-message typing-indicator-item';
    typingEl.id = 'chat-typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'GK';

    const bubble = document.createElement('div');
    bubble.className = 'typing-bubble';
    bubble.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

    typingEl.appendChild(avatar);
    typingEl.appendChild(bubble);
    chatBody.appendChild(typingEl);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById('chat-typing-indicator');
    if (indicator) indicator.remove();
  }

  // Fallback client-side generator in case website is opened offline or via file:///
  function generateLocalFallback(prompt) {
    const p = prompt.toLowerCase();
    if (p.includes('undp') || p.includes('experience') || p.includes('vaccine') || p.includes('cold chain')) {
      return "🏛️ **Gagandeep Kaur's UNDP & Health Experience:**\n\n• **U-WIN Coordinator (UNDP, Patiala):** Coordinated immunization and digital tracking under the U-WIN platform, managed cold chain logistics, and oversaw MIS data monitoring.\n• **Vaccine & Cold Chain Manager (UNDP, Tarn Taran):** Supervised district vaccine logistics, ensured WHO temperature compliance, and trained healthcare personnel.\n• **MIS Assistant (TB Alert India, Patiala):** Managed TB program data records, monitored treatment adherence, and delivered district health reports.";
    }
    if (p.includes('mis') || p.includes('excel') || p.includes('data') || p.includes('dashboard')) {
      return "📊 **MIS & Data Analytics:**\n\nGagandeep specializes in building reliable data systems:\n• **MIS Architecture:** Standardized input forms, data validation rules, and automated reporting.\n• **Advanced Excel:** Complex dynamic models utilizing XLOOKUP, INDEX-MATCH, SUMIFS, Pivot Tables, and interactive dashboard slicers.\n• **Relational Databases:** SQL schema design, normalized tables, and multi-table analytical JOINs.";
    }
    if (p.includes('ads') || p.includes('google') || p.includes('ppc') || p.includes('keyword')) {
      return "🎯 **Google Ads / PPC Campaigns:**\n\n• Intent-driven Google Search Ads campaign planning\n• Keyword research and negative keyword master lists to eliminate wasted spend\n• Single-theme ad groups with customized copy and extensions\n• Conversion tracking and CPC / CPA optimization\n*(Note: Portfolio campaign is a sample project for local home services).*";
    }
    if (p.includes('ai') || p.includes('langchain') || p.includes('python')) {
      return "🤖 **AI & LangChain Solutions:**\n\nGagandeep develops modern AI and data pipelines:\n• **LangChain:** Prompt orchestration, RAG document search, and structured output parsing\n• **Python:** Data processing with Pandas, automated API workflows, and machine learning concepts.";
    }
    if (p.includes('contact') || p.includes('hire') || p.includes('collaborate') || p.includes('email')) {
      return "📬 **Let's Connect:**\n\n• **Email:** [gagan9041783@gmail.com](mailto:gagan9041783@gmail.com)\n• **Phone:** +91 9041783035\n• **Location:** Mohali, Punjab, India\n• **LinkedIn:** [Gagandeep Kaur](https://www.linkedin.com/in/gagandeepkaur25?utm_source=share_via&utm_content=profile&utm_medium=member_android)\n• **Upwork:** [Freelance Profile](https://www.upwork.com/freelancers/~012d7b4c25524f13a6?mp_source=share)";
    }
    return "Thank you for reaching out! Gagandeep Kaur brings a strong blend of **governance and development leadership (UNDP)**, **data analysis (MIS, Advanced Excel)**, and **technology (Python, SQL, LangChain AI, Google Ads)**.\n\nWould you like more details on her experience, services, projects, or how to get in touch?";
  }

  async function handleUserSend(messageText) {
    const text = messageText.trim();
    if (!text) return;

    appendMessage('user', text);
    chatInput.value = '';
    showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: conversationHistory })
      });

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      removeTypingIndicator();
      appendMessage('assistant', data.reply || 'Thank you for your message.');
    } catch (err) {
      // Graceful local fallback if offline or served via file:///
      setTimeout(() => {
        removeTypingIndicator();
        const fallbackReply = generateLocalFallback(text);
        appendMessage('assistant', fallbackReply);
      }, 500);
    }
  }

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleUserSend(chatInput.value);
  });

  // Quick suggestion chips
  suggestionChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-prompt');
      if (prompt) {
        handleUserSend(prompt);
      }
    });
  });
}
