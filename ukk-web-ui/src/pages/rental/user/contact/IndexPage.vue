<template>
  <div class="contact-page">

    <!-- ── Hero ─────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero__bg">
        <div class="hero__grid" />
        <div class="hero__orb hero__orb--1" />
        <div class="hero__orb hero__orb--2" />
      </div>
      <div class="hero__inner">
        <div class="hero__badge">
          <q-icon name="support_agent" size="14px" />
          Hubungi Kami
        </div>
        <h1 class="hero__title">Kami Siap<br /><span class="hero__accent">Membantu Kamu</span></h1>
        <p class="hero__sub">Punya pertanyaan, mau reservasi, atau butuh rekomendasi alat? Hubungi kami langsung — respons cepat!</p>
      </div>
    </section>

    <!-- ── Contact Cards ─────────────────────────────────────── -->
    <section class="channels">
      <div class="channels__inner">
        <a href="https://wa.me/6281234567890" target="_blank" class="channel-card channel-card--wa">
          <div class="channel-card__icon">
            <q-icon name="chat" size="28px" />
          </div>
          <div class="channel-card__label">WhatsApp</div>
          <div class="channel-card__value">+62 812-3456-7890</div>
          <div class="channel-card__note">Respons dalam 15 menit di jam kerja</div>
          <div class="channel-card__cta">
            Chat Sekarang
            <q-icon name="arrow_forward" size="14px" />
          </div>
        </a>

        <a href="mailto:info@ukkreental.id" class="channel-card channel-card--email">
          <div class="channel-card__icon">
            <q-icon name="email" size="28px" />
          </div>
          <div class="channel-card__label">Email</div>
          <div class="channel-card__value">info@ukkreental.id</div>
          <div class="channel-card__note">Untuk pertanyaan formal & invoice</div>
          <div class="channel-card__cta">
            Kirim Email
            <q-icon name="arrow_forward" size="14px" />
          </div>
        </a>

        <div class="channel-card channel-card--store">
          <div class="channel-card__icon">
            <q-icon name="storefront" size="28px" />
          </div>
          <div class="channel-card__label">Kunjungi Toko</div>
          <div class="channel-card__value">Bandung, Jawa Barat</div>
          <div class="channel-card__note">Senin – Sabtu · 08.00 – 20.00 WIB</div>
          <div class="channel-card__cta">
            Lihat Lokasi ↓
          </div>
        </div>
      </div>
    </section>

    <!-- ── WA Info ────────────────────────────────────────────── -->
    <section class="wa-info">
      <div class="wa-info__inner">
        <div class="wa-info__text">
          <div class="section-tag">
            <q-icon name="chat" size="13px" />
            Konfirmasi Pembayaran
          </div>
          <h2 class="section-title">Pembayaran Transfer?<br /><em>Kirim Bukti ke WA Kami</em></h2>
          <p class="wa-info__body">
            Jika memilih metode bayar Transfer Bank, setelah transfer selesai
            <strong>wajib kirim foto bukti transfer ke WhatsApp kami</strong> agar admin bisa memverifikasi dan booking Anda diproses.
          </p>
          <div class="wa-steps">
            <div class="wa-step" v-for="(s, i) in waSteps" :key="i">
              <div class="wa-step__num">{{ i + 1 }}</div>
              <div class="wa-step__text">{{ s }}</div>
            </div>
          </div>
          <a href="https://wa.me/6281234567890?text=Halo%20UKK%20Rental%2C%20saya%20ingin%20konfirmasi%20pembayaran%20booking%20saya." target="_blank" class="wa-btn">
            <q-icon name="chat" size="18px" />
            Kirim Bukti Transfer via WA
          </a>
        </div>
        <div class="wa-info__visual">
          <div class="wa-chat-mockup">
            <div class="wm-header">
              <div class="wm-avatar">
                <q-icon name="camera_alt" size="18px" />
              </div>
              <div>
                <div class="wm-name">UKK Rental</div>
                <div class="wm-status">● Online</div>
              </div>
            </div>
            <div class="wm-body">
              <div class="wm-msg wm-msg--in">
                Halo! Saya sudah transfer untuk booking BK-20251234. Ini bukti transfernya 📷
              </div>
              <div class="wm-img">
                <q-icon name="image" size="22px" />
                <span>bukti_transfer.jpg</span>
              </div>
              <div class="wm-msg wm-msg--out">
                Terima kasih! Pembayaran sudah kami terima. Booking Anda sudah diproses ✅ Alat siap diambil sesuai tanggal booking ya!
              </div>
              <div class="wm-time">14:32 ✓✓</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Location & Map ─────────────────────────────────────── -->
    <section class="location">
      <div class="location__inner">
        <div class="section-tag" style="margin: 0 auto 14px; text-align:center">
          <q-icon name="location_on" size="13px" />
          Lokasi Toko
        </div>
        <h2 class="section-title" style="text-align:center">Temukan Kami<br /><em>di Bandung</em></h2>

        <div class="loc-layout">
          <div class="loc-map">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126748.56722619052!2d107.5381682!3d-6.9174639!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e68e6398252477f%3A0x146a1f93d3e815b2!2sBandung%2C%20Kota%20Bandung%2C%20Jawa%20Barat!5e0!3m2!1sid!2sid!4v1712900000000!5m2!1sid!2sid"
              width="100%"
              height="100%"
              style="border:0;"
              allowfullscreen
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            />
          </div>

          <div class="loc-info">
            <div class="loc-item" v-for="li in locItems" :key="li.label">
              <div class="loc-item__icon">
                <q-icon :name="li.icon" size="18px" />
              </div>
              <div>
                <div class="loc-item__label">{{ li.label }}</div>
                <div class="loc-item__val">{{ li.val }}</div>
              </div>
            </div>
            <a href="https://maps.google.com/?q=Bandung,Jawa+Barat" target="_blank" class="maps-btn">
              <q-icon name="map" size="16px" />
              Buka di Google Maps
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ── FAQ Snippet ────────────────────────────────────────── -->
    <section class="faq-snip">
      <div class="faq-snip__inner">
        <div class="section-tag" style="margin: 0 auto 14px">
          <q-icon name="help_outline" size="13px" />
          Pertanyaan Cepat
        </div>
        <h2 class="section-title" style="text-align:center">Mungkin <em>Sudah Ada Jawabannya</em></h2>
        <div class="faq-list">
          <div v-for="(f, i) in quickFaqs" :key="i" class="faq-item" :class="{ 'faq-item--open': openIdx === i }" @click="openIdx = openIdx === i ? -1 : i">
            <div class="faq-item__q">
              <span>{{ f.q }}</span>
              <q-icon :name="openIdx === i ? 'remove' : 'add'" size="18px" class="faq-toggle" />
            </div>
            <div class="faq-item__a-wrap">
              <div class="faq-item__a">{{ f.a }}</div>
            </div>
          </div>
        </div>
        <div style="text-align:center; margin-top:28px;">
          <router-link to="/rental/user/faq" class="btn-secondary">
            <q-icon name="read_more" size="15px" />
            Lihat Semua FAQ
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const openIdx = ref(-1)

const waSteps = [
  'Lakukan transfer ke rekening UKK Rental sesuai nominal tagihan',
  'Screenshot atau foto struk pembayaran yang jelas',
  'Kirim ke WhatsApp kami beserta nomor booking Anda',
  'Tunggu konfirmasi admin (maks. 2 jam di jam kerja)',
]

const locItems = [
  { icon: 'location_on', label: 'Alamat', val: 'Bandung, Jawa Barat, Indonesia' },
  { icon: 'schedule',    label: 'Jam Operasional', val: 'Senin – Sabtu · 08.00 – 20.00 WIB' },
  { icon: 'event_busy',  label: 'Hari Libur', val: 'Minggu & Hari Besar Nasional' },
  { icon: 'storefront',  label: 'Pickup & Return', val: 'Langsung di toko (no delivery)' },
]

const quickFaqs = [
  { q: 'Ke mana saya harus kirim bukti transfer?', a: 'Kirim foto bukti transfer ke WhatsApp admin kami di +62 812-3456-7890 beserta nomor booking Anda. Admin akan konfirmasi dalam 1–2 jam di hari kerja.' },
  { q: 'Apakah saya bisa datang ke toko tanpa booking dulu?', a: 'Untuk memastikan stok tersedia, lebih baik booking online terlebih dahulu. Namun Anda boleh datang untuk melihat koleksi alat sebelum memutuskan.' },
  { q: 'Bagaimana jika saya terlambat mengembalikan alat?', a: 'Segera hubungi kami via WhatsApp sebelum tanggal berakhir. Keterlambatan pengembalian dapat dikenakan biaya tambahan per hari sesuai tarif alat.' },
  { q: 'Apakah nomor WhatsApp admin aktif 24 jam?', a: 'WhatsApp aktif 24 jam untuk menerima pesan, namun respons admin dijamin di jam kerja (08.00–20.00 WIB). Di luar jam itu, pesan akan dijawab keesokan harinya.' },
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

.contact-page {
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
  --wa-green: #25d366;
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  min-height: 100vh;
  background: var(--gray-50);
  color: var(--gray-800);
}

/* ── Shared ────────────────────────────────────────────────── */
.section-tag {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(30,58,138,0.07); color: var(--navy-600);
  font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  padding: 5px 14px; border-radius: 999px;
  margin-bottom: 14px; border: 1px solid rgba(30,58,138,0.12);
  text-transform: uppercase;
}
.section-title {
  font-size: clamp(24px, 4vw, 36px); font-weight: 800;
  color: var(--gray-800); line-height: 1.25; margin: 0 0 20px;
  letter-spacing: -0.4px;
}
.section-title em { color: var(--navy-600); font-style: normal; }

/* ── Hero ──────────────────────────────────────────────────── */
.hero {
  position: relative; overflow: hidden;
  background: var(--navy-950); padding: 90px 28px 70px;
}
.hero__bg { position: absolute; inset: 0; pointer-events: none; }
.hero__grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 52px 52px;
}
.hero__orb {
  position: absolute; border-radius: 50%; filter: blur(80px);
}
.hero__orb--1 { width: 500px; height: 500px; background: rgba(30,58,138,0.2); top: -180px; left: -80px; }
.hero__orb--2 { width: 350px; height: 350px; background: rgba(59,130,246,0.1); bottom: -100px; right: -60px; }
.hero__inner { position: relative; max-width: 660px; margin: 0 auto; text-align: center; }
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
.hero__sub { color: rgba(255,255,255,0.5); font-size: 15px; line-height: 1.75; margin: 0; max-width: 480px; margin: 0 auto; }

/* ── Channel Cards ─────────────────────────────────────────── */
.channels { background: #fff; border-bottom: 1px solid var(--gray-100); padding: 48px 28px; }
.channels__inner {
  max-width: 900px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
}
.channel-card {
  border-radius: 18px; padding: 28px 24px;
  text-decoration: none; display: flex; flex-direction: column; gap: 4px;
  border: 2px solid transparent; transition: all 0.22s; cursor: pointer;
}
.channel-card--wa {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-color: #86efac; color: #14532d;
}
.channel-card--wa:hover { transform: translateY(-5px); box-shadow: 0 16px 40px rgba(34,197,94,0.25); }
.channel-card--email {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-color: #bfdbfe; color: var(--navy-700);
}
.channel-card--email:hover { transform: translateY(-5px); box-shadow: 0 16px 40px rgba(30,58,138,0.18); }
.channel-card--store {
  background: linear-gradient(135deg, #f8fafc, #f0f4ff);
  border-color: var(--gray-200); color: var(--gray-800);
}
.channel-card--store:hover { transform: translateY(-5px); box-shadow: 0 16px 40px rgba(30,58,138,0.1); border-color: rgba(30,58,138,0.25); }
.channel-card__icon { font-size: 28px; margin-bottom: 10px; opacity: 0.85; }
.channel-card__label { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.6; }
.channel-card__value { font-size: 17px; font-weight: 800; margin: 2px 0 4px; }
.channel-card__note { font-size: 12px; opacity: 0.6; line-height: 1.5; margin-bottom: 12px; }
.channel-card__cta { font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 5px; margin-top: auto; }

/* ── WA Info ───────────────────────────────────────────────── */
.wa-info { background: var(--navy-950); padding: 80px 28px; }
.wa-info__inner {
  max-width: 1000px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center;
}
.wa-info__text .section-tag {
  background: rgba(59,130,246,0.1); color: #93c5fd;
  border-color: rgba(59,130,246,0.2);
}
.wa-info__text .section-title { color: #fff; }
.wa-info__text .section-title em { color: #93c5fd; }
.wa-info__body {
  color: rgba(255,255,255,0.5); font-size: 15px; line-height: 1.8;
  margin: 0 0 24px;
}
.wa-info__body strong { color: #fff; }
.wa-steps { display: flex; flex-direction: column; gap: 12px; margin-bottom: 28px; }
.wa-step { display: flex; align-items: flex-start; gap: 12px; }
.wa-step__num {
  width: 26px; height: 26px; border-radius: 50%;
  background: var(--wa-green); color: #fff;
  font-size: 12px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px;
}
.wa-step__text { font-size: 13.5px; color: rgba(255,255,255,0.6); line-height: 1.65; }
.wa-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--wa-green); color: #fff;
  font-size: 14px; font-weight: 700;
  padding: 13px 24px; border-radius: 10px;
  text-decoration: none; transition: all 0.2s;
}
.wa-btn:hover { background: #22c55e; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,211,102,0.4); }

/* WA Chat Mockup */
.wa-chat-mockup {
  background: #e5ddd5;
  border-radius: 20px; overflow: hidden;
  box-shadow: 0 16px 48px rgba(0,0,0,0.4);
  max-width: 340px; margin: 0 auto;
}
.wm-header {
  background: #075e54; color: #fff;
  padding: 14px 18px; display: flex; align-items: center; gap: 10px;
}
.wm-avatar {
  width: 42px; height: 42px; border-radius: 50%;
  background: #25d366; display: flex; align-items: center; justify-content: center;
}
.wm-name { font-size: 15px; font-weight: 700; }
.wm-status { font-size: 11px; color: #a7f3d0; }
.wm-body { padding: 16px 14px; display: flex; flex-direction: column; gap: 8px; }
.wm-msg {
  max-width: 78%; padding: 9px 13px;
  border-radius: 12px; font-size: 13px; line-height: 1.55; color: #111;
}
.wm-msg--in { background: #fff; align-self: flex-start; border-bottom-left-radius: 3px; }
.wm-msg--out { background: #d9fdd3; align-self: flex-end; border-bottom-right-radius: 3px; }
.wm-img {
  background: rgba(255,255,255,0.7); border-radius: 10px;
  padding: 10px 14px; display: flex; align-items: center; gap: 8px;
  font-size: 12px; color: #555; align-self: flex-start;
  border: 1px solid rgba(0,0,0,0.08);
}
.wm-time { font-size: 10.5px; color: #999; text-align: right; }

/* ── Location ──────────────────────────────────────────────── */
.location { background: #fff; padding: 80px 28px; }
.location__inner { max-width: 1000px; margin: 0 auto; }
.loc-layout {
  display: grid; grid-template-columns: 1.3fr 1fr;
  gap: 48px; align-items: center; margin-top: 40px;
}
.loc-map {
  border-radius: 18px; overflow: hidden;
  border: 2px solid rgba(30,58,138,0.15);
  box-shadow: 0 8px 32px rgba(30,58,138,0.1);
  height: 360px;
}
.loc-map iframe { width: 100%; height: 100%; display: block; }
.loc-info { display: flex; flex-direction: column; gap: 14px; }
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
.loc-item__label { font-size: 10.5px; font-weight: 700; color: var(--gray-400); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2px; }
.loc-item__val   { font-size: 13.5px; font-weight: 600; color: var(--gray-700); }
.maps-btn {
  display: inline-flex; align-items: center; gap: 7px;
  background: var(--navy-500); color: #fff;
  padding: 12px 22px; border-radius: 10px;
  font-size: 14px; font-weight: 600; text-decoration: none;
  margin-top: 6px; transition: all 0.2s;
}
.maps-btn:hover { background: var(--navy-600); transform: translateY(-2px); box-shadow: 0 6px 18px rgba(30,58,138,0.35); }

/* ── FAQ Snippet ───────────────────────────────────────────── */
.faq-snip { background: rgba(30,58,138,0.04); padding: 80px 28px; }
.faq-snip__inner { max-width: 700px; margin: 0 auto; text-align: center; }
.faq-list { display: flex; flex-direction: column; gap: 8px; margin-top: 36px; text-align: left; }
.faq-item {
  background: #fff; border: 1.5px solid var(--gray-100);
  border-radius: 12px; overflow: hidden; cursor: pointer;
  transition: border-color 0.18s, box-shadow 0.18s;
}
.faq-item:hover { border-color: rgba(30,58,138,0.2); }
.faq-item--open { border-color: rgba(30,58,138,0.25); box-shadow: 0 4px 16px rgba(30,58,138,0.1); }
.faq-item__q {
  display: flex; justify-content: space-between; align-items: center;
  gap: 12px; padding: 16px 20px; font-size: 14.5px; font-weight: 600; color: var(--gray-800);
}
.faq-toggle { color: var(--gray-400); flex-shrink: 0; }
.faq-item--open .faq-toggle { color: var(--navy-600); }
.faq-item__a-wrap {
  display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.24s ease;
}
.faq-item--open .faq-item__a-wrap { grid-template-rows: 1fr; }
.faq-item__a {
  overflow: hidden; font-size: 13.5px; color: var(--gray-500);
  line-height: 1.75; padding: 0 20px;
}
.faq-item--open .faq-item__a { padding: 0 20px 16px; }
.btn-secondary {
  display: inline-flex; align-items: center; gap: 7px;
  background: var(--navy-500); color: #fff;
  padding: 12px 22px; border-radius: 10px;
  font-family: inherit; font-size: 14px; font-weight: 600;
  text-decoration: none; transition: all 0.2s;
}
.btn-secondary:hover { background: var(--navy-600); transform: translateY(-2px); box-shadow: 0 6px 18px rgba(30,58,138,0.3); }

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 768px) {
  .channels__inner { grid-template-columns: 1fr; }
  .wa-info__inner  { grid-template-columns: 1fr; }
  .loc-layout      { grid-template-columns: 1fr; }
  .loc-map         { height: 260px; }
}
</style>
