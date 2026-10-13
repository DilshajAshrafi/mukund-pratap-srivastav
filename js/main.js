/**
 * Mukund Pratap Srivastav — Portfolio Interactive Engine
 * Handles animations, terminal emulator, project interactions, and backend API integration.
 * Palette: Ivory greenish white, Burgundy reddish copper shine, Gold texture & Bluish off
 */

document.addEventListener('DOMContentLoaded', () => {
  initParticles();
  initTheme();
  initTypewriter();
  initMobileNav();
  initProjectFilters();
  initProjectLikes();
  initTerminal();
  initContactForm();
  initBackendStatus();
  initSmoothScroll();
});

/* ==========================================================================
   1. Interactive Gold & Copper Stardust Canvas Background
   ========================================================================== */
function initParticles() {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particleCount = Math.min(Math.floor(width / 22), 65);
  const particles = [];

  // Colors: Gold texture shimmer, Reddish Copper shine, Burgundy, and Ivory Greenish White
  const colors = [
    '212, 175, 55',  // Classic Gold
    '200, 103, 65',  // Copper Shine
    '253, 245, 196', // Light Gold Shimmer
    '116, 21, 47',   // Velvet Burgundy
    '242, 247, 242'  // Ivory Greenish White
  ];

  let mouse = { x: null, y: null, radius: 140 };

  window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
  });

  window.addEventListener('mouseout', () => {
    mouse.x = null;
    mouse.y = null;
  });

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 2 + 0.8,
      alpha: Math.random() * 0.65 + 0.3,
      color: colors[Math.floor(Math.random() * colors.length)]
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // Mouse proximity interaction
      if (mouse.x && mouse.y) {
        const mdx = p.x - mouse.x;
        const mdy = p.y - mouse.y;
        const mDist = Math.sqrt(mdx * mdx + mdy * mdy);
        if (mDist < mouse.radius) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(212, 175, 55, ${(1 - mDist / mouse.radius) * 0.28})`;
          ctx.lineWidth = 0.9;
          ctx.stroke();
        }
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color}, ${p.alpha})`;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(212, 175, 55, ${(1 - dist / 120) * 0.18})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(render);
  }
  render();
}

/* ==========================================================================
   2. Theme Manager (Dark / Light)
   ========================================================================== */
function initTheme() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const savedTheme = localStorage.getItem('mps_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(toggleBtn, savedTheme);

  toggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('mps_theme', newTheme);
    updateThemeIcon(toggleBtn, newTheme);
  });
}

function updateThemeIcon(btn, theme) {
  if (theme === 'light') {
    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
    btn.setAttribute('title', 'Switch to Dark Mode');
  } else {
    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
    btn.setAttribute('title', 'Switch to Light Mode');
  }
}

/* ==========================================================================
   3. Typewriter Animation
   ========================================================================== */
function initTypewriter() {
  const target = document.getElementById('typewriter');
  if (!target) return;

  const roles = [
    'Software Engineer',
    'Full-Stack Developer',
    'Cloud & Distributed Systems Architect',
    'Algorithm & Clean Code Specialist',
    'Tech Innovator'
  ];

  let roleIdx = 0;
  let charIdx = 0;
  let isDeleting = false;
  const typeSpeed = 95;
  const deleteSpeed = 45;
  const pauseEnd = 1800;

  function type() {
    const current = roles[roleIdx];
    if (isDeleting) {
      target.textContent = current.substring(0, charIdx - 1);
      charIdx--;
    } else {
      target.textContent = current.substring(0, charIdx + 1);
      charIdx++;
    }

    let delay = isDeleting ? deleteSpeed : typeSpeed;

    if (!isDeleting && charIdx === current.length) {
      delay = pauseEnd;
      isDeleting = true;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      roleIdx = (roleIdx + 1) % roles.length;
      delay = 400;
    }

    setTimeout(type, delay);
  }
  type();
}

/* ==========================================================================
   4. Mobile Navigation
   ========================================================================== */
function initMobileNav() {
  const hamburger = document.getElementById('hamburger-btn');
  const navMenu = document.getElementById('nav-menu');
  if (!hamburger || !navMenu) return;

  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('open');
  });

  navMenu.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
    });
  });
}

/* ==========================================================================
   5. Project Filter Tabs
   ========================================================================== */
function initProjectFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
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

/* ==========================================================================
   6. Project Likes Engine (Live Sync with SQLite)
   ========================================================================== */
function initProjectLikes() {
  fetch('/api/projects/likes')
    .then(res => res.json())
    .then(data => {
      if (data && data.projects) {
        Object.entries(data.projects).forEach(([id, stats]) => {
          const counter = document.getElementById(`likes-${id}`);
          if (counter) counter.textContent = stats.likes_count;
        });
      }
    })
    .catch(() => {});

  document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const projectId = btn.getAttribute('data-project');
      const counter = document.getElementById(`likes-${projectId}`);

      btn.classList.add('liked');

      try {
        const res = await fetch('/api/projects/like', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ projectId })
        });
        const result = await res.json();
        if (result.success && counter) {
          counter.textContent = result.likes;
        }
      } catch (e) {
        if (counter) {
          counter.textContent = parseInt(counter.textContent || '0') + 1;
        }
      }
    });
  });
}

/* ==========================================================================
   7. Interactive CLI Terminal Emulator
   ========================================================================== */
function initTerminal() {
  const terminalInput = document.getElementById('terminal-input');
  const terminalOutput = document.getElementById('terminal-output');
  if (!terminalInput || !terminalOutput) return;

  const commandResponses = {
    help: `Available commands:
• about       - Overview of Mukund Pratap Srivastav's background & philosophy
• skills      - List core engineering technologies & tools
• projects    - Summary of featured engineering systems
• stats       - Query live backend & database analytics
• contact     - Display contact channels and email
• hire        - Quick message for technical roles & collaboration
• clear       - Clear the terminal screen`,
    
    about: `Mukund Pratap Srivastav — Software Engineer & Systems Architect.
Specializes in high-throughput backend services, modern responsive web applications,
and cloud-native distributed computing with clean, maintainable architecture.`,

    skills: `Core Technical Skills:
• Languages:     Python, JavaScript (ES6+), TypeScript, C/C++, SQL
• Frameworks:    Flask, FastAPI, Node.js, Express, React
• Databases:     PostgreSQL, SQLite, Redis, MongoDB
• Cloud/DevOps:  Docker, AWS, Git, CI/CD Pipelines, Linux/Nginx`,

    projects: `Featured Projects:
1. Cloud-Native Microservices Platform — Distributed, auto-scaling backend suite
2. Smart Agro & IoT Analytics Engine   — High-throughput telemetry and insights
3. Real-Time Collaborative Studio      — WebSocket-driven code editor
4. DevPulse Observability Suite        — Real-time system monitoring`,

    contact: `Contact Mukund Pratap Srivastav:
• Email:    mukund.tech.dev@gmail.com
• Status:   Available for Full-Time Roles & Consulting
• Location: India`,

    hire: `Thank you for your interest!
Please scroll to the Contact section below or email mukund.tech.dev@gmail.com
to connect regarding engineering roles, technical collaboration, or inquiries.`
  };

  terminalInput.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
      const rawCmd = terminalInput.value.trim();
      terminalInput.value = '';

      if (!rawCmd) return;

      appendTerminalLine(`mps@portfolio:~$ ${rawCmd}`, 'prompt-echo');

      const cmd = rawCmd.toLowerCase();

      if (cmd === 'clear') {
        terminalOutput.innerHTML = '';
        return;
      }

      if (cmd === 'stats' || cmd === 'db') {
        try {
          const res = await fetch('/api/terminal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cmd })
          });
          const data = await res.json();
          if (data.output) {
            appendTerminalLine(data.output, data.status || 'info');
            return;
          }
        } catch (err) {}
      }

      if (commandResponses[cmd]) {
        appendTerminalLine(commandResponses[cmd], 'info');
      } else {
        appendTerminalLine(`Command not found: "${rawCmd}". Type 'help' for available commands.`, 'error');
      }

      const body = terminalOutput.closest('.terminal-body');
      if (body) body.scrollTop = body.scrollHeight;
    }
  });

  function appendTerminalLine(text, type = 'info') {
    const p = document.createElement('p');
    p.className = `terminal-line ${type}`;
    p.style.whiteSpace = 'pre-wrap';
    p.textContent = text;
    terminalOutput.appendChild(p);
  }
}

/* ==========================================================================
   8. Contact Form Handler (AJAX + Direct Gmail Fallback)
   ========================================================================== */
function initContactForm() {
  const form = document.getElementById('contact-form');
  const feedback = document.getElementById('form-feedback');
  const submitBtn = document.getElementById('submit-btn');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const subject = form.subject.value.trim();
    const message = form.message.value.trim();

    if (!name || !email || !message) {
      showFeedback('Please fill out all required fields.', 'error');
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending Message...';
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, subject, message })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showFeedback(result.message || 'Message sent successfully!', 'success');
        form.reset();

        if (result.gmail_compose_url && !result.email_sent) {
          const openGmailBtn = document.createElement('a');
          openGmailBtn.href = result.gmail_compose_url;
          openGmailBtn.target = '_blank';
          openGmailBtn.className = 'btn btn-outline btn-sm';
          openGmailBtn.style.marginTop = '10px';
          openGmailBtn.style.display = 'inline-block';
          openGmailBtn.textContent = 'Open in Gmail Web';
          feedback.appendChild(document.createElement('br'));
          feedback.appendChild(openGmailBtn);
        }
      } else {
        showFeedback(result.error || 'Failed to deliver message. Please try again.', 'error');
      }
    } catch (err) {
      // Fallback direct Gmail link if backend is unreachable
      const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=mukund.tech.dev@gmail.com&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
      showFeedback(`Server communication issue. Click below to compose directly in Gmail:`, 'error');
      const directBtn = document.createElement('a');
      directBtn.href = gmailUrl;
      directBtn.target = '_blank';
      directBtn.className = 'btn btn-outline btn-sm';
      directBtn.style.marginTop = '10px';
      directBtn.style.display = 'inline-block';
      directBtn.textContent = 'Compose in Gmail';
      feedback.appendChild(document.createElement('br'));
      feedback.appendChild(directBtn);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
      }
    }
  });

  function showFeedback(msg, type) {
    if (!feedback) return;
    feedback.textContent = msg;
    feedback.className = `form-feedback ${type}`;
    feedback.style.display = 'block';
  }
}

/* ==========================================================================
   9. Backend Health & Status Checker
   ========================================================================== */
function initBackendStatus() {
  const pill = document.getElementById('backend-status-pill');
  const dot = document.getElementById('backend-status-dot');
  const text = document.getElementById('backend-status-text');

  fetch('/api/health')
    .then(r => r.json())
    .then(data => {
      if (data && data.status === 'healthy') {
        if (text) text.textContent = '🟢 Full-Stack Engine Online (Flask + SQLite)';
        if (dot) dot.style.background = '#e27d53';
      }
    })
    .catch(() => {
      if (text) text.textContent = '⚡ Frontend Mode (Static Engine)';
      if (dot) dot.style.background = '#d4af37';
    });
}

/* ==========================================================================
   10. Smooth Scroll & Active Nav Spy
   ========================================================================== */
function initSmoothScroll() {
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 120;
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}
