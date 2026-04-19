<template>
  <div class="q-pa-lg" style="background-color: #f4f7fb; min-height: calc(100vh - 50px)">
    <div class="row items-center justify-between q-mb-xl">
      <div>
        <div class="text-h4 text-weight-bolder q-mb-xs text-dark" style="letter-spacing: -0.5px">Analytics Dashboard</div>
        <div class="text-subtitle1 text-grey-7 tracking-wide">Summary of your rental operational data</div>
      </div>
      <div class="row items-center q-gutter-x-sm">
        <div class="text-caption text-weight-bold text-grey-6 text-uppercase q-mr-sm">Range:</div>
        <q-input
          v-model="startDate"
          type="date"
          dense
          outlined
          bg-color="white"
          @update:model-value="applyFilter"
          style="width: 140px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-radius: 8px"
        />
        <div class="text-weight-bold text-grey-5">-</div>
        <q-input
          v-model="endDate"
          type="date"
          dense
          outlined
          bg-color="white"
          @update:model-value="applyFilter"
          style="width: 140px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-radius: 8px"
        />
      </div>
    </div>

    <div class="row q-col-gutter-lg q-mb-xl">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-white shadow-1 card-hover text-dark" style="border-radius: 20px; border: 1px solid #edf2f7">
          <q-card-section>
            <div class="row items-center no-wrap">
              <div class="col">
                <div class="text-caption text-weight-bold text-grey-6 text-uppercase tracking-wide" style="letter-spacing: 0.5px">Total Income</div>
                <div class="text-h5 text-weight-bolder q-mt-xs text-primary">{{ formatCurrency(totalIncome) }}</div>
              </div>
              <div class="col-auto">
                <div class="flex flex-center bg-blue-1" style="height: 54px; width: 54px; border-radius: 16px">
                  <q-icon name="payments" size="28px" color="primary" />
                </div>
              </div>
            </div>
            <div class="q-mt-sm text-caption text-weight-medium">
              <span class="text-positive"><q-icon name="trending_up" size="xs" /> +8.4%</span> <span class="text-grey-5">this month</span>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-white shadow-1 card-hover text-dark" style="border-radius: 20px; border: 1px solid #edf2f7">
          <q-card-section>
            <div class="row items-center no-wrap">
              <div class="col">
                <div class="text-caption text-weight-bold text-grey-6 text-uppercase tracking-wide">Total Transactions</div>
                <div class="text-h5 text-weight-bolder q-mt-xs text-positive">{{ totalRentals }} Data</div>
              </div>
              <div class="col-auto">
                <div class="flex flex-center bg-green-1" style="height: 54px; width: 54px; border-radius: 16px">
                  <q-icon name="receipt_long" size="28px" color="positive" />
                </div>
              </div>
            </div>
            <div class="q-mt-sm text-caption text-weight-medium">
              <span class="text-positive"><q-icon name="trending_up" size="xs" /> +12.1%</span> <span class="text-grey-5">this month</span>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-white shadow-1 card-hover text-dark" style="border-radius: 20px; border: 1px solid #edf2f7">
          <q-card-section>
            <div class="row items-center no-wrap">
              <div class="col">
                <div class="text-caption text-weight-bold text-grey-6 text-uppercase tracking-wide">Registered Customers</div>
                <div class="text-h5 text-weight-bolder q-mt-xs text-orange-8">{{ totalCustomers }} People</div>
              </div>
              <div class="col-auto">
                <div class="flex flex-center bg-orange-1" style="height: 54px; width: 54px; border-radius: 16px">
                  <q-icon name="people" size="28px" color="orange-8" />
                </div>
              </div>
            </div>
            <div class="q-mt-sm text-caption text-weight-medium">
              <span class="text-positive"><q-icon name="trending_up" size="xs" /> +5.2%</span> <span class="text-grey-5">this month</span>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-white shadow-1 card-hover text-dark" style="border-radius: 20px; border: 1px solid #edf2f7">
          <q-card-section>
            <div class="row items-center no-wrap">
              <div class="col">
                <div class="text-caption text-weight-bold text-grey-6 text-uppercase tracking-wide">Equipment Catalog</div>
                <div class="text-h5 text-weight-bolder q-mt-xs text-info">{{ totalItems }} Units</div>
              </div>
              <div class="col-auto">
                <div class="flex flex-center bg-cyan-1" style="height: 54px; width: 54px; border-radius: 16px">
                  <q-icon name="inventory_2" size="28px" color="info" />
                </div>
              </div>
            </div>
            <div class="q-mt-sm text-caption text-weight-medium">
              <span class="text-grey-5">Available in inventory</span>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Chart & Status Breakdown -->
    <div class="row q-col-gutter-lg q-mb-lg">
      <div class="col-12 col-md-8">
        <q-card class="shadow-1 bg-white" style="border-radius: 20px; border: 1px solid #edf2f7; height: 100%">
          <q-card-section class="q-pb-xs">
            <div class="text-h6 text-weight-bolder text-dark row items-center q-gutter-x-sm">
              <q-icon name="trending_up" color="primary" size="sm" />
              <span>Income Trend</span>
            </div>
          </q-card-section>
          
          <q-card-section class="q-pt-xl q-pb-lg relative-position">
            <!-- Grid Lines -->
            <div class="absolute-top-left full-width full-height q-px-xl" style="z-index: 0; padding-top: 48px; padding-bottom: 40px; opacity: 0.08">
              <div style="height: 25%; border-bottom: 1px dashed black"></div>
              <div style="height: 25%; border-bottom: 1px dashed black"></div>
              <div style="height: 25%; border-bottom: 1px dashed black"></div>
              <div style="height: 25%; border-bottom: 1px solid black"></div>
            </div>

            <div class="scroll-x no-wrap" style="height: 240px; overflow-x: auto; overflow-y: hidden">
              <div class="row items-end justify-around relative-position" style="height: 100%; min-width: 500px; z-index: 1;">
                
                <!-- SVG Area and Line -->
                <svg class="absolute" viewBox="0 0 100 100" preserveAspectRatio="none" style="top: 0; left: 0; right: 0; bottom: 38px; width: 100%; height: calc(100% - 38px); z-index: 0; pointer-events: none; overflow: visible" v-if="chartReady">
                  <defs>
                    <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#5c6bc0" stop-opacity="0.3" />
                      <stop offset="100%" stop-color="#5c6bc0" stop-opacity="0.0" />
                    </linearGradient>
                  </defs>
                  <!-- Area filled under the curve -->
                  <path :d="areaPath" fill="url(#areaGradient)" style="transition: d 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)" />
                  <!-- Thick Smooth Line -->
                  <path :d="linePath" fill="none" class="animated-line" stroke="#5c6bc0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke" style="transition: d 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); filter: drop-shadow(0px 6px 8px rgba(92, 107, 192, 0.4))" />
                </svg>

                <!-- SVG Dots -->
                <svg class="absolute" style="top: 0; left: 0; right: 0; bottom: 38px; width: 100%; height: calc(100% - 38px); z-index: 1; pointer-events: none; overflow: visible" v-if="chartReady">
                  <circle v-for="(day, i) in chartData" :key="'dot-'+i"
                    :cx="((i + 0.5) / chartData.length * 100) + '%'"
                    :cy="(100 - Math.max(day.percentage, 1)) + '%'"
                    r="5"
                    fill="white"
                    stroke="#5c6bc0"
                    stroke-width="2.5"
                    v-show="day.value > 0"
                    style="transition: cx 0.5s ease, cy 0.5s ease"
                  />
                </svg>

                <!-- Interactive Invisible Columns for Tooltips -->
                <div v-for="(day, index) in chartData" :key="index" class="col text-center hover-column" style="display: flex; flex-direction: column; justify-content: flex-end; align-items: center; position: relative; height: 100%">
                  
                  <!-- Tooltip Bubble (Visible on Hover) -->
                  <div 
                    class="text-weight-bold bg-dark text-white shadow-6 bubble-val" 
                    style="font-size: 0.70rem; padding: 4px 10px; border-radius: 8px; position: absolute; top: 10px; opacity: 0; transform: translateY(10px); transition: all 0.2s ease; z-index: 10; white-space: nowrap"
                    v-if="day.value > 0"
                  >
                    <span class="opacity-80">{{ day.tooltipLabel || day.label }} : </span><span class="text-primary-1">{{ formatCurrency(day.value) }}</span>
                  </div>

                  <!-- Invisible vertical bar to catch hover -->
                  <div class="hover-bar" style="width: 100%; height: calc(100% - 38px); position: absolute; bottom: 38px; transition: all 0.2s ease"></div>

                  <!-- X-Axis Labels -->
                  <div 
                    class="text-caption q-mt-sm q-mb-sm text-weight-bolder text-uppercase" 
                    :class="index === chartData.length - 1 ? 'text-primary' : 'text-grey-5'" 
                    style="letter-spacing: 0.5px; height: 20px; line-height: 20px; z-index: 2"
                  >
                    {{ day.label }}
                  </div>
                </div>
            </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card class="shadow-1 bg-white" style="border-radius: 20px; border: 1px solid #edf2f7; height: 100%">
          <q-card-section class="q-pb-xs">
            <div class="text-h6 text-weight-bolder text-dark row items-center q-gutter-x-sm">
              <q-icon name="donut_large" color="primary" size="sm" />
              <span>Transaction Status</span>
            </div>
          </q-card-section>
          <q-card-section>
            <div class="row items-center justify-center q-gutter-x-xl q-pt-md">
              <div class="col-auto">
                <div class="donut-chart shadow-3" :style="donutStyle">
                  <div class="donut-inner text-center flex flex-center column">
                    <div class="text-grey-6 text-weight-bold" style="font-size: 0.70rem">TOTAL</div>
                    <div class="text-weight-bolder text-dark" style="font-size: 1.5rem; line-height: 1.2">{{ totalRentals }}</div>
                  </div>
                </div>
              </div>
              <div class="col-12 q-mt-lg">
                <q-list dense>
                  <q-item v-for="(count, status) in statusCounts" :key="status" class="q-px-sm q-py-sm transition-item" style="border-radius: 8px">
                    <q-item-section avatar style="min-width: 32px">
                      <div style="width: 14px; height: 14px; border-radius: 4px;" :style="{ background: getHexColor(status) }"></div>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label class="text-weight-bold text-capitalize text-grey-9 text-caption">{{ status.replace('_', ' ') }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <span class="text-weight-bolder text-dark" style="font-size: 1.05rem">{{ count }}</span>
                    </q-item-section>
                  </q-item>
                  <q-item v-if="Object.keys(statusCounts).length === 0">
                    <q-item-section class="text-grey-6 text-center q-py-lg">No transactions yet</q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Recent -->
    <div class="row q-col-gutter-lg">
      <div class="col-12">
        <q-card class="shadow-1 bg-white" style="border-radius: 20px; border: 1px solid #edf2f7; height: 100%">
          <q-card-section class="q-pb-xs">
            <div class="text-h6 text-weight-bolder text-dark row items-center q-gutter-x-sm">
              <q-icon name="history" color="primary" size="sm" />
              <span>Ten Most Recent Transactions</span>
            </div>
          </q-card-section>
          <q-card-section>
            <q-list separator>
              <q-item v-for="rental in recentRentals" :key="rental.id" class="q-py-md transition-item" clickable @click="viewRental(rental)">
                <q-item-section avatar>
                  <q-avatar :color="getStatusColor(rental.status)" text-color="white" icon="receipt_long" />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-weight-bold text-dark" style="font-size: 1.05rem;">{{ rental.rental_code }}</q-item-label>
                  <q-item-label caption class="q-mt-xs">
                    <q-icon name="person" size="xs" /> {{ rental.customer_name ?? 'Customer' }} &nbsp;&bull;&nbsp; 
                    <span class="text-weight-medium text-capitalize">{{ rental.payment_method }}</span>
                  </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label class="text-weight-bold text-teal-8" style="font-size: 1.05rem;">{{ formatCurrency(rental.grand_total) }}</q-item-label>
                  <q-item-label caption class="text-capitalize q-mt-xs text-weight-bold" :class="'text-' + getStatusColor(rental.status)">{{ rental.status.replace('_', ' ') }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item v-if="recentRentals.length === 0">
                <q-item-section class="text-grey-6 text-center q-py-lg">No recent transactions</q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'

const API = new Api()
const router = useRouter()

const sd = new Date()
sd.setDate(sd.getDate() - 14)
const ed = new Date()

const startDate = ref(sd.toISOString().split('T')[0])
const endDate = ref(ed.toISOString().split('T')[0])

const totalIncome = ref(0)
const totalRentals = ref(0)
const totalCustomers = ref(0)
const totalItems = ref(0)

const allRentals = ref<any[]>([])
const statusCounts = ref<Record<string, number>>({})
const recentRentals = ref<any[]>([])
const chartData = ref<{label: string, tooltipLabel?: string, dateStart: string, value: number, percentage: number}[]>([])
const chartReady = ref(false)

const linePath = computed(() => {
   if (!chartReady.value || chartData.value.length === 0) return '';
   let path = '';
   for (let i = 0; i < chartData.value.length; i++) {
     const day = chartData.value[i]; 
     const x = ((i + 0.5) / chartData.value.length) * 100;
     const y = 100 - Math.max(day.percentage, 1);
     
     if (i === 0) {
       path += `M ${x.toFixed(2)} ${y.toFixed(2)} `;
     } else {
       const prevX = ((i - 0.5) / chartData.value.length) * 100;
       const prevY = 100 - Math.max(chartData.value[i-1].percentage, 1);
       const dx = x - prevX;
       
       const cp1x = prevX + dx / 2;
       const cp1y = prevY;
       
       const cp2x = x - dx / 2;
       const cp2y = y;
       
       path += `C ${cp1x.toFixed(2)} ${cp1y.toFixed(2)}, ${cp2x.toFixed(2)} ${cp2y.toFixed(2)}, ${x.toFixed(2)} ${y.toFixed(2)} `;
     }
   }
   return path;
})

const areaPath = computed(() => {
   if (!chartReady.value || chartData.value.length === 0) return '';
   let lPath = linePath.value;
   const firstX = (0.5 / chartData.value.length) * 100;
   const lastX = ((chartData.value.length - 0.5) / chartData.value.length) * 100;
   lPath += `L ${lastX.toFixed(2)} 100 L ${firstX.toFixed(2)} 100 Z`;
   return lPath;
})

const formatCurrency = (val: number) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val)
}

const formatShortCurrency = (val: number) => {
  if (val >= 1000000) return (val / 1000000).toFixed(1).replace(/\.0$/, '') + 'Jt'
  if (val >= 1000) return (val / 1000).toFixed(0) + 'K'
  return val.toString()
}

const applyFilter = () => {
  chartReady.value = false
  
  if (!startDate.value || !endDate.value) return

  let start = new Date(startDate.value)
  start.setHours(0,0,0,0)
  let end = new Date(endDate.value)
  end.setHours(23,59,59,999)

  if (start > end) {
    const temp = start
    start = end
    end = temp
    startDate.value = start.toISOString().split('T')[0]
    endDate.value = end.toISOString().split('T')[0]
  }

  // Filter transactions
  const filtered = allRentals.value.filter((r) => {
    const d = new Date(r.created_at || r.start_date)
    return d >= start && d <= end
  })
  
  // Choose grouping strategy: if diff is > 65 days, group by month
  const diffDays = Math.ceil((end.getTime() - start.getTime()) / (1000 * 3600 * 24))
  if (diffDays > 65) {
    generateChartDataMonths(filtered, start, end)
  } else {
    generateChartDataDays(filtered, start, end)
  }
  
  // Calculate Totals exactly for filtered scope
  let income = 0
  const counts: Record<string, number> = {}
  filtered.forEach((r: any) => {
    if (r.status !== 'dibatalkan' && r.status !== 'menunggu_bayar') {
      income += (r.grand_total || 0)
    }
    counts[r.status] = (counts[r.status] || 0) + 1
  })
  
  totalIncome.value = income
  totalRentals.value = filtered.length
  statusCounts.value = counts
}

const generateChartDataDays = (rows: any[], start: Date, end: Date) => {
  const dataMap: Record<string, number> = {}
  
  let curr = new Date(start)
  while (curr <= end) {
    const yyyy = curr.getFullYear()
    const mm = String(curr.getMonth() + 1).padStart(2, '0')
    const dd = String(curr.getDate()).padStart(2, '0')
    dataMap[`${yyyy}-${mm}-${dd}`] = 0
    curr.setDate(curr.getDate() + 1)
  }

  rows.forEach((r: any) => {
    if (r.status !== 'dibatalkan' && r.status !== 'menunggu_bayar') {
      const dbDate = new Date(r.created_at || r.start_date)
      const dKey = `${dbDate.getFullYear()}-${String(dbDate.getMonth() + 1).padStart(2, '0')}-${String(dbDate.getDate()).padStart(2, '0')}`
      if (dataMap[dKey] !== undefined) {
        dataMap[dKey] += (r.grand_total || 0)
      }
    }
  })

  let maxVal = Math.max(...Object.values(dataMap))
  if (maxVal === 0) maxVal = 1
  
  const formatterDisplay = new Intl.DateTimeFormat('id-ID', { weekday: 'short' })
  const dateFmt = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short' })
  const totalDays = Object.keys(dataMap).length
  
  chartData.value = Object.keys(dataMap).map(dateStr => {
    const [y, m, d] = dateStr.split('-')
    const dateObj = new Date(Number(y), Number(m)-1, Number(d))
    return {
      label: totalDays <= 14 ? formatterDisplay.format(dateObj) : dateFmt.format(dateObj).split(' ')[0],
      tooltipLabel: `${formatterDisplay.format(dateObj)}, ${dateFmt.format(dateObj)}`,
      dateStart: dateStr,
      value: dataMap[dateStr],
      percentage: (dataMap[dateStr] / maxVal) * 100
    }
  })

  setTimeout(() => { chartReady.value = true }, 50)
}

const generateChartDataMonths = (rows: any[], start: Date, end: Date) => {
  const dataMap: Record<string, number> = {}
  
  let curr = new Date(start.getFullYear(), start.getMonth(), 1)
  const endMonth = new Date(end.getFullYear(), end.getMonth(), 1)
  
  while (curr <= endMonth) {
    const yyyy = curr.getFullYear()
    const mm = String(curr.getMonth() + 1).padStart(2, '0')
    dataMap[`${yyyy}-${mm}`] = 0
    curr.setMonth(curr.getMonth() + 1)
  }

  rows.forEach((r: any) => {
    if (r.status !== 'dibatalkan' && r.status !== 'menunggu_bayar') {
      const dbDate = new Date(r.created_at || r.start_date)
      const dKey = `${dbDate.getFullYear()}-${String(dbDate.getMonth() + 1).padStart(2, '0')}`
      if (dataMap[dKey] !== undefined) {
        dataMap[dKey] += (r.grand_total || 0)
      }
    }
  })

  let maxVal = Math.max(...Object.values(dataMap))
  if (maxVal === 0) maxVal = 1
  
  const formatter = new Intl.DateTimeFormat('id-ID', { month: 'short' })
  chartData.value = Object.keys(dataMap).map(dateStr => {
    const [y, m] = dateStr.split('-')
    const dateObj = new Date(Number(y), Number(m)-1, 1)
    return {
      label: formatter.format(dateObj),
      tooltipLabel: `${formatter.format(dateObj)} ${y}`,
      dateStart: dateStr,
      value: dataMap[dateStr],
      percentage: (dataMap[dateStr] / maxVal) * 100
    }
  })

  setTimeout(() => { chartReady.value = true }, 50)
}

const getHexColor = (status: string) => {
  switch (status) {
    case 'menunggu_bayar': return '#f2c037' // warning
    case 'menunggu_verif': return '#f57c00' // orange-8
    case 'diproses': return '#31ccec' // info
    case 'aktif': return '#1976d2' // primary
    case 'selesai': return '#21ba45' // positive
    case 'dibatalkan': return '#c10015' // negative
    default: return '#9e9e9e' // grey
  }
}

const donutStyle = computed(() => {
  if (totalRentals.value === 0) return 'background: #e2e8f0;'
  let gradientStr = `conic-gradient(`
  let currentPercentage = 0
  
  const entries = Object.entries(statusCounts.value)
  for (let i = 0; i < entries.length; i++) {
    const [status, count] = entries[i]
    if (count === 0) continue
    const perc = (count / totalRentals.value) * 100
    const color = getHexColor(status)
    gradientStr += `${color} ${currentPercentage}%, ${color} ${currentPercentage + perc}%, `
    currentPercentage += perc
  }
  
  if (currentPercentage < 100) {
    gradientStr += `#e2e8f0 ${currentPercentage}%, #e2e8f0 100%, `
  }
  
  gradientStr = gradientStr.replace(/, $/, ')')
  return `background: ${gradientStr};`
})

const getStatusColor = (status: string) => {
  switch (status) {
    case 'menunggu_bayar': return 'warning'
    case 'menunggu_verif': return 'orange-8'
    case 'diproses': return 'info'
    case 'aktif': return 'primary'
    case 'selesai': return 'positive'
    case 'dibatalkan': return 'negative'
    default: return 'grey'
  }
}

const loadData = () => {
  // Load Rentals
  API.get('transaction/rentals?limit=1000', (status: number, data: any) => {
    if (status === 200) {
      const rows = data?.data ?? data
      if (Array.isArray(rows)) {
        allRentals.value = rows
        
        applyFilter()

        // Setup recent rentals (sort descending by created_at, take 10)
        recentRentals.value = rows
          .sort((a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime())
          .slice(0, 10)
      }
    }
  }, 'rental')

  // Load Customers
  API.get('auth/users?limit=0', (status: number, data: any) => {
    if (status === 200) {
      const rows = data?.data ?? data
      if (Array.isArray(rows)) {
        totalCustomers.value = rows.length
      }
    }
  }, 'identity')

  // Load Items
  API.get('master/items?limit=0', (status: number, data: any) => {
    if (status === 200) {
      const rows = data?.data ?? data
      if (Array.isArray(rows)) {
        totalItems.value = rows.length
      }
    }
  }, 'rental')
}

const viewRental = (rental: any) => {
  router.push({ name: 'view-transaction/rentals', params: { id: rental.id } })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.opacity-80 {
  opacity: 0.8;
}
.tracking-wide {
  letter-spacing: 0.5px;
}
.card-hover {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
.transition-item {
  transition: background-color 0.2s ease;
  border-radius: 8px;
}
.transition-item:hover {
  background-color: #f8f9fa;
}
.bar-gradient {
  background: linear-gradient(180deg, var(--q-primary) 0%, rgba(25,118,210,0.5) 100%);
  box-shadow: 0 4px 12px rgba(25,118,210,0.25);
  border-radius: 8px 8px 4px 4px;
}
.bar-hover:hover {
  filter: brightness(1.15);
  cursor: pointer;
  transform: scaleY(1.02) scaleX(1.05);
  box-shadow: 0 8px 16px rgba(25,118,210,0.4);
}
.donut-chart {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  position: relative;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.donut-chart:hover {
  transform: scale(1.05);
}
.donut-inner {
  position: absolute;
  top: 15%; left: 15%; right: 15%; bottom: 15%;
  background: white;
  border-radius: 50%;
  box-shadow: inset 0px 4px 10px rgba(0,0,0,0.06);
}

.hover-column {
  cursor: pointer;
}
.hover-column:hover .bubble-val {
  opacity: 1 !important;
  transform: translateY(0) !important;
}
.hover-column:hover .hover-bar {
  background-color: rgba(25, 118, 210, 0.04);
  border-radius: 8px;
}
.animated-line {
  stroke-dasharray: 2000;
  stroke-dashoffset: 2000;
  animation: drawLine 1.5s ease-out forwards;
}
@keyframes drawLine {
  to {
    stroke-dashoffset: 0;
  }
}
</style>

