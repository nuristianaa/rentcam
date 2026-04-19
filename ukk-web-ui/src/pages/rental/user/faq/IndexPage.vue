<template>
  <div class="faq-page">

    <!-- ── Hero ─────────────────────────────────────────────────── -->
    <section class="faq-hero">
      <div class="faq-hero__bg">
        <div class="faq-hero__grid" />
        <div class="faq-hero__orb faq-hero__orb--1" />
        <div class="faq-hero__orb faq-hero__orb--2" />
      </div>

      <div class="faq-hero__inner">
        <div class="faq-hero__badge">
          <q-icon name="help_outline" size="14px" />
          Help Center
        </div>
        <h1 class="faq-hero__title">How can we<br /><span class="faq-hero__title--accent">help you?</span></h1>
        <p class="faq-hero__sub">Find answers to frequently asked questions about our rental service.</p>

        <!-- Search -->
        <div class="faq-search-wrap">
          <q-icon name="search" class="faq-search-icon" size="18px" />
          <input
            v-model="search"
            class="faq-search-input"
            placeholder="Search questions..."
          />
          <button v-if="search" class="faq-search-clear" @click="search = ''">
            <q-icon name="close" size="16px" />
          </button>
        </div>

        <!-- Mini stats -->
        <div class="faq-hero__stats">
          <div class="faq-stat">
            <span class="faq-stat__num">{{ allFaq.length }}</span>
            <span class="faq-stat__label">Questions</span>
          </div>
          <div class="faq-stat-sep" />
          <div class="faq-stat">
            <span class="faq-stat__num">{{ categories.length - 1 }}</span>
            <span class="faq-stat__label">Categories</span>
          </div>
          <div class="faq-stat-sep" />
          <div class="faq-stat">
            <span class="faq-stat__num">24/7</span>
            <span class="faq-stat__label">Support</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Body ──────────────────────────────────────────────────── -->
    <div class="faq-body">

      <!-- Category pills -->
      <div class="faq-cats-wrap">
        <div class="faq-cats">
          <button
            v-for="cat in categories"
            :key="cat.key"
            class="faq-cat-pill"
            :class="{ 'faq-cat-pill--active': activeCategory === cat.key }"
            @click="activeCategory = cat.key"
          >
            <q-icon :name="cat.icon" size="15px" />
            {{ cat.label }}
            <span v-if="cat.key !== 'semua'" class="pill-count">
              {{ allFaq.filter(f => f.cat === cat.key).length }}
            </span>
          </button>
        </div>
      </div>

      <!-- Empty -->
      <div v-if="filteredItems.length === 0" class="faq-empty">
        <div class="faq-empty__icon">
          <q-icon name="search_off" size="30px" />
        </div>
        <div class="faq-empty__title">Not found</div>
        <div class="faq-empty__text">No results for <strong>"{{ search }}"</strong></div>
        <button class="faq-reset-btn" @click="search = ''; activeCategory = 'semua'">
          <q-icon name="refresh" size="14px" />
          Reset Search
        </button>
      </div>

      <!-- FAQ Groups -->
      <template v-else>
        <div
          v-for="group in groupedItems"
          :key="group.key"
          class="faq-group"
        >
          <div class="faq-group__header">
            <div class="faq-group__icon">
              <q-icon :name="group.icon" size="16px" />
            </div>
            <span class="faq-group__label">{{ group.label }}</span>
            <span class="faq-group__count">{{ group.items.length }}</span>
          </div>

          <div class="faq-list">
            <div
              v-for="(item, idx) in group.items"
              :key="idx"
              class="faq-item"
              :class="{ 'faq-item--open': openKeys.has(`${group.key}-${idx}`) }"
              @click="toggle(`${group.key}-${idx}`)"
            >
              <div class="faq-item__q">
                <div class="faq-item__num">{{ String(idx + 1).padStart(2, '0') }}</div>
                <span class="faq-item__q-text" v-html="highlight(item.q)" />
                <div class="faq-item__toggle">
                  <q-icon
                    :name="openKeys.has(`${group.key}-${idx}`) ? 'remove' : 'add'"
                    size="18px"
                  />
                </div>
              </div>
              <div class="faq-item__a-wrap">
                <div class="faq-item__a" v-html="highlight(item.a)" />
              </div>
            </div>
          </div>
        </div>
      </template>

    </div>

    <!-- ── CTA ───────────────────────────────────────────────────── -->
    <section class="faq-cta">
      <div class="faq-cta__inner">
        <div class="faq-cta__icon">
          <q-icon name="support_agent" size="28px" />
        </div>
        <div class="faq-cta__title">Still have questions?</div>
        <div class="faq-cta__sub">Our support team is ready to help anytime — 24 hours a day, 7 days a week.</div>
        <div class="faq-cta__actions">
          <a href="https://wa.me/6281234567890" target="_blank" class="cta-btn cta-btn--primary">
            <q-icon name="chat" size="16px" />
            Chat via WhatsApp
          </a>
          <a href="mailto:support@ukkreental.id" class="cta-btn cta-btn--outline">
            <q-icon name="email" size="16px" />
            Send Email
          </a>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const search = ref('')
const activeCategory = ref('semua')
const openKeys = ref<Set<string>>(new Set())

const toggle = (key: string) => {
  const s = new Set(openKeys.value)
  if (s.has(key)) s.delete(key)
  else s.add(key)
  openKeys.value = s
}

const highlight = (text: string) => {
  if (!search.value.trim()) return text
  const q = search.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(`(${q})`, 'gi'), '<mark>$1</mark>')
}

const categories = [
  { key: 'semua',      label: 'All',         icon: 'apps' },
  { key: 'rental',     label: 'How to Rent',   icon: 'camera_alt' },
  { key: 'bayar',      label: 'Payment',    icon: 'payments' },
  { key: 'pengiriman', label: 'Store Pickup',  icon: 'storefront' },
  { key: 'status',     label: 'Booking Status', icon: 'alt_route' },
  { key: 'lainnya',    label: 'Others',       icon: 'help_outline' },
]

const allFaq = [
  // ── How to Rent
  { cat: 'rental', q: 'How do I rent camera equipment?', a: 'Choose the equipment on the <em>Photo Equipment</em> page, click "Rent Now", set your start & end dates, and complete the payment. Your booking will enter <em>Waiting for Payment</em> status automatically.' },
  { cat: 'rental', q: 'What is the minimum rental duration?', a: 'The minimum rental duration is <strong>1 day</strong>. There is no maximum limit, but equipment availability depends on other bookings.' },
  { cat: 'rental', q: 'Can I extend my rental period?', a: 'Yes! Contact us before your rental period ends via WhatsApp, and we will help you extend it as long as the equipment is available.' },
  { cat: 'rental', q: 'What equipment is available?', a: 'We provide mirrorless cameras, DSLRs, lenses with various mounts, drones, lighting, gimbals, and accessories. Check the <em>Photo Equipment</em> page for a full list and real-time availability.' },
  { cat: 'rental', q: 'Are there any specific requirements to rent?', a: 'Renters must: (1) have a registered account, (2) provide a valid ID card (KTP), and (3) pay a deposit based on the value of the equipment. Additional verification may be required for certain premium items.' },
  // ── Payment
  { cat: 'bayar', q: 'What payment methods are accepted?', a: 'We accept <strong>Bank Transfers</strong> and <strong>COD (cash payment in store)</strong> upon bringing the equipment.' },
  { cat: 'bayar', q: 'How to confirm a bank transfer payment?', a: 'After transferring, <strong>send a photo of your transfer receipt to the WhatsApp admin</strong> first. After confirmation, the booking status will update. Do not just upload it in the system without contacting WA admin.' },
  { cat: 'bayar', q: 'Which WhatsApp number should I send the transfer receipt to?', a: 'Send the transfer receipt to the admin WhatsApp number listed on the contact page. Click the <em>Chat WhatsApp</em> button on this website to get directly connected.' },
  { cat: 'bayar', q: 'Is there a deposit?', a: 'Yes, a deposit is required to be paid during pickup at the store as a guarantee. It is fully refunded after the equipment is returned in good condition.' },
  { cat: 'bayar', q: 'What if I cancel my order?', a: 'Cancellations before the item is picked up can be made at no cost. Contact us via WhatsApp immediately to cancel.' },
  { cat: 'bayar', q: 'How long does transfer payment verification take?', a: 'After sending the transfer receipt via WhatsApp, the admin will confirm it within <strong>1-2 hours</strong> during business hours (Monday-Saturday, 08:00-20:00 WIB).' },
  // ── Store Pickup
  { cat: 'pengiriman', q: 'Is there a delivery or home drop-off service?', a: 'There are no delivery services. Equipment must be picked up and returned <strong>directly to our store</strong> in Bandung. This ensures the condition of the equipment is checked together during handover.' },
  { cat: 'pengiriman', q: 'Where do I pick up the equipment?', a: 'Pick up the equipment directly at our store located in <strong>Bandung, West Java</strong>. See the location map on the About Us page or click the Google Maps button.' },
  { cat: 'pengiriman', q: 'When can I pick up the equipment?', a: 'Equipment can be obtained on the rental start date according to your booking. Store operating hours: <strong>Monday-Saturday, 08:00-20:00 WIB</strong>.' },
  { cat: 'pengiriman', q: 'How is the return process?', a: 'Return the equipment to the store before or right on the rental end date. Condition is checked together. If good, deposit will be refunded on the spot or within 1-3 business days.' },
  { cat: 'pengiriman', q: 'What condition should the equipment be in upon handover?', a: 'Each piece of equipment is checked and cleaned. We attach an equipment condition record signed together during handover in the store.' },
  // ── Booking Status
  { cat: 'status', q: 'What are the different booking statuses?', a: 'There are 5 main statuses: <strong>Waiting for Payment</strong> → <strong>Waiting for Verification</strong> → <strong>Processing</strong> → <strong>Active</strong> → <strong>Completed</strong>. Plus a <em>Cancelled</em> status if the booking is cancelled.' },
  { cat: 'status', q: 'What does "Waiting for Payment" mean?', a: 'Your booking has been created successfully. Make your payment and send the transfer receipt to WA admin (for transfers). COD buyers can come directly to the store for pickup.' },
  { cat: 'status', q: 'What does "Waiting for Verification" mean?', a: 'Admin is verifying the transfer receipt you sent via WhatsApp. This process usually takes 1-2 hours on business days.' },
  { cat: 'status', q: 'What does "Processing" mean?', a: 'Your payment has been verified, and the equipment is being prepared. You can come to the store to pick up the equipment on your booked date.' },
  { cat: 'status', q: 'What does "Active" mean?', a: 'The equipment is in your hands, and the rental period has begun. Store everything properly, use them with care, and return to the store on schedule.' },
  { cat: 'status', q: 'What does "Completed" mean?', a: 'The equipment has been returned to the store and confirmed by the admin. The deposit will be processed to be returned to you.' },
  // ── Others
  { cat: 'lainnya', q: 'What happens if the equipment is damaged while I have it?', a: 'The renter is responsible for damages incurred during the rental period. Repair or replacement costs are adjusted based on the extent of the damage and may be deducted from the deposit.' },
  { cat: 'lainnya', q: 'Can I check out the equipment before renting?', a: 'Of course! As our system is store-pickup based, you can come directly to our store in Bandung to check the condition of the equipment. Contact us first via WhatsApp to set an appointment.' },
  { cat: 'lainnya', q: 'Is equipment insurance available?', a: 'Currently, we do not provide a separate insurance package. We advise renters to always be careful when using our equipment.' },
]

const filteredItems = computed(() =>
  allFaq.filter(item => {
    const matchCat = activeCategory.value === 'semua' || item.cat === activeCategory.value
    const matchSearch = !search.value.trim() ||
      item.q.toLowerCase().includes(search.value.toLowerCase()) ||
      item.a.toLowerCase().includes(search.value.toLowerCase())
    return matchCat && matchSearch
  })
)

const groupedItems = computed(() => {
  const catMap = Object.fromEntries(
    categories.slice(1).map(c => [c.key, { ...c, items: [] as typeof allFaq }])
  )
  for (const item of filteredItems.value) {
    catMap[item.cat]?.items.push(item)
  }
  return Object.values(catMap).filter(g => g.items.length > 0)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Design Tokens ──────────────────────────────────────────── */
.faq-page {
  --navy-950: #030c1f;
  --navy-900: #060e2b;
  --navy-700: #0f2258;
  --navy-600: #1a337a;
  --navy-500: #1e3a8a;
  --navy-400: #2563eb;
  --navy-300: #3b82f6;
  --gray-50:  #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-300: #cbd5e1;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 16px rgba(30,58,138,0.08);
  --shadow-lg: 0 8px 32px rgba(30,58,138,0.13);

  min-height: 100vh;
  background: var(--gray-50);
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  color: var(--gray-800);
}

/* ── Hero ───────────────────────────────────────────────────── */
.faq-hero {
  position: relative;
  overflow: hidden;
  background: var(--navy-950);
  padding: 80px 24px 60px;
}
.faq-hero__bg { position: absolute; inset: 0; pointer-events: none; }
.faq-hero__grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 52px 52px;
}
.faq-hero__orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); pointer-events: none;
}
.faq-hero__orb--1 { width: 500px; height: 500px; background: rgba(30,58,138,0.25); top: -150px; right: -100px; }
.faq-hero__orb--2 { width: 300px; height: 300px; background: rgba(59,130,246,0.1); bottom: -80px; left: 5%; }
.faq-hero__inner { position: relative; max-width: 720px; margin: 0 auto; }

.faq-hero__badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(59,130,246,0.1); backdrop-filter: blur(8px);
  border: 1px solid rgba(59,130,246,0.2);
  color: #93c5fd; font-size: 11px; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase;
  padding: 5px 14px; border-radius: 999px; margin-bottom: 20px;
}
.faq-hero__title {
  font-size: clamp(30px, 5vw, 48px);
  font-weight: 800; color: #fff;
  line-height: 1.2; margin: 0 0 14px; letter-spacing: -0.4px;
}
.faq-hero__title--accent { color: #93c5fd; }
.faq-hero__sub {
  color: rgba(255,255,255,0.5); font-size: 15px;
  line-height: 1.7; margin: 0 0 28px; max-width: 520px;
}

/* Search */
.faq-search-wrap {
  display: flex; align-items: center;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(14px);
  border: 1.5px solid rgba(255,255,255,0.15);
  border-radius: var(--radius-lg);
  padding: 0 16px; gap: 10px;
  transition: all 0.2s; margin-bottom: 28px;
}
.faq-search-wrap:focus-within {
  background: rgba(255,255,255,0.13);
  border-color: rgba(59,130,246,0.4);
  box-shadow: 0 0 0 3px rgba(59,130,246,0.12);
}
.faq-search-icon { color: rgba(255,255,255,0.45); flex-shrink: 0; }
.faq-search-input {
  flex: 1; background: none; border: none; outline: none;
  color: #fff; font-size: 15px; font-family: inherit;
  padding: 15px 0;
}
.faq-search-input::placeholder { color: rgba(255,255,255,0.35); }
.faq-search-clear {
  background: rgba(255,255,255,0.12); border: none;
  color: rgba(255,255,255,0.7); cursor: pointer; padding: 4px;
  display: flex; align-items: center; border-radius: 50%;
  transition: background 0.15s;
}
.faq-search-clear:hover { background: rgba(255,255,255,0.22); }

/* Stats */
.faq-hero__stats {
  display: flex; align-items: center; gap: 20px;
}
.faq-stat { display: flex; flex-direction: column; gap: 2px; }
.faq-stat__num { font-size: 18px; font-weight: 700; color: #fff; line-height: 1; }
.faq-stat__label { font-size: 11px; color: rgba(255,255,255,0.4); font-weight: 500; letter-spacing: 0.04em; }
.faq-stat-sep { width: 1px; height: 28px; background: rgba(255,255,255,0.15); }

/* ── Body ──────────────────────────────────────────────────── */
.faq-body {
  max-width: 760px; margin: 0 auto;
  padding: 40px 24px 80px;
}

/* Category pills */
.faq-cats-wrap { margin-bottom: 32px; }
.faq-cats { display: flex; gap: 8px; flex-wrap: wrap; }
.faq-cat-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 999px;
  border: 1.5px solid var(--gray-200);
  background: #fff; font-size: 13px; font-family: inherit;
  font-weight: 500; color: var(--gray-500); cursor: pointer;
  transition: all 0.18s; box-shadow: var(--shadow-sm);
}
.faq-cat-pill:hover {
  border-color: rgba(30,58,138,0.25); color: var(--navy-600);
  background: rgba(30,58,138,0.04);
}
.faq-cat-pill--active {
  background: var(--navy-600); border-color: var(--navy-600);
  color: #fff; box-shadow: 0 4px 14px rgba(30,58,138,0.35);
}
.pill-count {
  background: rgba(255,255,255,0.22); font-size: 11px; font-weight: 600;
  padding: 1px 7px; border-radius: 999px; line-height: 1.5;
}
.faq-cat-pill:not(.faq-cat-pill--active) .pill-count {
  background: var(--gray-100); color: var(--gray-500);
}

/* Group */
.faq-group { margin-bottom: 36px; }
.faq-group__header {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 12px; padding-bottom: 12px;
  border-bottom: 1.5px solid var(--gray-100);
}
.faq-group__icon {
  width: 32px; height: 32px; border-radius: var(--radius-sm);
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.faq-group__label {
  font-size: 12px; font-weight: 700; color: var(--gray-600);
  letter-spacing: 0.06em; text-transform: uppercase;
}
.faq-group__count {
  margin-left: auto;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  font-size: 11px; font-weight: 600;
  padding: 2px 10px; border-radius: 999px;
}

/* FAQ Items */
.faq-list { display: flex; flex-direction: column; gap: 6px; }
.faq-item {
  background: #fff; border: 1.5px solid var(--gray-100);
  border-radius: var(--radius-md); cursor: pointer; overflow: hidden;
  transition: border-color 0.18s, box-shadow 0.18s, transform 0.15s;
  box-shadow: var(--shadow-sm);
}
.faq-item:hover {
  border-color: rgba(30,58,138,0.2);
  box-shadow: var(--shadow-md); transform: translateY(-1px);
}
.faq-item--open {
  border-color: rgba(30,58,138,0.3);
  box-shadow: var(--shadow-lg);
}
.faq-item__q {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 18px 20px;
}
.faq-item__num {
  font-family: 'DM Mono', monospace;
  font-size: 11px; font-weight: 500; color: var(--navy-400);
  letter-spacing: 0.06em; margin-top: 3px; flex-shrink: 0; min-width: 24px;
}
.faq-item__q-text {
  flex: 1; font-size: 14.5px; font-weight: 600;
  color: var(--gray-800); line-height: 1.55;
}
.faq-item__toggle {
  flex-shrink: 0; width: 30px; height: 30px;
  border-radius: var(--radius-sm); background: var(--gray-100);
  color: var(--gray-400); display: flex; align-items: center; justify-content: center;
  margin-top: -2px; transition: background 0.18s, color 0.18s;
}
.faq-item--open .faq-item__toggle { background: var(--navy-600); color: #fff; }
.faq-item:hover:not(.faq-item--open) .faq-item__toggle {
  background: rgba(30,58,138,0.1); color: var(--navy-600);
}

/* Accordion */
.faq-item__a-wrap {
  display: grid; grid-template-rows: 0fr;
  transition: grid-template-rows 0.26s ease;
}
.faq-item--open .faq-item__a-wrap { grid-template-rows: 1fr; }
.faq-item__a {
  overflow: hidden; font-size: 14px; color: var(--gray-500);
  line-height: 1.8; padding: 0 20px 0 58px;
}
.faq-item--open .faq-item__a { padding: 0 20px 18px 58px; }
.faq-item__a :deep(strong) { color: var(--gray-700); }
.faq-item__a :deep(em) { color: var(--navy-600); font-style: normal; font-weight: 500; }
:deep(mark) {
  background: #dbeafe; color: var(--navy-700);
  border-radius: 3px; padding: 0 3px;
}

/* Empty state */
.faq-empty {
  text-align: center; padding: 72px 24px;
  display: flex; flex-direction: column; align-items: center; gap: 10px;
}
.faq-empty__icon {
  width: 64px; height: 64px; border-radius: var(--radius-lg);
  background: var(--gray-100); color: var(--gray-400);
  display: flex; align-items: center; justify-content: center; margin-bottom: 8px;
}
.faq-empty__title { font-size: 17px; font-weight: 700; color: var(--gray-700); }
.faq-empty__text  { color: var(--gray-400); font-size: 14px; }
.faq-reset-btn {
  margin-top: 12px; padding: 9px 20px;
  background: var(--navy-600); color: #fff; border: none;
  border-radius: var(--radius-sm); font-family: inherit;
  font-size: 13px; font-weight: 600; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px;
  transition: background 0.18s, transform 0.15s;
}
.faq-reset-btn:hover { background: var(--navy-700); transform: translateY(-1px); }

/* ── CTA ────────────────────────────────────────────────────── */
.faq-cta {
  background: var(--navy-950);
  padding: 64px 24px;
}
.faq-cta__inner {
  max-width: 480px; margin: 0 auto; text-align: center;
}
.faq-cta__icon {
  width: 62px; height: 62px; border-radius: 18px;
  background: rgba(59,130,246,0.12);
  border: 1.5px solid rgba(59,130,246,0.2);
  color: #93c5fd;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 18px;
}
.faq-cta__title { color: #fff; font-size: 22px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.3px; }
.faq-cta__sub { color: rgba(255,255,255,0.45); font-size: 14px; margin-bottom: 28px; line-height: 1.65; }
.faq-cta__actions { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
.cta-btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 11px 22px; border-radius: var(--radius-sm);
  font-family: inherit; font-size: 13.5px; font-weight: 600;
  text-decoration: none; transition: all 0.18s;
}
.cta-btn--primary {
  background: var(--navy-600); color: #fff;
  box-shadow: 0 4px 16px rgba(30,58,138,0.4);
}
.cta-btn--primary:hover { background: var(--navy-700); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(30,58,138,0.5); }
.cta-btn--outline {
  background: transparent; color: rgba(255,255,255,0.65);
  border: 1.5px solid rgba(255,255,255,0.18);
}
.cta-btn--outline:hover { background: rgba(255,255,255,0.07); color: #fff; border-color: rgba(255,255,255,0.35); }
</style>