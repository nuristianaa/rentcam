<template>
  <div class="howto-page">

    <!-- ── Hero ────────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero__bg">
        <div class="hero__grid" />
        <div class="hero__orb hero__orb--1" />
        <div class="hero__orb hero__orb--2" />
      </div>
      <div class="hero__inner">
        <div class="hero__badge">
          <q-icon name="auto_stories" size="14px" />
          Panduan Lengkap
        </div>
        <h1 class="hero__title">Cara Menyewa<br /><span class="hero__accent">Langkah demi Langkah</span></h1>
        <p class="hero__sub">Dari memilih alat, konfirmasi bayar via WhatsApp, hingga ambil sendiri di toko — ikuti panduan ini dan proses rental jadi super mudah.</p>
        <div class="hero__pills">
          <div class="hero__pill" v-for="p in heroPills" :key="p">
            <q-icon name="check_circle" size="14px" />
            {{ p }}
          </div>
        </div>
      </div>
    </section>

    <!-- ── Progress Bar ─────────────────────────────────────────── -->
    <div class="progress-strip">
      <div class="progress-strip__inner">
        <button
          v-for="(step, i) in steps"
          :key="i"
          class="ps-btn"
          :class="{ 'ps-btn--active': activeStep >= i }"
          @click="activeStep = i; scrollToStep(i)"
        >
          <div class="ps-btn__num">{{ String(i + 1).padStart(2, '0') }}</div>
          <div class="ps-btn__label">{{ step.shortLabel }}</div>
        </button>
        <div class="ps-fill" :style="{ width: `${(activeStep / (steps.length - 1)) * 100}%` }" />
      </div>
    </div>

    <!-- ── Steps ────────────────────────────────────────────────── -->
    <div class="steps-body">
      <div
        v-for="(step, i) in steps"
        :key="i"
        :ref="el => stepRefs[i] = el"
        class="step-block"
        :class="{ 'step-block--right': i % 2 === 1 }"
      >
        <div class="step-block__visual">
          <div class="step-visual-card" :class="`step-visual-card--${step.color}`">
            <div class="step-visual-card__num">{{ String(i + 1).padStart(2, '0') }}</div>
            <q-icon :name="step.icon" size="48px" class="step-visual-card__icon" />
            <div class="step-visual-card__label">{{ step.shortLabel }}</div>
          </div>
        </div>

        <div class="step-block__content">
          <div class="step-tag">Langkah {{ i + 1 }}</div>
          <h2 class="step-title">{{ step.title }}</h2>
          <p class="step-desc">{{ step.desc }}</p>

          <div class="step-tips" v-if="step.tips.length">
            <div class="step-tip" v-for="t in step.tips" :key="t.text">
              <div class="step-tip__icon">
                <q-icon :name="t.icon" size="15px" />
              </div>
              <div class="step-tip__text">{{ t.text }}</div>
            </div>
          </div>

          <div class="step-cta" v-if="step.cta">
            <a :href="step.cta.href" :target="step.cta.external ? '_blank' : undefined" class="step-cta-btn" :class="`step-cta-btn--${step.cta.color}`">
              <q-icon :name="step.cta.icon" size="16px" />
              {{ step.cta.label }}
            </a>
          </div>

          <div class="step-nav">
            <button v-if="i > 0" class="step-nav-btn" @click="scrollToStep(i - 1)">
              <q-icon name="arrow_back" size="14px" />
              Langkah Sebelumnya
            </button>
            <button v-if="i < steps.length - 1" class="step-nav-btn step-nav-btn--next" @click="scrollToStep(i + 1)">
              Langkah Berikutnya
              <q-icon name="arrow_forward" size="14px" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Status Flow Sidebar ──────────────────────────────────── -->
    <section class="status-section">
      <div class="status-section__inner">
        <div class="section-tag" style="margin: 0 auto 14px">
          <q-icon name="alt_route" size="13px" />
          Status Booking
        </div>
        <h2 class="section-title" style="text-align:center">Pantau Status<br /><em>Booking Anda Secara Real-Time</em></h2>
        <p class="status-section__sub">Setiap perubahan status dapat dipantau di halaman Riwayat Booking.</p>

        <div class="status-flow">
          <div v-for="(s, i) in statusFlow" :key="s.value" class="status-node">
            <div class="status-node__dot" :class="`snd--${s.color}`">
              <q-icon :name="s.icon" size="18px" />
            </div>
            <div class="status-node__connector" v-if="i < statusFlow.length - 1" />
            <div class="status-node__info">
              <div class="status-node__label">{{ s.label }}</div>
              <div class="status-node__desc">{{ s.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ──────────────────────────────────────────────────── -->
    <section class="cta">
      <div class="cta__inner">
        <div class="cta__icon">
          <q-icon name="photo_camera" size="28px" />
        </div>
        <h2 class="cta__title">Sudah Paham?<br /><em>Mulai Booking Sekarang!</em></h2>
        <p class="cta__sub">Pilih alat favoritmu dan mulai petualangan fotografimu hari ini.</p>
        <div class="cta__actions">
          <router-link to="/rental/user/items" class="cta-btn cta-btn--primary">
            <q-icon name="camera_alt" size="16px" />
            Lihat Koleksi Alat
          </router-link>
          <router-link to="/rental/user/contact" class="cta-btn cta-btn--ghost">
            <q-icon name="chat" size="16px" />
            Hubungi Kami
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeStep = ref(0)
const stepRefs = ref<any[]>([])

const scrollToStep = (i: number) => {
  activeStep.value = i
  stepRefs.value[i]?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const heroPills = [
  'Booking Online 24/7',
  'Ambil Langsung di Toko',
  'Transfer? Kirim Bukti ke WA',
  'Deposit Transparan',
]

const steps = [
  {
    shortLabel: 'Buat Akun',
    icon: 'person_add',
    color: 'purple',
    title: 'Daftar & Login ke Akun Anda',
    desc: 'Buat akun gratis di RENTCAM untuk mulai booking. Daftar hanya butuh email dan password — tidak ada biaya pendaftaran sama sekali.',
    tips: [
      { icon: 'lock', text: 'Akun Anda aman dan terenkripsi' },
      { icon: 'phone_android', text: 'Bisa login dari HP atau komputer' },
      { icon: 'info', text: 'Guest bisa browse alat, tapi perlu login untuk booking' },
    ],
    cta: { href: '/login', icon: 'login', label: 'Daftar Sekarang', color: 'navy', external: false },
  },
  {
    shortLabel: 'Pilih Alat',
    icon: 'camera_alt',
    color: 'blue',
    title: 'Jelajahi & Pilih Alat Foto',
    desc: 'Browse koleksi lengkap alat foto kami: kamera mirrorless, DSLR, lensa, drone, lighting, gimbal, dan banyak lagi. Filter berdasarkan kategori untuk menemukan alat yang pas.',
    tips: [
      { icon: 'search', text: 'Gunakan filter kategori untuk pencarian lebih cepat' },
      { icon: 'check_circle', text: 'Status "Tersedia" berarti stok ada di tanggal Anda' },
      { icon: 'photo_camera', text: 'Klik detail alat untuk lihat spesifikasi lengkap dan kalender disponibilitas' },
    ],
    cta: { href: '/rental/user/items', icon: 'storefront', label: 'Lihat Koleksi Alat', color: 'navy', external: false },
  },
  {
    shortLabel: 'Tentukan Tanggal',
    icon: 'calendar_month',
    color: 'teal',
    title: 'Pilih Tanggal Sewa',
    desc: 'Tentukan tanggal mulai dan tanggal selesai sewa. Durasi minimal 1 hari. Sistem akan mengecek ketersediaan stok secara real-time sesuai tanggal yang Anda pilih.',
    tips: [
      { icon: 'event', text: 'Tanggal mulai adalah hari Anda ambil alat di toko' },
      { icon: 'event_available', text: 'Tanggal selesai adalah hari Anda wajib kembalikan alat' },
      { icon: 'warning', text: 'Tanggal yang sudah dipesan orang lain tidak bisa dipilih' },
    ],
    cta: null,
  },
  {
    shortLabel: 'Konfirmasi Bayar',
    icon: 'chat',
    color: 'green',
    title: 'Bayar & Kirim Bukti ke WhatsApp',
    desc: 'Setelah booking tersimpan, lakukan pembayaran. Ada 2 pilihan: TRANSFER BANK (kirim bukti foto ke WA admin) atau COD (bayar tunai langsung saat ambil di toko).',
    tips: [
      { icon: 'account_balance', text: 'Transfer Bank: Transfer → Foto bukti → Kirim ke WA admin → Tunggu konfirmasi' },
      { icon: 'payments', text: 'COD: Tidak perlu transfer, cukup siapkan uang tunai saat datang ke toko' },
      { icon: 'timer', text: 'Konfirmasi WA dari admin maks. 2 jam di jam kerja (08.00–20.00)' },
    ],
    cta: { href: 'https://wa.me/6281234567890?text=Halo%20admin%2C%20saya%20ingin%20konfirmasi%20pembayaran%20booking%20saya.', icon: 'chat', label: 'Kirim Bukti ke WhatsApp', color: 'wa', external: true },
  },
  {
    shortLabel: 'Ambil di Toko',
    icon: 'storefront',
    color: 'orange',
    title: 'Datang ke Toko & Ambil Alat',
    desc: 'Setelah status booking berubah ke "Diproses", datanglah ke toko kami di Bandung sesuai tanggal mulai sewa. Bawa identitas diri (KTP) dan siapkan deposit saat pengambilan.',
    tips: [
      { icon: 'badge', text: 'Bawa KTP asli saat pengambilan alat di toko' },
      { icon: 'payments', text: 'Deposit dibayar di toko saat pengambilan (tunai/transfer)' },
      { icon: 'schedule', text: 'Jam toko: Senin–Sabtu 08.00–20.00 WIB' },
      { icon: 'fact_check', text: 'Cek kondisi alat bersama admin sebelum dibawa pulang' },
    ],
    cta: { href: 'https://maps.google.com/?q=Bandung,Jawa+Barat', icon: 'map', label: 'Buka Google Maps', color: 'navy', external: true },
  },
  {
    shortLabel: 'Gunakan Alat',
    icon: 'camera',
    color: 'purple',
    title: 'Gunakan Alat dengan Bertanggung Jawab',
    desc: 'Masa sewa berjalan! Gunakan alat sesuai panduan. Perawatan alat selama masa sewa adalah tanggung jawab penyewa. Simpan di tempat aman dan hindari benturan keras.',
    tips: [
      { icon: 'shield', text: 'Simpan alat di tas kamera yang aman dari benturan' },
      { icon: 'water_drop', text: 'Hindari paparan hujan/lembab berlebihan pada kamera dan lensa' },
      { icon: 'support_agent', text: 'Jika ada kendala dengan alat, segera hubungi kami via WhatsApp' },
    ],
    cta: null,
  },
  {
    shortLabel: 'Kembalikan',
    icon: 'task_alt',
    color: 'blue',
    title: 'Kembalikan Alat & Terima Deposit',
    desc: 'Kembalikan alat ke toko kami sebelum atau tepat pada tanggal selesai sewa. Kondisi alat dicek bersama admin. Jika kondisi baik, deposit dikembalikan penuh pada saat itu juga.',
    tips: [
      { icon: 'event', text: 'Kembalikan maksimal sebelum toko tutup (20.00 WIB) di hari selesai sewa' },
      { icon: 'cleaning_services', text: 'Bersihkan lensa dan bodi kamera sebelum dikembalikan' },
      { icon: 'payments', text: 'Deposit kembali penuh jika kondisi alat baik, tidak ada kerusakan baru' },
      { icon: 'warning', text: 'Keterlambatan pengembalian dapat dikenakan biaya tambahan per hari' },
    ],
    cta: null,
  },
]

const statusFlow = [
  { value: 'menunggu_bayar', label: 'Menunggu Bayar', desc: 'Booking dibuat, lakukan pembayaran dan kirim bukti ke WA admin', icon: 'receipt_long', color: 'yellow' },
  { value: 'menunggu_verif', label: 'Menunggu Verifikasi', desc: 'Bukti bayar diterima, admin sedang verifikasi', icon: 'fact_check', color: 'orange' },
  { value: 'diproses', label: 'Diproses', desc: 'Pembayaran OK, alat disiapkan — silakan datang ke toko', icon: 'inventory_2', color: 'blue' },
  { value: 'aktif', label: 'Aktif', desc: 'Alat sudah di tangan Anda, masa sewa berjalan', icon: 'camera_alt', color: 'teal' },
  { value: 'selesai', label: 'Selesai', desc: 'Alat dikembalikan ke toko, deposit diproses', icon: 'task_alt', color: 'green' },
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

.howto-page {
  --navy-950: #030c1f;
  --navy-700: #0f2258;
  --navy-600: #1a337a;
  --navy-500: #1e3a8a;
  --navy-400: #2563eb;
  --gray-50:  #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  background: var(--gray-50);
  color: var(--gray-800);
}

/* ── Shared ──────────────────────────────────────────────────── */
.section-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  padding: 5px 14px; border-radius: 999px; margin-bottom: 14px;
  border: 1px solid rgba(30,58,138,0.12); text-transform: uppercase;
}
.section-title {
  font-size: clamp(24px, 4vw, 36px); font-weight: 800;
  color: var(--gray-800); line-height: 1.25; margin: 0 0 16px;
  letter-spacing: -0.4px;
}
.section-title em { color: var(--navy-600); font-style: normal; }

/* ── Hero ────────────────────────────────────────────────────── */
.hero {
  position: relative; overflow: hidden;
  background: var(--navy-950); padding: 90px 28px 72px;
}
.hero__bg { position: absolute; inset: 0; pointer-events: none; }
.hero__grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 52px 52px;
}
.hero__orb { position: absolute; border-radius: 50%; filter: blur(80px); }
.hero__orb--1 { width: 500px; height: 500px; background: rgba(30,58,138,0.22); top: -160px; right: -60px; }
.hero__orb--2 { width: 300px; height: 300px; background: rgba(59,130,246,0.08); bottom: -80px; left: 8%; }
.hero__inner { position: relative; max-width: 680px; margin: 0 auto; text-align: center; }
.hero__badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2);
  color: #93c5fd; font-size: 11px; font-weight: 600;
  letter-spacing: 0.1em; padding: 5px 14px; border-radius: 999px;
  margin-bottom: 20px; text-transform: uppercase;
}
.hero__title {
  font-size: clamp(28px, 5vw, 46px); font-weight: 800; color: #fff;
  line-height: 1.2; margin: 0 0 14px; letter-spacing: -0.4px;
}
.hero__accent { color: #93c5fd; }
.hero__sub { color: rgba(255,255,255,0.5); font-size: 15px; line-height: 1.75; margin: 0 auto 28px; max-width: 520px; }
.hero__pills { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.hero__pill {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.7); font-size: 12px; font-weight: 500;
  padding: 5px 13px; border-radius: 999px;
}

/* ── Progress Strip ──────────────────────────────────────────── */
.progress-strip {
  background: #fff; border-bottom: 1px solid var(--gray-100);
  position: sticky; top: 0; z-index: 50;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.progress-strip__inner {
  max-width: 900px; margin: 0 auto;
  display: flex; position: relative; overflow-x: auto;
  padding: 0 16px;
}
.ps-btn {
  flex: 1; min-width: 80px; padding: 14px 8px;
  background: none; border: none; cursor: pointer;
  font-family: inherit; display: flex; flex-direction: column;
  align-items: center; gap: 3px; opacity: 0.35;
  transition: opacity 0.2s; position: relative; z-index: 1;
}
.ps-btn--active { opacity: 1; }
.ps-btn__num {
  font-family: 'DM Mono', monospace; font-size: 10px;
  font-weight: 500; color: var(--navy-600); letter-spacing: 0.1em;
}
.ps-btn__label { font-size: 11px; font-weight: 600; color: var(--gray-700); }
.ps-fill {
  position: absolute; bottom: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, var(--navy-500), var(--navy-400));
  border-radius: 999px; transition: width 0.4s ease;
}

/* ── Step Blocks ─────────────────────────────────────────────── */
.steps-body { max-width: 1100px; margin: 0 auto; padding: 0 28px; }
.step-block {
  display: grid; grid-template-columns: 1fr 1.5fr;
  gap: 64px; align-items: center;
  padding: 80px 0; border-bottom: 1px solid var(--gray-100);
}
.step-block:last-child { border-bottom: none; }
.step-block--right { direction: rtl; }
.step-block--right > * { direction: ltr; }

/* Visual card */
.step-visual-card {
  border-radius: 24px; padding: 44px 32px;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 16px; min-height: 280px;
  position: relative; overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.12);
}
.step-visual-card::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.12), transparent 65%);
  pointer-events: none;
}
.step-visual-card--purple { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #fff; }
.step-visual-card--blue   { background: linear-gradient(135deg, #1e3a8a, #2563eb); color: #fff; }
.step-visual-card--teal   { background: linear-gradient(135deg, #0f766e, #14b8a6); color: #fff; }
.step-visual-card--green  { background: linear-gradient(135deg, #15803d, #22c55e); color: #fff; }
.step-visual-card--orange { background: linear-gradient(135deg, #c2410c, #f97316); color: #fff; }
.step-visual-card__num {
  font-family: 'DM Mono', monospace;
  font-size: 13px; font-weight: 500; opacity: 0.55; letter-spacing: 0.12em;
}
.step-visual-card__icon { opacity: 0.95; }
.step-visual-card__label { font-size: 16px; font-weight: 800; letter-spacing: -0.2px; }

/* Content */
.step-tag {
  display: inline-flex; font-size: 11px; font-weight: 700;
  color: var(--navy-600); letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 10px;
}
.step-title {
  font-size: clamp(20px, 3vw, 30px); font-weight: 800;
  color: var(--gray-800); line-height: 1.25; margin: 0 0 14px;
  letter-spacing: -0.3px;
}
.step-desc {
  font-size: 15px; color: var(--gray-500); line-height: 1.8; margin: 0 0 22px;
}
.step-tips { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
.step-tip { display: flex; align-items: flex-start; gap: 10px; }
.step-tip__icon {
  width: 28px; height: 28px; border-radius: 8px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-tip__text { font-size: 13.5px; color: var(--gray-600); line-height: 1.6; padding-top: 4px; }

.step-cta { margin-bottom: 20px; }
.step-cta-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 11px 22px; border-radius: 10px;
  font-family: inherit; font-size: 14px; font-weight: 700;
  text-decoration: none; transition: all 0.2s;
}
.step-cta-btn--navy { background: var(--navy-500); color: #fff; }
.step-cta-btn--navy:hover { background: var(--navy-600); transform: translateY(-2px); box-shadow: 0 6px 18px rgba(30,58,138,0.35); }
.step-cta-btn--wa { background: #25d366; color: #fff; }
.step-cta-btn--wa:hover { background: #22c55e; transform: translateY(-2px); box-shadow: 0 6px 18px rgba(37,211,102,0.4); }

.step-nav { display: flex; gap: 10px; flex-wrap: wrap; }
.step-nav-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: none; border: 1.5px solid var(--gray-200);
  color: var(--gray-500); font-family: inherit; font-size: 12.5px;
  font-weight: 600; padding: 7px 14px; border-radius: 8px; cursor: pointer;
  transition: all 0.18s;
}
.step-nav-btn:hover { border-color: rgba(30,58,138,0.3); color: var(--navy-600); }
.step-nav-btn--next { background: rgba(30,58,138,0.05); }

/* ── Status Flow ─────────────────────────────────────────────── */
.status-section { background: var(--navy-950); padding: 80px 28px; }
.status-section__inner { max-width: 800px; margin: 0 auto; text-align: center; }
.status-section .section-tag {
  background: rgba(59,130,246,0.1); color: #93c5fd; border-color: rgba(59,130,246,0.2);
}
.status-section .section-title { color: #fff; }
.status-section .section-title em { color: #93c5fd; }
.status-section__sub { color: rgba(255,255,255,0.4); font-size: 14px; margin-bottom: 44px; }

.status-flow {
  display: flex; align-items: flex-start;
  justify-content: center; gap: 0;
  flex-wrap: nowrap;
}
.status-node { display: flex; flex-direction: column; align-items: center; flex: 1; }
.status-node__dot {
  width: 52px; height: 52px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff; border: 2px solid; margin-bottom: 12px;
  flex-shrink: 0;
}
.snd--yellow { background: rgba(234,179,8,0.18); border-color: rgba(234,179,8,0.45); }
.snd--orange { background: rgba(249,115,22,0.18); border-color: rgba(249,115,22,0.45); }
.snd--blue   { background: rgba(59,130,246,0.18); border-color: rgba(59,130,246,0.45); }
.snd--teal   { background: rgba(20,184,166,0.18); border-color: rgba(20,184,166,0.45); }
.snd--green  { background: rgba(34,197,94,0.18);  border-color: rgba(34,197,94,0.45);  }
.status-node__connector {
  position: absolute; display: none;
}
.status-node__label { font-size: 12px; font-weight: 700; color: #fff; margin-bottom: 4px; }
.status-node__desc  { font-size: 10.5px; color: rgba(255,255,255,0.4); line-height: 1.55; padding: 0 4px; }

/* ── CTA ─────────────────────────────────────────────────────── */
.cta { background: var(--gray-50); padding: 80px 28px; text-align: center; border-top: 1px solid var(--gray-100); }
.cta__inner { max-width: 500px; margin: 0 auto; }
.cta__icon {
  width: 64px; height: 64px; border-radius: 18px;
  background: rgba(30,58,138,0.08); color: var(--navy-600);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 20px; border: 1.5px solid rgba(30,58,138,0.12);
}
.cta__title {
  font-size: clamp(22px, 3.5vw, 32px); font-weight: 800;
  color: var(--gray-800); line-height: 1.3; margin: 0 0 12px;
}
.cta__title em { color: var(--navy-600); font-style: normal; }
.cta__sub { color: var(--gray-500); font-size: 15px; line-height: 1.65; margin: 0 0 28px; }
.cta__actions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.cta-btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 12px 22px; border-radius: 10px;
  font-family: inherit; font-size: 14px; font-weight: 600;
  text-decoration: none; transition: all 0.2s;
}
.cta-btn--primary { background: var(--navy-500); color: #fff; box-shadow: 0 4px 16px rgba(30,58,138,0.3); }
.cta-btn--primary:hover { background: var(--navy-600); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(30,58,138,0.4); }
.cta-btn--ghost { background: var(--gray-100); color: var(--gray-700); border: 1.5px solid var(--gray-200); }
.cta-btn--ghost:hover { border-color: rgba(30,58,138,0.25); color: var(--navy-600); background: rgba(30,58,138,0.05); }

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 780px) {
  .step-block { grid-template-columns: 1fr; gap: 32px; }
  .step-block--right { direction: ltr; }
  .step-visual-card { min-height: 180px; flex-direction: row; padding: 28px 24px; }
  .status-flow { flex-direction: column; align-items: center; gap: 20px; }
}
</style>
