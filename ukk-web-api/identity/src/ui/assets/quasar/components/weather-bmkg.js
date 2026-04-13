

const WeatherBmkg = {
  template: `
  <div class="row">
    <div v-if="weathers.current" class="col-12 col-sm-4">
      <q-card class="q-ma-sm" flat bordered>
        <q-item>
          <q-item-section avatar>
            <q-avatar size="52px" square>
              <img :src="weathers.current.image">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-h3 text-bold">{{weathers.current.weather_desc_en}}</q-item-label>
            <q-item-label class="text-h5 text-bold text-grey-8" >{{formatDate(weathers.current.datetime)}}</q-item-label>
          </q-item-section>
        </q-item>

        <q-card-section class="q-pt-none q-pb-xs q-px-md">
          <div class="text-bold">{{ weathers.location.provinsi || '' }}</div>
          <div class="text-caption ">
            {{ weathers.location.desa || '' }},
              {{ weathers.location.kecamatan || '' }},
              {{ weathers.location.kotkab || '' }}<br>
          </div>
        </q-card-section>

      </q-card>
    </div>
    <div class="col-12 col-sm-8 row">
    <template v-for="(w, i) in weathers.data" :key="i">
      <div v-if="i < 3" class="col-6 col-sm-4" @click="getWeather">
        <q-card class="q-ma-sm" flat bordered>
          <q-item>
            <q-item-section avatar>
              <q-avatar size="24px" square>
                <img :src="w.image">
              </q-avatar>
              <q-item-label class="text-bold text-h6">{{w.weather_desc_en}}</q-item-label>
              <q-item-label class="text-grey-8">{{formatDate(w.datetime, true)}}</q-item-label>
            </q-item-section>

          </q-item>

        </q-card>
      </div>
    </template>
    </div>
  </div>
  `,
  props: {
    admCode: { type: String, default: '16.13.04.2010' },
  },
  data() {
    return {
      weathers: {
        location: null,
        data: [],
        current: null,
      },
    }
  },
  computed: {
    //
  },
  methods: {
    async getWeather() {
      const apiWeather = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4="+this.admCode;
      this.weathers.location = null
      this.weathers.current = null
      this.weathers.data = []
      try {
        const response = await fetch(apiWeather);
        if (!response.ok) throw new Error("Gagal mengambil data dari server BMKG.");
        const res = await response.json();

        if (res.lokasi) this.weathers.location = res.lokasi
        if (res.data && res.data[0] && Array.isArray(res.data[0].cuaca)) {
          const r = res.data[0].cuaca
          const current = r[0] ?? []
          const today = r[1] ?? []
          const futures = r[2] ?? []
          if (current.length) this.weathers.data = [...this.weathers.data, ...current] 
          // if (today.length) this.weathers.data = [...this.weathers.data, ...today] 
          // if (futures.length) this.weathers.data = [...this.weathers.data, ...futures] 
          this.weathers.current = this.getCurrentWeather(this.weathers.data)

          if (!this.weathers.current && current.length) this.weathers.current = current[0]
        }
        this.renderWeather(res);
      } catch (err) {
        this.weatherBmkg = `<p id="error">ERROR: ${err.message}</p>`;
      }
    },
    renderWeather(data) {
      // console.log('renderWeather', data)
      if (!data) {
        this.weatherBmkg = "<p>Data tidak ditemukan.</p>";
        return;
      }

      let html = "";

      // Lokasi
      const lokasi = data.lokasi || {};
      if (lokasi.desa && lokasi.kecamatan) {
        html += `<h2>Desa/Kelurahan: ${this.escapeHTML(lokasi.desa)}</h2>`;
        html += `<p>
          Kecamatan: ${this.escapeHTML(lokasi.kecamatan || "N/A")}<br>
          Kota/Kab: ${this.escapeHTML(lokasi.kotkab || "N/A")}<br>
          Provinsi: ${this.escapeHTML(lokasi.provinsi || "N/A")}<br>
          Koordinat: Lat: ${this.escapeHTML(lokasi.lat || "N/A")}, Lon: ${this.escapeHTML(lokasi.lon || "N/A")}<br>
          Timezone: ${this.escapeHTML(lokasi.timezone || "N/A")}<br>
        </p>`;
      } else {
        html += "<h2>Lokasi Tidak Ditemukan</h2>";
      }

      // Detail Cuaca
      html += "<h3>Detail Prakiraan Cuaca:</h3>";

      if (data.data && data.data[0] && Array.isArray(data.data[0].cuaca)) {
        data.data[0].cuaca.forEach((hari, i) => {
          html += `<h4>Hari ke-${i + 1}</h4><ul>`;
          if (Array.isArray(hari)) {
            hari.forEach((p) => {
              const waktu = this.escapeHTML(p.local_datetime || "N/A");
              const deskripsi = this.escapeHTML(p.weather_desc || "N/A");
              const suhu = this.escapeHTML(p.t || "N/A");
              const kelembapan = this.escapeHTML(p.hu || "N/A");
              const kecAngin = this.escapeHTML(p.ws || "N/A");
              const arahAngin = this.escapeHTML(p.wd || "N/A");
              const jarakPandang = this.escapeHTML(p.vs_text || "N/A");
              const img = p.image ? p.image.replace(/ /g, "%20") : "";
              const alt = deskripsi || "Ikon Cuaca";

              html += `<li>
                <strong>Jam:</strong> ${waktu} |
                <strong>Cuaca:</strong> ${deskripsi}`;
              if (img && this.isValidUrl(img)) {
                html += ` <img src="${img}" alt="${alt}" title="${alt}"> |`;
              }
              html += ` <strong>Suhu:</strong> ${suhu}°C |
                <strong>Kelembapan:</strong> ${kelembapan}% |
                <strong>Kec. Angin:</strong> ${kecAngin} km/j |
                <strong>Arah Angin:</strong> dari ${arahAngin} |
                <strong>Jarak Pandang:</strong> ${jarakPandang}
              </li>`;
            });
          } else {
            html += "<li>Data tidak valid.</li>";
          }
          html += "</ul>";
        });
      } else {
        html += "<p>Struktur data prakiraan cuaca tidak ditemukan.</p>";
      }

      this.weatherBmkg = html;
    },
    escapeHTML(str) {
      return str
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    },
    isValidUrl(url) {
      try {
        new URL(url);
        return true;
      } catch {
        return false;
      }
    },
    formatDate(dateStr, timeOnly = false) {
      const date = new Date(dateStr)

      // Nama bulan singkat (Inggris)
      const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

      const day = date.getDate()
      const month = monthNames[date.getMonth()]
      const year = date.getFullYear()

      const hours = String(date.getHours()).padStart(2, "0")
      const minutes = String(date.getMinutes()).padStart(2, "0")

      if (timeOnly) return `${hours}:${minutes}`
      return `${day} ${month} ${year} - ${hours}:${minutes}`
    },
    getCurrentWeather(data) {
      const now = new Date() // waktu sistem lokal

      // cari data yang cocok dengan jam terdekat (<= sekarang, dan < 3 jam berikutnya)
      return data.find((item, index) => {
        const itemTime = new Date(item.datetime.replace(" ", "T"))
        // console.log('v', now, itemTime, item)
        const nextItem = data[index + 1]
          ? new Date(data[index + 1].datetime.replace(" ", "T"))
          : null

        // jika ini adalah slot waktu yang sedang berlangsung
        if (nextItem) {
          return now >= itemTime && now < nextItem
        } else {
          // jika ini data terakhir, ambil kalau sekarang >= jamnya
          return now >= itemTime
        }
      }) || null
    }
  },
  mounted() {
    this.getWeather()
  },
}
