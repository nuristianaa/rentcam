<template>
  <div class="about-page">

    <!-- ── HERO ─────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero__bg">
        <div class="hero__grid" />
        <div class="hero__orb hero__orb--1" />
        <div class="hero__orb hero__orb--2" />
      </div>

      <div class="hero__inner">
        <div class="hero__badge">
          <q-icon name="camera_alt" size="14px" />
          RENTCAM · Bandung
        </div>
        <h1 class="hero__title">
          Photo Rental Platform<br />
          <span class="hero__title--accent">Trusted in Bandung</span>
        </h1>
        <p class="hero__sub">
          We are here to easily help anyone access high-quality photo equipment — without needing to buy them. From cameras, lenses, drones, and lighting.
        </p>
        <div class="hero__actions">
          <router-link to="/rental/user/items" class="btn btn--primary">
            <q-icon name="camera_alt" size="16px" />
            View Collection
          </router-link>
          <router-link to="/rental/user/faq" class="btn btn--ghost">
            <q-icon name="help_outline" size="15px" />
            Help Center
          </router-link>
        </div>
      </div>
    </section>

    <!-- ── STATS ─────────────────────────────────────────────── -->
    <section class="stats">
      <div class="stats__inner">
        <div v-for="stat in stats" :key="stat.label" class="stat-card">
          <div class="stat-card__icon">
            <q-icon :name="stat.icon" size="22px" />
          </div>
          <div class="stat-card__num">{{ stat.num }}</div>
          <div class="stat-card__label">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- ── STORY ─────────────────────────────────────────────── -->
    <section class="story">
      <div class="story__inner">
        <div class="story__text">
          <div class="section-tag">
            <q-icon name="auto_stories" size="13px" />
            Our Story
          </div>
          <h2 class="section-title">From a School Project,<br /><em>for Everyone.</em></h2>
          <p class="story__body">
            RENTCAM was born from a real concern: expensive photo equipment, limited budgets, but unstoppable creativity. Starting as a vocational school project in Bandung, we built a platform that allows anyone — from students, content creators, to professional photographers — to access high-quality equipment without having to buy.
          </p>
          <p class="story__body">
            Our system is simple: online booking, bank transfer and WhatsApp confirmation, then visit our store to directly pick up the equipment. Everything is documented transparently and in real-time.
          </p>
          <div class="story__tags">
            <span class="tag">
              <q-icon name="school" size="12px" />
              Vocational Project
            </span>
            <span class="tag">
              <q-icon name="location_on" size="12px" />
              Bandung, West Java
            </span>
            <span class="tag">
              <q-icon name="emoji_objects" size="12px" />
              Local Innovation
            </span>
          </div>
        </div>

        <div class="story__visual">
          <div class="timeline">
            <div v-for="(ev, i) in timeline" :key="i" class="tl-item">
              <div class="tl-dot">
                <q-icon :name="ev.icon" size="18px" />
              </div>
              <div class="tl-line" v-if="i < timeline.length - 1" />
              <div class="tl-content">
                <div class="tl-year">{{ ev.year }}</div>
                <div class="tl-title">{{ ev.title }}</div>
                <div class="tl-desc">{{ ev.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── ALUR SISTEM ────────────────────────────────────────── -->
    <section class="flow">
      <div class="flow__inner">
        <div class="section-tag" style="margin: 0 auto 14px">
          <q-icon name="alt_route" size="13px" />
          System Flow
        </div>
        <h2 class="section-title" style="text-align:center">
          How Our System<br /><em>Works</em>
        </h2>
        <div class="flow-steps">
          <div v-for="(step, i) in flowSteps" :key="i" class="flow-step">
            <div class="flow-step__num">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="flow-step__icon">
              <q-icon :name="step.icon" size="22px" />
            </div>
            <div class="flow-step__title">{{ step.title }}</div>
            <div class="flow-step__desc">{{ step.desc }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── FITUR ──────────────────────────────────────────────── -->
    <section class="features">
      <div class="features__inner">
        <div class="section-tag" style="margin: 0 auto 14px">
          <q-icon name="star_outline" size="13px" />
          Our Advantages
        </div>
        <h2 class="section-title" style="text-align:center">
          What Makes Us<br /><em>Different</em>
        </h2>
        <div class="feat-grid">
          <div v-for="feat in features" :key="feat.title" class="feat-card">
            <div class="feat-card__icon">
              <q-icon :name="feat.icon" size="22px" />
            </div>
            <h3 class="feat-card__title">{{ feat.title }}</h3>
            <p class="feat-card__desc">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── TIM ────────────────────────────────────────────────── -->
    <section class="team">
      <div class="team__inner">
        <div class="section-tag" style="margin: 0 auto 14px">
          <q-icon name="groups" size="13px" />
          Our Team
        </div>
        <h2 class="section-title" style="text-align:center">
          People<br /><em>Behind the Scenes</em>
        </h2>
        <div class="team__grid">
          <div v-for="member in team" :key="member.name" class="member-card">
            <div class="member-card__avatar" :style="{ background: member.bg }">
              <span class="member-card__initials">{{ member.initials }}</span>
            </div>
            <div class="member-card__name">{{ member.name }}</div>
            <div class="member-card__role">{{ member.role }}</div>
            <div class="member-card__tags">
              <span v-for="t in member.tags" :key="t" class="member-tag">{{ t }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── LOKASI ─────────────────────────────────────────────── -->
    <section class="location">
      <div class="location__inner">
        <div class="location__text">
          <div class="section-tag">
            <q-icon name="location_on" size="13px" />
            Our Location
          </div>
          <h2 class="section-title">We are in<br /><em>Bandung.</em></h2>
          <p class="location__body">
            Come directly to our basecamp or book online to secure your date. Pickup your gear directly from our store in Bandung.
          </p>
          <div class="location__info">
            <div class="loc-item">
              <div class="loc-item__icon">
                <q-icon name="home" size="18px" />
              </div>
              <div>
                <div class="loc-item__label">Address</div>
                <div class="loc-item__val">Bandung, West Java</div>
              </div>
            </div>
            <div class="loc-item">
              <div class="loc-item__icon">
                <q-icon name="schedule" size="18px" />
              </div>
              <div>
                <div class="loc-item__label">Operating Hours</div>
                <div class="loc-item__val">Monday–Saturday, 08:00–20:00 WIB</div>
              </div>
            </div>
            <div class="loc-item">
              <div class="loc-item__icon">
                <q-icon name="support_agent" size="18px" />
              </div>
              <div>
                <div class="loc-item__label">Contact via</div>
                <div class="loc-item__val">WhatsApp & Email</div>
              </div>
            </div>
          </div>
        </div>

        <div class="location__map">
          <div class="map-card">
            <div class="map-card__header">
              <q-icon name="location_on" size="16px" />
              <span>RENTCAM · Bandung, West Java</span>
            </div>
            <div class="map-card__body">
              <svg viewBox="0 0 320 230" xmlns="http://www.w3.org/2000/svg" class="map-svg">
                <rect width="320" height="230" fill="#f0f4ff"/>
                <line x1="0" y1="57"  x2="320" y2="57"  stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="0" y1="115" x2="320" y2="115" stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="0" y1="172" x2="320" y2="172" stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="64"  y1="0" x2="64"  y2="230" stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="128" y1="0" x2="128" y2="230" stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="192" y1="0" x2="192" y2="230" stroke="#c7d2fe" stroke-width="0.5"/>
                <line x1="256" y1="0" x2="256" y2="230" stroke="#c7d2fe" stroke-width="0.5"/>
                <path d="M0 105 Q90 95 160 115 Q230 135 320 110" stroke="#818cf8" stroke-width="3" fill="none" stroke-linecap="round"/>
                <path d="M0 145 Q105 140 165 148 Q225 155 320 143" stroke="#818cf8" stroke-width="2" fill="none" stroke-linecap="round"/>
                <path d="M138 0 Q144 64 146 115 Q148 165 143 230" stroke="#818cf8" stroke-width="3" fill="none" stroke-linecap="round"/>
                <rect x="20"  y="62"  width="52" height="30" rx="5" fill="#dde4ff" opacity="0.8"/>
                <rect x="20"  y="118" width="46" height="20" rx="5" fill="#dde4ff" opacity="0.8"/>
                <rect x="92"  y="62"  width="32" height="26" rx="5" fill="#dde4ff" opacity="0.8"/>
                <rect x="162" y="74"  width="56" height="30" rx="5" fill="#dde4ff" opacity="0.8"/>
                <rect x="210" y="62"  width="72" height="26" rx="5" fill="#dde4ff" opacity="0.8"/>
                <rect x="210" y="122" width="72" height="40" rx="5" fill="#dde4ff" opacity="0.8"/>
                <circle cx="155" cy="113" r="20" fill="rgba(26,51,122,0.12)"/>
                <circle cx="155" cy="113" r="11" fill="rgba(26,51,122,0.22)"/>
                <circle cx="155" cy="113" r="7"  fill="#1a337a"/>
                <rect x="108" y="82" width="94" height="18" rx="9" fill="#1a337a"/>
                <text x="155" y="94" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">RENTCAM</text>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ───────────────────────────────────────────────── -->
    <section class="cta">
      <div class="cta__inner">
        <div class="cta__icon">
          <q-icon name="camera_alt" size="28px" />
        </div>
        <h2 class="cta__title">Ready to start<br />your photography journey?</h2>
        <p class="cta__sub">Don't let expensive photo gear be a barrier to your creativity.</p>
        <div class="cta__actions">
          <router-link to="/rental/user/items" class="btn btn--primary btn--lg">
            <q-icon name="photo_camera" size="17px" />
            Rent Now
          </router-link>
          <router-link to="/rental/user/faq" class="btn btn--outline-white btn--lg">
            <q-icon name="help_outline" size="16px" />
            Read FAQ
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
const stats = [
  { icon: 'camera_alt',    num: '50+',  label: 'Available Equipments' },
  { icon: 'people',        num: '200+', label: 'Happy Customers' },
  { icon: 'star',          num: '4.9',  label: 'Average Rating' },
  { icon: 'support_agent', num: '24/7', label: 'Active Support' },
]

const timeline = [
  { icon: 'emoji_objects', year: '2023', title: 'First Idea',  desc: 'Born from a vocational assignment, emerged a vision for a local photo rental platform.' },
  { icon: 'build',         year: '2024', title: 'Built',     desc: 'A small team built the system from scratch with great enthusiasm.' },
  { icon: 'rocket_launch', year: '2025', title: 'Launched',  desc: 'The official platform went live and serves hundreds of Bandung customers.' },
  { icon: 'trending_up',   year: 'Now',  title: 'Growing',   desc: 'Continuing to innovate and expand our photo equipment collection.' },
]

const flowSteps = [
  { icon: 'search',           title: 'Choose Equipment',            desc: 'Browse the catalog, choose available equipment, and set booking dates.' },
  { icon: 'calendar_month',   title: 'Set Period',       desc: 'Select the start and end dates. The system checks stock availability in real-time.' },
  { icon: 'chat',             title: 'Transfer & Send WA',   desc: 'Transfer to our bank account, then send a photo receipt to WhatsApp admin for confirmation.' },
  { icon: 'fact_check',       title: 'Admin Verification',       desc: 'Admin verifies the transfer receipt and confirms your booking.' },
  { icon: 'storefront',       title: 'Store Pickup',          desc: 'Visit our store in Bandung on the start date. Equipment is ready and checked.' },
  { icon: 'task_alt',         title: 'Complete & Deposit',      desc: 'Return the equipment to the store. Condition checked together, full deposit returned if good.' },
]

const features = [
  { icon: 'payments',       title: 'Affordable Prices',   desc: 'Rent starting at pocket-friendly prices without compromising quality.' },
  { icon: 'verified',       title: 'Well-Maintained Equipment',        desc: 'Every equipment is checked and cleaned before hand-over at the store.' },
  { icon: 'storefront',     title: 'Store Pickup',      desc: 'Pickup and return directly to the store — no need to wait for courier.' },
  { icon: 'shield',         title: 'Transparent Deposit',  desc: 'Verified deposit system for the safety of all parties.' },
  { icon: 'chat',           title: 'WA Confirmation',  desc: 'Send transfer receipt to admin WhatsApp — fast confirmation within 2 hours.' },
  { icon: 'support_agent',  title: 'Responsive Support',   desc: 'Our team is ready to help at any time via WhatsApp.' },
]

const team = [
  { name: 'Backend Developer',  role: 'Laravel & API',       initials: 'BE', bg: 'linear-gradient(135deg,#0f2258,#1a337a)', tags: ['Laravel', 'REST API', 'Database'] },
  { name: 'Frontend Developer', role: 'Vue & UI/UX',         initials: 'FE', bg: 'linear-gradient(135deg,#1e3a8a,#2563eb)', tags: ['Vue 3', 'Quasar', 'UI/UX'] },
  { name: 'Project Manager',    role: 'Planning & Scrum', initials: 'PM', bg: 'linear-gradient(135deg,#1e3a8a,#0f2258)', tags: ['Figma', 'Scrum', 'Design'] },
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Design Tokens ──────────────────────────────────────────── */
.about-page {
  --navy-950: #030c1f;
  --navy-900: #060e2b;
  --navy-800: #0a1940;
  --navy-700: #0f2258;
  --navy-600: #1a337a;
  --navy-500: #1e3a8a;
  --navy-400: #2563eb;
  --navy-300: #3b82f6;
  --blue-100: #dbeafe;
  --blue-50:  #eff6ff;
  --gray-50:  #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;

  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  min-height: 100vh;
  background: var(--gray-50);
  color: var(--gray-800);
  overflow-x: hidden;
}

/* ── Shared ───────────────────────────────────────────────────── */
.section-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  padding: 5px 14px; border-radius: 999px;
  margin-bottom: 14px; border: 1px solid rgba(30,58,138,0.12);
  text-transform: uppercase;
}
.section-title {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 800; color: var(--gray-800);
  line-height: 1.25; margin: 0 0 20px; letter-spacing: -0.4px;
}
.section-title em { color: var(--navy-600); font-style: normal; }

/* ── Buttons ──────────────────────────────────────────────────── */
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px; border-radius: 10px;
  font-family: inherit; font-size: 14px; font-weight: 600;
  text-decoration: none; transition: all 0.2s; cursor: pointer; border: none;
  line-height: 1;
}
.btn--lg { padding: 14px 28px; font-size: 15px; }
.btn--primary {
  background: var(--navy-500); color: #fff;
  box-shadow: 0 4px 16px rgba(30,58,138,0.3);
}
.btn--primary:hover { background: var(--navy-600); transform: translateY(-2px); box-shadow: 0 8px 28px rgba(30,58,138,0.4); }
.btn--ghost {
  background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.85);
  border: 1.5px solid rgba(255,255,255,0.2);
}
.btn--ghost:hover { background: rgba(255,255,255,0.15); color: #fff; }
.btn--outline-white {
  background: transparent; color: rgba(255,255,255,0.75);
  border: 1.5px solid rgba(255,255,255,0.22);
}
.btn--outline-white:hover { background: rgba(255,255,255,0.08); color: #fff; border-color: rgba(255,255,255,0.4); }

/* ── Hero ─────────────────────────────────────────────────────── */
.hero {
  position: relative;
  background: var(--navy-950);
  padding: 100px 28px 80px;
  overflow: hidden;
  text-align: center;
}
.hero__bg { position: absolute; inset: 0; pointer-events: none; }
.hero__grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 52px 52px;
}
.hero__orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); pointer-events: none;
}
.hero__orb--1 { width: 500px; height: 500px; background: rgba(30,58,138,0.25); top: -150px; left: -100px; }
.hero__orb--2 { width: 400px; height: 400px; background: rgba(59,130,246,0.1); bottom: -100px; right: -60px; }
.hero__inner  { position: relative; max-width: 680px; margin: 0 auto; }

.hero__badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(59,130,246,0.1); backdrop-filter: blur(8px);
  border: 1px solid rgba(59,130,246,0.2);
  color: #93c5fd; font-size: 12px; font-weight: 600;
  letter-spacing: 0.08em; padding: 5px 16px;
  border-radius: 999px; margin-bottom: 22px;
}
.hero__title {
  font-size: clamp(28px, 5vw, 50px);
  font-weight: 800; color: #fff;
  line-height: 1.2; margin: 0 0 16px; letter-spacing: -0.4px;
}
.hero__title--accent { color: #93c5fd; }
.hero__sub { color: rgba(255,255,255,0.5); font-size: 15.5px; line-height: 1.75; margin: 0 0 28px; max-width: 540px; margin-left: auto; margin-right: auto; }
.hero__actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* ── Stats ────────────────────────────────────────────────────── */
.stats {
  background: #fff;
  border-bottom: 1px solid var(--gray-100);
  padding: 0 28px;
}
.stats__inner {
  max-width: 900px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(4, 1fr);
}
.stat-card {
  padding: 32px 16px; text-align: center;
  border-right: 1px solid var(--gray-100);
  transition: background 0.2s; cursor: default;
}
.stat-card:last-child { border-right: none; }
.stat-card:hover { background: var(--blue-50); }
.stat-card__icon {
  width: 46px; height: 46px; border-radius: 12px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; transition: background 0.2s;
}
.stat-card:hover .stat-card__icon { background: rgba(30,58,138,0.14); }
.stat-card__num { font-size: 26px; font-weight: 800; color: var(--navy-700); line-height: 1; margin-bottom: 5px; }
.stat-card__label { font-size: 12px; color: var(--gray-400); font-weight: 600; letter-spacing: 0.04em; }

/* ── Story ────────────────────────────────────────────────────── */
.story { background: #fff; padding: 80px 28px; }
.story__inner {
  max-width: 1000px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 64px; align-items: center;
}
.story__body { color: var(--gray-500); font-size: 15px; line-height: 1.8; margin: 0 0 14px; }
.story__tags { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 22px; }
.tag {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(30,58,138,0.06); border: 1.5px solid rgba(30,58,138,0.12);
  color: var(--navy-600); font-size: 12px; font-weight: 600;
  padding: 5px 14px; border-radius: 999px;
}

/* Timeline */
.timeline { display: flex; flex-direction: column; }
.tl-item  { display: flex; gap: 18px; position: relative; }
.tl-dot {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--navy-600);
  color: #fff; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; z-index: 1;
  box-shadow: 0 4px 14px rgba(30,58,138,0.3);
}
.tl-line {
  position: absolute; left: 21px; top: 44px;
  width: 2px; height: calc(100% + 12px);
  background: linear-gradient(to bottom, rgba(30,58,138,0.3), transparent);
}
.tl-content { padding: 8px 0 28px; }
.tl-year  { font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 500; color: var(--navy-400); letter-spacing: 0.12em; margin-bottom: 2px; }
.tl-title { font-size: 15px; font-weight: 700; color: var(--gray-800); margin-bottom: 4px; }
.tl-desc  { font-size: 13px; color: var(--gray-500); line-height: 1.65; }

/* ── Flow Steps ───────────────────────────────────────────────── */
.flow { background: var(--navy-950); padding: 80px 28px; }
.flow__inner { max-width: 1000px; margin: 0 auto; text-align: center; }
.flow__inner .section-tag {
  background: rgba(59,130,246,0.1); color: #93c5fd;
  border-color: rgba(59,130,246,0.2);
}
.flow__inner .section-title { color: #fff; }
.flow__inner .section-title em { color: #93c5fd; }
.flow-steps {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 16px; margin-top: 40px; text-align: left;
}
.flow-step {
  background: rgba(255,255,255,0.04);
  border: 1.5px solid rgba(255,255,255,0.07);
  border-radius: 16px; padding: 24px 20px;
  transition: all 0.22s;
}
.flow-step:hover {
  border-color: rgba(59,130,246,0.25);
  background: rgba(255,255,255,0.07);
  transform: translateY(-3px);
}
.flow-step__num {
  font-family: 'DM Mono', monospace;
  font-size: 11px; font-weight: 500; color: rgba(255,255,255,0.25);
  letter-spacing: 0.1em; margin-bottom: 12px;
}
.flow-step__icon {
  width: 44px; height: 44px;
  background: rgba(30,58,138,0.35);
  border: 1px solid rgba(59,130,246,0.2);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: #93c5fd; margin-bottom: 14px;
}
.flow-step__title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.flow-step__desc  { font-size: 12.5px; color: rgba(255,255,255,0.45); line-height: 1.65; }

/* ── Features ─────────────────────────────────────────────────── */
.features { background: #fff; padding: 80px 28px; }
.features__inner { max-width: 1000px; margin: 0 auto; text-align: center; }
.feat-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 16px; margin-top: 40px; text-align: left;
}
.feat-card {
  background: var(--gray-50); border: 1.5px solid var(--gray-100);
  border-radius: 16px; padding: 26px 22px;
  transition: all 0.22s; cursor: default;
}
.feat-card:hover {
  border-color: rgba(30,58,138,0.2); background: rgba(30,58,138,0.03);
  transform: translateY(-4px); box-shadow: 0 12px 32px rgba(30,58,138,0.1);
}
.feat-card__icon {
  width: 46px; height: 46px; border-radius: 12px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 16px; transition: background 0.2s;
}
.feat-card:hover .feat-card__icon { background: rgba(30,58,138,0.14); }
.feat-card__title { font-size: 15px; font-weight: 700; color: var(--gray-800); margin-bottom: 8px; }
.feat-card__desc  { font-size: 13px; color: var(--gray-500); line-height: 1.7; margin: 0; }

/* ── Team ─────────────────────────────────────────────────────── */
.team { background: rgba(30,58,138,0.04); padding: 80px 28px; }
.team__inner { max-width: 820px; margin: 0 auto; text-align: center; }
.team__grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 20px; margin-top: 40px;
}
.member-card {
  background: #fff; border: 1.5px solid var(--gray-100);
  border-radius: 20px; padding: 30px 20px 22px;
  transition: all 0.22s;
}
.member-card:hover {
  border-color: rgba(30,58,138,0.2); transform: translateY(-5px);
  box-shadow: 0 16px 40px rgba(30,58,138,0.1);
}
.member-card__avatar {
  width: 72px; height: 72px; border-radius: 50%;
  margin: 0 auto 14px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 20px rgba(10,25,64,0.25);
}
.member-card__initials { font-size: 20px; font-weight: 800; color: #fff; letter-spacing: 0.04em; }
.member-card__name { font-size: 15px; font-weight: 700; color: var(--gray-800); margin-bottom: 4px; }
.member-card__role { font-size: 12px; color: var(--gray-400); font-weight: 500; margin-bottom: 12px; }
.member-card__tags { display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; }
.member-tag {
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  font-size: 10px; font-weight: 600;
  padding: 3px 10px; border-radius: 999px;
  border: 1px solid rgba(30,58,138,0.12);
}

/* ── Location ─────────────────────────────────────────────────── */
.location { background: #fff; padding: 80px 28px; }
.location__inner {
  max-width: 1000px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 56px; align-items: center;
}
.location__body { color: var(--gray-500); font-size: 15px; line-height: 1.8; margin: 0 0 24px; }
.location__info { display: flex; flex-direction: column; gap: 12px; }
.loc-item {
  display: flex; align-items: center; gap: 14px;
  background: var(--gray-50); border: 1.5px solid var(--gray-100);
  border-radius: 12px; padding: 14px 16px; transition: border-color 0.18s;
}
.loc-item:hover { border-color: rgba(30,58,138,0.2); }
.loc-item__icon {
  width: 40px; height: 40px; border-radius: 10px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.loc-item__label { font-size: 10.5px; font-weight: 700; color: var(--gray-400); letter-spacing: 0.06em; margin-bottom: 2px; text-transform: uppercase; }
.loc-item__val   { font-size: 13.5px; font-weight: 600; color: var(--gray-700); }
.map-card {
  background: rgba(30,58,138,0.04); border: 2px solid rgba(30,58,138,0.1);
  border-radius: 20px; overflow: hidden;
  box-shadow: 0 8px 32px rgba(30,58,138,0.1);
}
.map-card__header {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 16px; background: var(--navy-700);
  color: #fff; font-size: 13px; font-weight: 600;
}
.map-card__body { padding: 8px; }
.map-svg { width: 100%; border-radius: 12px; display: block; }

/* ── CTA ──────────────────────────────────────────────────────── */
.cta {
  position: relative; overflow: hidden;
  background: var(--navy-950);
  padding: 80px 28px; text-align: center;
}
.cta__inner { position: relative; max-width: 520px; margin: 0 auto; }
.cta__icon {
  width: 64px; height: 64px; border-radius: 18px;
  background: rgba(59,130,246,0.12);
  border: 1.5px solid rgba(59,130,246,0.2);
  color: #93c5fd;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 22px;
}
.cta__title {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 800; color: #fff; line-height: 1.25; margin: 0 0 14px;
  letter-spacing: -0.4px;
}
.cta__sub { color: rgba(255,255,255,0.45); font-size: 15px; margin-bottom: 32px; line-height: 1.65; }
.cta__actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* ── Responsive ────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .stats__inner { grid-template-columns: repeat(2, 1fr); }
  .stat-card:nth-child(2) { border-right: none; }
  .story__inner, .location__inner { grid-template-columns: 1fr; gap: 36px; }
  .flow-steps { grid-template-columns: repeat(2, 1fr); }
  .feat-grid { grid-template-columns: repeat(2, 1fr); }
  .team__grid { grid-template-columns: 1fr; max-width: 300px; margin-left: auto; margin-right: auto; }
}
@media (max-width: 480px) {
  .flow-steps, .feat-grid { grid-template-columns: 1fr; }
}
</style>