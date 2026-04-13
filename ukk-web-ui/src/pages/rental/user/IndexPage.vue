<template>
  <div class="landing">


    <!-- ── HERO ─────────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero__bg">
        <div class="hero__grid" />
        <div class="hero__orb hero__orb--1" />
        <div class="hero__orb hero__orb--2" />
        <div class="hero__orb hero__orb--3" />
      </div>

      <div class="hero__inner">
        <div class="hero__badge">
          <span class="hero__badge-dot" />
          <q-icon name="camera_alt" size="12px" />
          Rental Peralatan Foto · Bandung
        </div>

        <h1 class="hero__title">
          Sewa Alat Foto<br />
          <span class="hero__title--accent">Profesional,</span>
          <span class="hero__title--light"> Mudah &amp; Terpercaya.</span>
        </h1>

        <p class="hero__sub">
          Kamera, lensa, drone, lighting — semua tersedia dengan harga terjangkau.
          Pesan online, ambil langsung ke toko kami di Bandung — cepat, mudah, dan terpercaya.
        </p>

        <div class="hero__actions">
          <button class="btn btn--primary btn--lg" @click="$router.push({ name: 'rental/user/items' })">
            <q-icon name="photo_camera" size="17px" />
            Lihat Semua Alat
          </button>
          <button v-if="isLoggedIn" class="btn btn--ghost btn--lg" @click="$router.push({ name: 'rental/user/rental-histories' })">
            <q-icon name="history" size="16px" />
            Riwayat Booking
          </button>
          <button v-else class="btn btn--outline-white btn--lg" @click="$router.push({ name: 'login' })">
            <q-icon name="login" size="16px" />
            Masuk / Daftar
          </button>
        </div>

        <div class="hero__stats">
          <div class="hero__stat">
            <div class="hero__stat-num">50<span class="hero__stat-accent">+</span></div>
            <div class="hero__stat-label">Item Tersedia</div>
          </div>
          <div class="hero__stat-sep" />
          <div class="hero__stat">
            <div class="hero__stat-num">Rp<span class="hero__stat-accent"> 0</span></div>
            <div class="hero__stat-label">Biaya Pendaftaran</div>
          </div>
          <div class="hero__stat-sep" />
          <div class="hero__stat">
            <div class="hero__stat-num">24<span class="hero__stat-accent">/7</span></div>
            <div class="hero__stat-label">Customer Support</div>
          </div>
        </div>
      </div>

      <div class="hero__scroll">
        <div class="hero__scroll-line" />
        <q-icon name="keyboard_arrow_down" size="18px" />
      </div>
    </section>

    <!-- ── BRANDS / MITRA ────────────────────────────────────────── -->
    <section class="brands-section">
      <div class="container">
        <p class="brands-title">Brand Pilihan Terbaik untuk Karya Anda</p>
        <div class="brands-grid">
          <div class="brand-item">Sony</div>
          <div class="brand-item">Canon</div>
          <div class="brand-item">Fujifilm</div>
          <div class="brand-item">Nikon</div>
          <div class="brand-item">DJI</div>
          <div class="brand-item">Godox</div>
        </div>
      </div>
    </section>

    <!-- ── CARA KERJA ────────────────────────────────────────────── -->
    <section class="section how reveal-section">
      <div class="container">
        <div class="section__head">
          <div class="section__tag">Cara Kerja</div>
          <h2 class="section__title">Empat Langkah Mudah</h2>
          <p class="section__sub">Dari memilih alat hingga alat tiba di tangan Anda — semua prosesnya sederhana dan terlacak secara real-time.</p>
        </div>

        <div class="steps">
          <div class="steps__connector" />
          <div class="step" v-for="(step, i) in steps" :key="i">
            <div class="step__num">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="step__icon-wrap">
              <q-icon :name="step.icon" size="24px" />
            </div>
            <div class="step__content">
              <div class="step__title">{{ step.title }}</div>
              <div class="step__desc">{{ step.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── KATEGORI ────────────────────────────────────────────── -->
    <section class="section section--navy categories reveal-section">
      <div class="container">
        <div class="section__head">
          <div class="section__tag section__tag--light">Koleksi Kami</div>
          <h2 class="section__title section__title--light">Apa yang Bisa Disewa?</h2>
          <p class="section__sub section__sub--light">Dari kamera entry-level hingga perlengkapan profesional — tersedia untuk semua kebutuhan sesi foto Anda.</p>
        </div>

        <div class="cat-grid">
          <div
            class="cat-card"
            v-for="cat in categories"
            :key="cat.title"
            @click="goToItems(cat.filter)"
          >
            <div class="cat-card__glow" />
            <div class="cat-card__icon-wrap">
              <q-icon :name="cat.icon" size="26px" />
            </div>
            <div class="cat-card__title">{{ cat.title }}</div>
            <div class="cat-card__desc">{{ cat.desc }}</div>
            <div class="cat-card__cta">
              Lihat Koleksi
              <q-icon name="arrow_forward" size="13px" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── KEUNGGULAN ──────────────────────────────────────────── -->
    <section class="section why reveal-section">
      <div class="container">
        <div class="why__layout">
          <div class="why__left">
            <div class="section__tag">Kenapa Kami?</div>
            <h2 class="section__title">Rental yang Bisa<br />Diandalkan</h2>
            <p class="section__sub">
              Kami tidak sekadar meminjamkan alat. Setiap proses dirancang agar pelanggan merasa aman, nyaman, dan percaya.
            </p>
            <button v-if="isLoggedIn" class="btn btn--primary q-mt-md" @click="$router.push({ name: 'rental/user/items' })">
              <q-icon name="camera" size="16px" />
              Mulai Booking
            </button>
            <div class="why__deco">
              <div class="why__ring why__ring--1" />
              <div class="why__ring why__ring--2" />
              <div class="why__ring-dot" />
            </div>
          </div>

          <div class="why__right">
            <div class="why-card" v-for="item in whyItems" :key="item.title">
              <div class="why-card__icon">
                <q-icon :name="item.icon" size="20px" />
              </div>
              <div class="why-card__body">
                <div class="why-card__title">{{ item.title }}</div>
                <div class="why-card__desc">{{ item.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── STATUS FLOW ─────────────────────────────────────────── -->
    <section class="section section--navy flow reveal-section">
      <div class="container">
        <div class="section__head">
          <div class="section__tag section__tag--light">Alur Status Booking</div>
          <h2 class="section__title section__title--light">Pantau Pesanan Real-Time</h2>
          <p class="section__sub section__sub--light">Setiap perubahan status dapat dipantau langsung di halaman riwayat booking Anda.</p>
        </div>

        <div class="flow-track">
          <div class="flow-line" />
          <div class="flow-node" v-for="(s, i) in statusFlow" :key="s.value">
            <div class="flow-node__step">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="flow-node__dot" :class="`flow-node__dot--${s.color}`">
              <q-icon :name="s.icon" size="16px" />
            </div>
            <div class="flow-node__label">{{ s.label }}</div>
            <div class="flow-node__desc">{{ s.desc }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── PEMBAYARAN ──────────────────────────────────────────── -->
    <section class="section payment reveal-section">
      <div class="container">
        <div class="section__head">
          <div class="section__tag">Pembayaran</div>
          <h2 class="section__title">Metode Pembayaran</h2>
          <p class="section__sub">Bayar sesuai preferensi Anda. Deposit dikembalikan penuh setelah alat kembali dalam kondisi baik — tidak ada biaya tersembunyi.</p>
        </div>

        <div class="pay-grid">
          <!-- Transfer Bank -->
          <div class="pay-card pay-card--featured">
            <div class="pay-card__head">
              <div class="pay-card__icon">
                <q-icon name="account_balance" size="22px" />
              </div>
              <div>
                <div class="pay-card__label">Transfer Bank</div>
                <div class="pay-card__badge">Direkomendasikan</div>
              </div>
            </div>
            <div class="pay-card__desc">Lakukan transfer ke rekening kami, kemudian <strong>kirim bukti transfer via WhatsApp</strong> ke nomor admin. Setelah dikonfirmasi, status booking akan diperbarui.</div>
            <div class="pay-card__steps">
              <div class="pay-step">
                <div class="pay-step__num">1</div>
                <div class="pay-step__text">Lakukan transfer ke rekening yang tertera</div>
              </div>
              <div class="pay-step">
                <div class="pay-step__num">2</div>
                <div class="pay-step__text">Kirim foto bukti transfer ke WhatsApp admin</div>
              </div>
              <div class="pay-step">
                <div class="pay-step__num">3</div>
                <div class="pay-step__text">Tunggu konfirmasi dari admin (maks. 2 jam)</div>
              </div>
            </div>
            <a href="https://wa.me/6281234567890" target="_blank" class="pay-wa-btn">
              <q-icon name="chat" size="16px" />
              Kirim Bukti ke WhatsApp
            </a>
          </div>

          <!-- COD -->
          <div class="pay-card">
            <div class="pay-card__head">
              <div class="pay-card__icon">
                <q-icon name="payments" size="22px" />
              </div>
              <div class="pay-card__label">COD (Bayar di Toko)</div>
            </div>
            <div class="pay-card__desc">Bayar tunai secara langsung saat mengambil alat di toko kami. Tidak perlu transfer terlebih dahulu.</div>
            <div class="pay-card__steps">
              <div class="pay-step">
                <div class="pay-step__num">1</div>
                <div class="pay-step__text">Buat booking secara online</div>
              </div>
              <div class="pay-step">
                <div class="pay-step__num">2</div>
                <div class="pay-step__text">Datang ke toko sesuai tanggal sewa</div>
              </div>
              <div class="pay-step">
                <div class="pay-step__num">3</div>
                <div class="pay-step__text">Bayar tunai dan ambil alat langsung</div>
              </div>
            </div>
          </div>

          <!-- Deposit -->
          <div class="pay-deposit">
            <div class="pay-deposit__icon">
              <q-icon name="shield" size="20px" />
            </div>
            <div>
              <div class="pay-deposit__title">Sistem Deposit Transparan</div>
              <div class="pay-deposit__desc">Deposit wajib dibayar saat pengambilan alat sebagai jaminan. Dikembalikan 100% saat alat dikembalikan dalam kondisi baik — tidak ada biaya tersembunyi.</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── LOKASI ──────────────────────────────────────────────── -->
    <section class="section section--navy location reveal-section">
      <div class="container">
        <div class="loc-layout">
          <div class="loc-info">
            <div class="section__tag section__tag--light">Lokasi Toko</div>
            <h2 class="section__title section__title--light">Kunjungi Toko Kami</h2>
            <p class="section__sub section__sub--light">
              Alat dapat diambil dan dikembalikan langsung ke toko kami. Tidak ada biaya pengiriman — cukup datang sesuai jadwal booking Anda.
            </p>
            <div class="loc-details">
              <div class="loc-detail-item">
                <div class="loc-detail-icon"><q-icon name="location_on" size="18px" /></div>
                <div>
                  <div class="loc-detail-label">Alamat</div>
                  <div class="loc-detail-val">Bandung, Jawa Barat</div>
                </div>
              </div>
              <div class="loc-detail-item">
                <div class="loc-detail-icon"><q-icon name="schedule" size="18px" /></div>
                <div>
                  <div class="loc-detail-label">Jam Operasional</div>
                  <div class="loc-detail-val">Senin – Sabtu · 08.00 – 20.00 WIB</div>
                </div>
              </div>
              <div class="loc-detail-item">
                <div class="loc-detail-icon"><q-icon name="store" size="18px" /></div>
                <div>
                  <div class="loc-detail-label">Metode Pickup</div>
                  <div class="loc-detail-val">Ambil langsung di toko (no delivery)</div>
                </div>
              </div>
            </div>
            <a
              href="https://maps.google.com/?q=Bandung,Jawa+Barat"
              target="_blank"
              class="btn btn--primary loc-map-btn"
            >
              <q-icon name="map" size="16px" />
              Buka di Google Maps
            </a>
          </div>

          <div class="loc-map">
            <div class="map-embed-wrap">
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
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────────────── -->
    <section class="cta reveal-section">
      <div class="cta__bg">
        <div class="cta__orb cta__orb--1" />
        <div class="cta__orb cta__orb--2" />
        <div class="cta__grid" />
      </div>
      <div class="cta__inner">
        <div class="section__tag cta__tag">Mulai Sekarang</div>
        <h2 class="cta__title">Siap Merekam<br /><em>Momen Terbaik?</em></h2>
        <p class="cta__sub">Temukan alat foto yang tepat dan buat booking dalam hitungan menit.</p>
        <div class="cta__actions">
          <button class="btn btn--primary btn--lg" @click="$router.push({ name: 'rental/user/items' })">
            <q-icon name="photo_camera" size="17px" />
            Jelajahi Alat Foto
          </button>
          <a href="https://wa.me/6281234567890" target="_blank" class="btn btn--outline-white btn--lg">
            <q-icon name="chat" size="17px" />
            Hubungi via WhatsApp
          </a>
        </div>
      </div>
    </section>

    <!-- ── FOOTER ─────────────────────────────────────────────── -->
    <footer class="footer">
      <div class="footer__inner">
        <div class="footer__brand">
          <div class="footer__logo">
            <q-icon name="camera_alt" size="18px" />
          </div>
          <span class="footer__name">RENTCAM</span>
          <p class="footer__tagline">Platform rental peralatan foto terpercaya di Bandung.</p>
        </div>
        <div class="footer__links">
          <div class="footer__col">
            <div class="footer__col-title">Navigasi</div>
            <router-link class="footer__link" to="/rental/user/items">Alat Foto</router-link>
            <router-link class="footer__link" to="/rental/user/how-to">Cara Sewa</router-link>
            <router-link class="footer__link" to="/rental/user/about">Tentang Kami</router-link>
            <router-link class="footer__link" to="/rental/user/faq">FAQ</router-link>
            <router-link class="footer__link" to="/rental/user/contact">Kontak Kami</router-link>
          </div>
          <div class="footer__col">
            <div class="footer__col-title">Akun</div>
            <router-link class="footer__link" to="/rental/user/rental-histories">Riwayat Booking</router-link>
            <router-link class="footer__link" to="/login">Masuk</router-link>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <span>&copy; 2026 RENTCAM · rental alat photo</span>
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, computed } from 'vue'
import { authStore } from 'src/stores/auth'

const router = useRouter()
const auth   = authStore()

const isLoggedIn = computed(() => !!auth.getToken())

const goToItems = (filter?: string) => {
  router.push({ name: 'rental/user/items', query: filter ? { category: filter } : {} })
}

// Scroll reveal
onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1 }
  )
  document.querySelectorAll('.reveal-section').forEach((el) => observer.observe(el))
})

const steps = [
  {
    icon: 'search',
    title: 'Pilih Alat',
    desc: 'Browse koleksi kamera, lensa, drone, dan aksesori. Filter berdasarkan kategori dan ketersediaan stok.',
  },
  {
    icon: 'calendar_today',
    title: 'Tentukan Tanggal',
    desc: 'Pilih tanggal mulai dan selesai. Minimal 1 hari. Sistem cek otomatis ketersediaan stok secara real-time.',
  },
  {
    icon: 'chat',
    title: 'Bayar & Kirim Bukti WA',
    desc: 'Transfer ke rekening kami, lalu kirim bukti bayar via WhatsApp. COD bisa bayar tunai langsung di toko.',
  },
  {
    icon: 'storefront',
    title: 'Ambil di Toko',
    desc: 'Datang ke toko kami di Bandung sesuai tanggal mulai sewa. Alat siap dan sudah dicek kondisinya.',
  },
]

const categories = [
  {
    icon: 'camera_alt',
    title: 'Kamera',
    desc: 'Mirrorless & DSLR dari berbagai brand untuk kebutuhan foto dan video profesional.',
    filter: 'kamera',
  },
  {
    icon: 'center_focus_strong',
    title: 'Lensa',
    desc: 'Lensa portrait, wide, telephoto, macro — berbagai mount tersedia.',
    filter: 'lensa',
  },
  {
    icon: 'flight',
    title: 'Drone',
    desc: 'Drone aerial untuk foto dan video dari ketinggian dengan hasil sinematik.',
    filter: 'drone',
  },
  {
    icon: 'wb_incandescent',
    title: 'Lighting',
    desc: 'Strobo, softbox, LED panel, dan aksesori pencahayaan lainnya.',
    filter: 'lighting',
  },
  {
    icon: 'videocam',
    title: 'Video',
    desc: 'Gimbal, monitor, mikrofon, dan perlengkapan produksi video.',
    filter: 'video',
  },
  {
    icon: 'photo_filter',
    title: 'Aksesori',
    desc: 'Filter, tripod, tas kamera, baterai, memory card, dan lain-lain.',
    filter: 'aksesori',
  },
]

const whyItems = [
  {
    icon: 'verified',
    title: 'Kondisi Alat Terjamin',
    desc: 'Setiap alat dicek dan dibersihkan sebelum diserahkan. Kami melampirkan berita acara kondisi alat.',
  },
  {
    icon: 'storefront',
    title: 'Pickup Langsung di Toko',
    desc: 'Ambil dan kembalikan alat langsung ke toko kami. Tidak ada biaya antar-jemput, lebih efisien!',
  },
  {
    icon: 'shield',
    title: 'Deposit Transparan',
    desc: 'Deposit dibayar saat pengambilan dan dikembalikan penuh setelah alat kembali dalam kondisi baik.',
  },
  {
    icon: 'support_agent',
    title: 'Support via WhatsApp',
    desc: 'Konfirmasi pembayaran, tanya info alat, atau lapor kendala — semua bisa via WhatsApp kami.',
  },
]

// Status flow sesuai dengan meta.ts
const statusFlow = [
  {
    value: 'menunggu_bayar',
    label: 'Menunggu Bayar',
    desc: 'Booking dibuat, lakukan pembayaran',
    icon: 'receipt_long',
    color: 'yellow',
  },
  {
    value: 'menunggu_verif',
    label: 'Menunggu Verifikasi',
    desc: 'Bukti bayar diterima, admin verifikasi',
    icon: 'fact_check',
    color: 'orange',
  },
  {
    value: 'diproses',
    label: 'Diproses',
    desc: 'Alat disiapkan, Anda bisa datang ke toko',
    icon: 'inventory_2',
    color: 'blue',
  },
  {
    value: 'aktif',
    label: 'Aktif',
    desc: 'Alat sudah di tangan Anda, masa sewa berjalan',
    icon: 'camera_alt',
    color: 'teal',
  },
  {
    value: 'selesai',
    label: 'Selesai',
    desc: 'Alat dikembalikan ke toko, deposit diproses',
    icon: 'task_alt',
    color: 'green',
  },
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Design Tokens ──────────────────────────────────────────── */
.landing {
  /* Navy / Dark Blue palette */
  --navy-950: #030c1f;
  --navy-900: #060e2b;
  --navy-800: #0a1940;
  --navy-700: #0f2258;
  --navy-600: #1a337a;
  --navy-500: #1e3a8a;
  --navy-400: #2563eb;
  --navy-300: #3b82f6;

  /* Grays */
  --gray-50:  #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-300: #cbd5e1;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;

  /* Blue accents */
  --blue-glow: rgba(30, 58, 138, 0.18);
  --blue-border: rgba(59, 130, 246, 0.2);

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.07);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.1);
  --shadow-lg: 0 12px 36px rgba(0,0,0,0.14);
  --shadow-blue: 0 8px 32px rgba(30,58,138,0.3);

  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  color: var(--gray-800);
  background: #fff;
}

/* ── Scroll Reveal ──────────────────────────────────────────── */
.reveal-section {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.reveal-section.is-visible {
  opacity: 1;
  transform: none;
}

/* ── Container ──────────────────────────────────────────────── */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 28px;
}
.section {
  padding: 96px 0;
}
.section--navy {
  background: var(--navy-900);
}

/* ── Section Head ────────────────────────────────────────────── */
.section__head {
  text-align: center;
  max-width: 580px;
  margin: 0 auto 60px;
}
.section__tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(30,58,138,0.08);
  color: var(--navy-600);
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 999px;
  border: 1px solid rgba(30,58,138,0.15);
  margin-bottom: 16px;
}
.section__tag--light {
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.7);
  border-color: rgba(255,255,255,0.15);
}
.section__title {
  font-size: clamp(24px, 3.5vw, 34px);
  font-weight: 800;
  color: var(--gray-800);
  line-height: 1.25;
  margin: 0 0 14px;
  letter-spacing: -0.02em;
}
.section__title--light { color: #fff; }
.section__sub {
  font-size: 15.5px;
  color: var(--gray-500);
  line-height: 1.8;
  margin: 0;
}
.section__sub--light { color: rgba(255,255,255,0.5); }

/* ── Navbar ──────────────────────────────────────────────────── */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(6,14,43,0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.navbar__inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 28px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 32px;
}
.navbar__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.navbar__logo {
  width: 34px; height: 34px;
  background: var(--navy-600);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
}
.navbar__name {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
}
.navbar__links {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  flex: 1;
}
.navbar__link {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 500;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: all 0.18s;
}
.navbar__link:hover,
.navbar__link.router-link-active {
  color: #fff;
  background: rgba(255,255,255,0.08);
}
.navbar__actions {
  margin-left: auto;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 24px;
  border-radius: var(--radius-sm);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  text-decoration: none;
  transition: all 0.2s ease;
  line-height: 1;
}
.btn--sm { padding: 9px 16px; font-size: 13px; }
.btn--lg { padding: 15px 30px; font-size: 15px; }

.btn--primary {
  background: var(--navy-500);
  color: #fff;
  box-shadow: var(--shadow-blue);
}
.btn--primary:hover {
  background: var(--navy-600);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(30,58,138,0.45);
}

.btn--ghost {
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.8);
  border: 1.5px solid rgba(255,255,255,0.15);
}
.btn--ghost:hover {
  background: rgba(255,255,255,0.13);
  color: #fff;
  border-color: rgba(255,255,255,0.3);
}

.btn--outline {
  background: transparent;
  color: rgba(255,255,255,0.7);
  border: 1.5px solid rgba(255,255,255,0.2);
}
.btn--outline:hover {
  background: rgba(255,255,255,0.06);
  color: #fff;
}

.btn--outline-white {
  background: transparent;
  color: rgba(255,255,255,0.75);
  border: 1.5px solid rgba(255,255,255,0.22);
}
.btn--outline-white:hover {
  background: rgba(255,255,255,0.08);
  color: #fff;
  border-color: rgba(255,255,255,0.4);
}

/* ── HERO ────────────────────────────────────────────────────── */
.hero {
  position: relative;
  background: var(--navy-950);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 140px 28px 100px;
}

.hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 52px 52px;
}

.hero__orb--1 {
  position: absolute;
  width: 700px; height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(30,58,138,0.22) 0%, transparent 65%);
  top: -200px; left: -200px;
  filter: blur(80px);
}
.hero__orb--2 {
  position: absolute;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 65%);
  bottom: -100px; right: -100px;
  filter: blur(100px);
}
.hero__orb--3 {
  position: absolute;
  width: 300px; height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 65%);
  top: 40%; right: 15%;
  filter: blur(60px);
}

.hero__inner {
  position: relative;
  max-width: 760px;
  text-align: center;
  animation: fadeUp 0.8s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: none; }
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.2);
  color: rgba(147, 197, 253, 1);
  font-family: 'DM Mono', monospace;
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 6px 16px;
  border-radius: 999px;
  margin-bottom: 32px;
}
.hero__badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #60a5fa;
  box-shadow: 0 0 8px #60a5fa;
  animation: pulseDot 2s ease infinite;
}
@keyframes pulseDot {
  0%,100% { box-shadow: 0 0 6px #60a5fa; }
  50%      { box-shadow: 0 0 16px #60a5fa, 0 0 28px rgba(59,130,246,0.3); }
}

.hero__title {
  font-size: clamp(38px, 6vw, 64px);
  font-weight: 800;
  color: #fff;
  line-height: 1.12;
  margin: 0 0 22px;
  letter-spacing: -0.025em;
  animation: fadeUp 0.7s 0.1s ease both;
}
.hero__title--accent {
  color: #93c5fd;
}
.hero__title--light {
  color: rgba(255,255,255,0.75);
}

.hero__sub {
  font-size: 16.5px;
  color: rgba(255,255,255,0.45);
  line-height: 1.85;
  max-width: 540px;
  margin: 0 auto 40px;
  animation: fadeUp 0.7s 0.18s ease both;
}

.hero__actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 64px;
  animation: fadeUp 0.7s 0.26s ease both;
}

.hero__stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 36px;
  animation: fadeUp 0.7s 0.34s ease both;
}
.hero__stat-num {
  font-size: 28px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1;
  margin-bottom: 4px;
}
.hero__stat-accent { color: #60a5fa; }
.hero__stat-label {
  font-size: 11.5px;
  color: rgba(255,255,255,0.35);
  font-weight: 500;
  letter-spacing: 0.04em;
}
.hero__stat-sep {
  width: 1px; height: 40px;
  background: rgba(255,255,255,0.08);
}

.hero__scroll {
  position: absolute;
  bottom: 36px; left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: rgba(255,255,255,0.2);
  animation: scrollBounce 2.5s ease infinite;
}
.hero__scroll-line {
  width: 1px; height: 28px;
  background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.2));
}
@keyframes scrollBounce {
  0%,100% { transform: translateX(-50%) translateY(0); }
  50%      { transform: translateX(-50%) translateY(6px); }
}

/* ── Brands ──────────────────────────────────────────────────── */
.brands-section {
  padding: 30px 0;
  border-bottom: 1px solid var(--gray-200);
  background: #fff;
}
.brands-title {
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-400);
  margin: 0 0 16px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.brands-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
  opacity: 0.6;
}
.brand-item {
  font-family: 'DM Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--gray-600);
  letter-spacing: 0.05em;
  transition: all 0.3s;
  cursor: default;
}
.brand-item:hover {
  color: var(--navy-500);
  transform: scale(1.05);
}

/* ── Steps ───────────────────────────────────────────────────── */
.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  position: relative;
}
.steps__connector {
  position: absolute;
  top: 28px; left: 12.5%; right: 12.5%;
  height: 1.5px;
  background: linear-gradient(to right, var(--navy-500), var(--navy-300));
  opacity: 0.25;
}
.step {
  background: var(--gray-50);
  border: 1.5px solid var(--gray-100);
  border-radius: var(--radius-lg);
  padding: 28px 22px;
  position: relative;
  transition: all 0.2s;
}
.step:hover {
  border-color: var(--navy-300);
  background: rgba(30,58,138,0.04);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(30,58,138,0.1);
}
.step__num {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  color: var(--navy-400);
  letter-spacing: 0.1em;
  margin-bottom: 16px;
}
.step__icon-wrap {
  width: 48px; height: 48px;
  background: var(--navy-500);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  margin-bottom: 16px;
  box-shadow: 0 4px 14px rgba(30,58,138,0.3);
}
.step__title {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--gray-800);
  margin-bottom: 8px;
}
.step__desc {
  font-size: 13px;
  color: var(--gray-500);
  line-height: 1.7;
}

/* ── Categories ──────────────────────────────────────────────── */
.cat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.cat-card {
  position: relative;
  background: rgba(255,255,255,0.04);
  border: 1.5px solid rgba(255,255,255,0.07);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
  cursor: pointer;
  transition: all 0.22s;
  overflow: hidden;
}
.cat-card__glow {
  position: absolute;
  top: -40px; left: -40px;
  width: 140px; height: 140px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.cat-card:hover {
  border-color: rgba(59,130,246,0.3);
  background: rgba(255,255,255,0.07);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.3);
}
.cat-card:hover .cat-card__glow { opacity: 1; }
.cat-card__icon-wrap {
  width: 52px; height: 52px;
  background: rgba(59,130,246,0.12);
  border: 1px solid rgba(59,130,246,0.2);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  color: #93c5fd;
  margin-bottom: 16px;
}
.cat-card__title {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.cat-card__desc {
  font-size: 13px;
  color: rgba(255,255,255,0.45);
  line-height: 1.65;
  margin-bottom: 16px;
}
.cat-card__cta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 600;
  color: #60a5fa;
  transition: gap 0.2s;
}
.cat-card:hover .cat-card__cta { gap: 10px; }

/* ── Why Us ──────────────────────────────────────────────────── */
.why__layout {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 64px;
  align-items: center;
}
.why__left {
  position: relative;
}
.why__deco {
  position: absolute;
  bottom: -60px; right: -40px;
  pointer-events: none;
}
.why__ring {
  position: absolute;
  border-radius: 50%;
  border: 1.5px solid rgba(30,58,138,0.15);
}
.why__ring--1 { width: 160px; height: 160px; top: -80px; left: -80px; }
.why__ring--2 { width: 100px; height: 100px; top: -50px; left: -50px; }
.why__ring-dot {
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--navy-400);
  position: absolute;
  top: -80px; left: -10px;
  opacity: 0.4;
}
.why__right {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.why-card {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  background: var(--gray-50);
  border: 1.5px solid var(--gray-100);
  border-radius: var(--radius-md);
  padding: 20px 18px;
  transition: all 0.2s;
}
.why-card:hover {
  border-color: rgba(30,58,138,0.2);
  background: rgba(30,58,138,0.03);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.why-card__icon {
  width: 40px; height: 40px; flex-shrink: 0;
  background: var(--navy-500);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
}
.why-card__title {
  font-size: 14px;
  font-weight: 700;
  color: var(--gray-800);
  margin-bottom: 6px;
}
.why-card__desc {
  font-size: 12.5px;
  color: var(--gray-500);
  line-height: 1.65;
}

/* ── Status Flow ─────────────────────────────────────────────── */
.flow-track {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  position: relative;
}
.flow-line {
  position: absolute;
  top: 28px; left: 10%; right: 10%;
  height: 1.5px;
  background: linear-gradient(to right, rgba(255,255,255,0.06), rgba(255,255,255,0.15), rgba(255,255,255,0.06));
}
.flow-node {
  text-align: center;
  position: relative;
}
.flow-node__step {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: rgba(255,255,255,0.25);
  margin-bottom: 10px;
  letter-spacing: 0.08em;
}
.flow-node__dot {
  width: 54px; height: 54px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 14px;
  border: 2px solid;
  color: #fff;
}
.flow-node__dot--yellow  { background: rgba(234,179,8,0.15);  border-color: rgba(234,179,8,0.4);  }
.flow-node__dot--orange  { background: rgba(249,115,22,0.15); border-color: rgba(249,115,22,0.4); }
.flow-node__dot--blue    { background: rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.4); }
.flow-node__dot--teal    { background: rgba(20,184,166,0.15); border-color: rgba(20,184,166,0.4); }
.flow-node__dot--green   { background: rgba(34,197,94,0.15);  border-color: rgba(34,197,94,0.4);  }
.flow-node__label {
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}
.flow-node__desc {
  font-size: 11.5px;
  color: rgba(255,255,255,0.4);
  line-height: 1.6;
}

/* ── Payment ─────────────────────────────────────────────────── */
.pay-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  align-items: start;
  margin-top: 8px;
}
.pay-card {
  background: var(--gray-50);
  border: 1.5px solid var(--gray-100);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.pay-card:hover {
  border-color: rgba(30,58,138,0.2);
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(30,58,138,0.1);
}
.pay-card--featured {
  border-color: rgba(30,58,138,0.25);
  background: rgba(30,58,138,0.04);
  box-shadow: 0 4px 16px rgba(30,58,138,0.08);
}
.pay-card--featured:hover {
  border-color: var(--navy-400);
  box-shadow: 0 12px 32px rgba(30,58,138,0.18);
}
.pay-card__head {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}
.pay-card__icon {
  width: 42px; height: 42px;
  background: var(--navy-500);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  flex-shrink: 0;
}
.pay-card__label {
  font-size: 15px;
  font-weight: 700;
  color: var(--gray-800);
  line-height: 1.3;
}
.pay-card__badge {
  display: inline-block;
  background: var(--navy-500);
  color: #fff;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 999px;
  margin-top: 4px;
}
.pay-card__desc {
  font-size: 13px;
  color: var(--gray-500);
  line-height: 1.7;
  margin-bottom: 14px;
}
.pay-card__desc strong { color: var(--gray-800); }
.pay-card__steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.pay-step {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.pay-step__num {
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--navy-500);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}
.pay-step__text {
  font-size: 12.5px;
  color: var(--gray-600);
  line-height: 1.55;
}
.pay-wa-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #25d366;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
  margin-top: auto;
}
.pay-wa-btn:hover {
  background: #22c55e;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(37,211,102,0.35);
}
.pay-deposit {
  display: flex;
  flex-direction: column;
  gap: 0;
  background: rgba(30,58,138,0.05);
  border: 1.5px solid rgba(30,58,138,0.12);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
}
.pay-deposit__icon {
  width: 42px; height: 42px;
  background: var(--navy-500);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  flex-shrink: 0;
  margin-bottom: 14px;
}
.pay-deposit__title {
  font-size: 15px;
  font-weight: 700;
  color: var(--navy-700);
  margin-bottom: 8px;
}
.pay-deposit__desc {
  font-size: 13px;
  color: var(--gray-600);
  line-height: 1.7;
}

/* ── Location ────────────────────────────────────────────────── */
.loc-layout {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 60px;
  align-items: center;
}
.loc-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 24px 0 28px;
}
.loc-detail-item {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 12px 16px;
}
.loc-detail-icon {
  width: 38px; height: 38px;
  background: rgba(59,130,246,0.15);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #93c5fd;
  flex-shrink: 0;
}
.loc-detail-label {
  font-size: 10.5px;
  font-weight: 700;
  color: rgba(255,255,255,0.35);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 2px;
}
.loc-detail-val {
  font-size: 13.5px;
  font-weight: 600;
  color: #fff;
}
.loc-map-btn {
  margin-top: 4px;
}
.loc-map {
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 2px solid rgba(59,130,246,0.2);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}
.map-embed-wrap {
  width: 100%;
  height: 380px;
  position: relative;
}
.map-embed-wrap iframe {
  width: 100%;
  height: 100%;
  display: block;
}

/* ── CTA ─────────────────────────────────────────────────────── */
.cta {
  position: relative;
  overflow: hidden;
  background: var(--navy-950);
  padding: 100px 28px;
  text-align: center;
}
.cta__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.cta__orb--1 {
  position: absolute;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(30,58,138,0.25) 0%, transparent 65%);
  top: -150px; left: -100px;
  filter: blur(80px);
}
.cta__orb--2 {
  position: absolute;
  width: 400px; height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 65%);
  bottom: -100px; right: -60px;
  filter: blur(80px);
}
.cta__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
  background-size: 52px 52px;
}
.cta__inner {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}
.cta__tag {
  background: rgba(59,130,246,0.1);
  color: #93c5fd;
  border-color: rgba(59,130,246,0.2);
}
.cta__title {
  font-size: clamp(28px, 4.5vw, 48px);
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
  margin: 0 0 16px;
  letter-spacing: -0.02em;
}
.cta__title em {
  color: #93c5fd;
  font-style: normal;
}
.cta__sub {
  font-size: 16px;
  color: rgba(255,255,255,0.45);
  line-height: 1.7;
  margin-bottom: 36px;
}
.cta__actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* ── Footer ──────────────────────────────────────────────────── */
.footer {
  background: var(--navy-900);
  border-top: 1px solid rgba(255,255,255,0.05);
  padding: 60px 0 0;
}
.footer__inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 28px 48px;
  display: flex;
  gap: 64px;
  align-items: flex-start;
}
.footer__brand {
  flex: 1;
}
.footer__logo {
  width: 40px; height: 40px;
  background: var(--navy-600);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  margin-bottom: 10px;
}
.footer__name {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.footer__tagline {
  font-size: 13px;
  color: rgba(255,255,255,0.35);
  line-height: 1.6;
  margin: 0;
  max-width: 200px;
}
.footer__links {
  display: flex;
  gap: 48px;
}
.footer__col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.footer__col-title {
  font-size: 11px;
  font-weight: 700;
  color: rgba(255,255,255,0.4);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.footer__link {
  font-size: 13.5px;
  color: rgba(255,255,255,0.5);
  text-decoration: none;
  transition: color 0.18s;
}
.footer__link:hover { color: #fff; }
.footer__bottom {
  border-top: 1px solid rgba(255,255,255,0.05);
  padding: 18px 28px;
  text-align: center;
  font-size: 12px;
  color: rgba(255,255,255,0.2);
  max-width: 1100px;
  margin: 0 auto;
}

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 1000px) {
  .pay-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 900px) {
  .steps { grid-template-columns: repeat(2, 1fr); }
  .steps__connector { display: none; }
  .cat-grid { grid-template-columns: repeat(2, 1fr); }
  .why__layout { grid-template-columns: 1fr; gap: 40px; }
  .why__deco { display: none; }
  .flow-track { grid-template-columns: repeat(3, 1fr); }
  .flow-line { display: none; }
  .pay-grid { grid-template-columns: 1fr; gap: 16px; }
  .loc-layout { grid-template-columns: 1fr; gap: 36px; }
  .map-embed-wrap { height: 280px; }
  .footer__inner { flex-direction: column; gap: 36px; }
}
@media (max-width: 600px) {
  .steps { grid-template-columns: 1fr; }
  .cat-grid { grid-template-columns: 1fr; }
  .why__right { grid-template-columns: 1fr; }
  .flow-track { grid-template-columns: repeat(2, 1fr); }
  .navbar__links { display: none; }
}
</style>