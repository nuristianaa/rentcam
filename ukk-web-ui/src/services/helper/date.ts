import { date } from 'quasar'

export default {
  currentmillis(): number {
    return new Date().getTime()
  },
  date2millis(dateTime: string, local = false): number {
    try {
      const time = new Date(dateTime).getTime()
      const tzOffset = local ? new Date().getTimezoneOffset() * 60000 : 0
      return time + tzOffset
    } catch (error) {
      console.error("Invalid date format for 'date2millis'", error)
      return 0
    }
  },
  today(format = 'YYYY-MM-DD'): string {
    return this.toDate(new Date(), format)
  },
  endOfMonth(date, format = 'YYYY-MM-DD'): string {
    if (date){
      const now = new Date(date)
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0)
      return this.toDate(lastDay, format)
    } else {
      const now = new Date()
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0)
      return this.toDate(lastDay, format)
    }
    
  },
  now(days = 0, format = 'YYYY-MM-DD HH:mm:ss'): string {
    const date = new Date()
    if (days !== 0) {
      date.setDate(date.getDate() + days)
    }
    return this.toDate(date, format)
  },
  utcTime(): string {
    const now = new Date()
    const utcHours = now.getUTCHours().toString().padStart(2, '0')
    const utcMinutes = now.getUTCMinutes().toString().padStart(2, '0')
    const utcSeconds = now.getUTCSeconds().toString().padStart(2, '0')
    return `${utcHours}:${utcMinutes}:${utcSeconds}`
  },
  readDate(date: string | Date | number, includeTime = false): string {
    return includeTime ? this.toDate(date, 'DD-MMM-YY HH:mm') : this.toDate(date, 'DD-MMM-YY')
  },
  readRangeDate(start: string | Date | number, end: string | Date | number) {
    const fr = this.toDate(start, 'MMM YY')
    const to = this.toDate(end, 'MMM YY')
    if (fr == to) {
      return (this.toDate(start, 'DD') ?? '') + ' - ' + (this.toDate(end, 'DD MMM YY') ?? '')
    } else {
      return (this.toDate(start, 'DD MMM') ?? '') + ' - ' + (this.toDate(end, 'DD MMM YY') ?? '')
    }
  },
  toDate(dateInput: string | Date | number, format = 'YYYY-MM-DD'): string {
    try {
      return date.formatDate(dateInput, format)
    } catch (error) {
      console.error("Invalid date input for 'toDate'", error)
      return ''
    }
  },
  addDate(dateInput: string | Date | number, days: number, isMidNight: boolean = false, format: string = 'YYYY-MM-DD'): string {
    const date = new Date(dateInput)
    date.setDate(date.getDate() + days)
    if (isMidNight) {
      date.setHours(0, 0, 0, 0) // Set to midnight
      return this.toDate(date, format)
    }
    return this.toDate(date, format)
  },
  subDate(dateInput: string | Date | number, days: number): string {
    const date = new Date(dateInput)
    date.setDate(date.getDate() - days)
    return this.toDate(date)
  },
  ym2date(yearMonth: string): string {
    try {
      const months = ['', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
      const [monthStr, year] = yearMonth.split(' ')
      if (monthStr) {
        const monthIndex = months.indexOf(monthStr.toLowerCase())
        if (monthIndex <= 0 || !year) return ''
        const month = monthIndex < 10 ? `0${monthIndex}` : `${monthIndex}`
        return `${year}-${month}-01`
      }
      return ''
    } catch (error) {
      console.error("Invalid input for 'ym2date'", error)
      return ''
    }
  },
  millis2textdhm(ms: number): string {
    const days = Math.floor(ms / (24 * 60 * 60 * 1000))
    const hours = Math.floor((ms % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000))
    const minutes = Math.floor((ms % (60 * 60 * 1000)) / (60 * 1000))
    return `${days} Days : ${hours} Hours : ${minutes} Minutes`
  },
  millis2textHm(ms: number | string): string {
    const date = new Date(ms)
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },
  millis2Date(millis: number, format: string = 'yyyy-MM-dd'): string {
    const date = new Date(millis)

    // Manual formatting (basic)
    const yyyy = date.getFullYear()
    const mm = String(date.getMonth() + 1).padStart(2, '0') // Months are zero-based
    const dd = String(date.getDate()).padStart(2, '0')

    if (format === 'yyyy-MM-dd') return `${yyyy}-${mm}-${dd}`
    if (format === 'dd-MM-yyyy') return `${dd}-${mm}-${yyyy}`
    if (format === 'dd-MMM-yy') {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      return `${dd}-${months[date.getMonth()]}-${String(yyyy).slice(-2)}`
    }

    // Default fallback
    return date.toISOString()
  },
  diffInDay(startDate: string | Date | number, endDate: string | Date | number): number {
    const diffMs = new Date(endDate).getTime() - new Date(startDate).getTime()
    return diffMs / (1000 * 60 * 60 * 24)
  },
  sessionTimer(t: number) {
    // let t = endDate - this.currentMillis()
    const times = [
      { id: 0, text: 'Days', time: 1 },
      { id: 1, text: 'Hours', time: 1 },
      { id: 2, text: 'Minutes', time: 1 },
      { id: 3, text: 'Seconds', time: 1 }
    ]
    if (t >= 0) {
      if (times[3]) times[3].time = Math.floor((t / 1000) % 60) // seconds
      if (times[2]) times[2].time = Math.floor((t / 1000 / 60) % 60) // minutes
      if (times[1]) times[1].time = Math.floor((t / (1000 * 60 * 60)) % 24) // hours
      if (times[0]) times[0].time = Math.floor(t / (1000 * 60 * 60 * 24)) // days
    } else {
      if (times[3] && times[2] && times[1] && times[0]) times[3].time = times[2].time = times[1].time = times[0].time = 0
    }
    return times
  },
  readTimeLogs(timestamp: number | null): string {
    if (timestamp) {
      const now = new Date()
      const date = new Date(timestamp)
      const diffMs = now.getTime() - date.getTime() // Difference in milliseconds
      const diffSec = Math.floor(diffMs / 1000)
      const diffMin = Math.floor(diffSec / 60)
      const diffHours = Math.floor(diffMin / 60)
      const diffDays = Math.floor(diffHours / 24)

      const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }
      const fullOptions: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' }

      if (diffMs < 0) {
        return 'In the future' // Handle future timestamps
      }

      if (diffHours < 24) {
        const hours = date.getHours().toString().padStart(2, '0') // Adds leading zero if necessary
        const minutes = date.getMinutes().toString().padStart(2, '0') // Adds leading zero if necessary
        return `${hours}:${minutes}`
      }

      if (diffDays < 7) {
        // If within the past week
        const weekday = date.toLocaleDateString('en-US', { weekday: 'long' })
        return diffDays === 1 ? 'Yesterday' : `Last ${weekday}`
      }

      if (diffDays < 30) {
        // If within the past month, show "January 31"
        return date.toLocaleDateString('en-US', options)
      }

      // Otherwise, show full date like "January 31, 2025"
      return date.toLocaleDateString('en-US', fullOptions)
    }
    return ''
  },
  getWeekNumber(date: any = null) {
    if (!date) return null
    const dt = new Date(date)

    const dayOfWeek: any = (dt.getDay() + 6) % 7 // make Monday = 0
    const nearestThursday: any = new Date(dt)
    nearestThursday.setDate(dt.getDate() - dayOfWeek + 3)

    const firstDayOfYear: any = new Date(nearestThursday.getFullYear(), 0, 1)
    const diffInDays = Math.round((nearestThursday - firstDayOfYear) / 86400000)

    return Math.floor(diffInDays / 7) + 1
  },
  addMinute(dateStr: string, minutes: number) {
    const date = new Date(dateStr.replace(' ', 'T'))

    if (isNaN(date.getTime())) {
      throw new Error('Invalid date format')
    }

    date.setMinutes(date.getMinutes() + minutes)

    // Return as formatted string (e.g. "2025-07-17 15:30")
    const pad = (n: number) => n.toString().padStart(2, '0')
    const formatted = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`

    return formatted
  },
  convertToDHM(minutes: number) {
    const days = Math.floor(minutes / (24 * 60))
    const hours = Math.floor((minutes % (24 * 60)) / 60)
    const mins = minutes % 60

    const parts = []
    if (days > 0) parts.push(`${days} Days`)
    if (hours > 0) parts.push(`${hours} Hours`)
    if (mins > 0 || parts.length === 0) parts.push(`${mins} Minutes`)

    return parts.join(' ')
  },
  rangeDateTime(start: string, end: string, raw = false, toMinute = true): string | number {
    const timeStart = new Date(start).getTime()
    const timeEnd = new Date(end).getTime()

    if (isNaN(timeStart) || isNaN(timeEnd)) {
      throw new Error('Invalid date format')
    }

    const diffMs = timeEnd - timeStart
    const isNegative = diffMs < 0
    const absDiffMs = Math.abs(diffMs)
    const diffMinutes = Math.round(absDiffMs / 60000)

    if (raw) {
      return isNegative ? -diffMinutes : diffMinutes
    }

    if (toMinute) {
      return isNegative ? `-${diffMinutes}M` : `${diffMinutes}M`
    }

    const dhm = this.convertToDHM(diffMinutes)
    return isNegative ? `-${dhm}` : dhm
  },
  minuteToDhm(minute: any) {
    const ms = Math.abs(parseInt(minute ?? 0))
    if (ms != 0) {
      let days: any = Math.floor(ms / (24 * 60))
      const daysms = ms % (24 * 60)
      let hours: any = Math.floor(daysms / 60)
      const hoursms = ms % 60
      let minutes: any = Math.floor(hoursms)
      if (days < 10) days = '0' + days
      if (hours < 10) hours = '0' + hours
      if (minutes < 10) minutes = '0' + minutes
      return `${minute < 0 ? '-' : ''}${days}:${hours}:${minutes}`
    } else return '00:00:00'
  },
  getMonthName(month: number) {
    let result: string | undefined = ''
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if (month !== null) result = months[month]
    return result
  },
  extractRangeDate(val: any, selector: any = null) {
    if (!val) return null

    // pisahkan jika ada " to "
    const parts = val.split(' to ').map((s) => s.trim())
    const start = parts[0]
    const end = parts[1] || parts[0] // kalau single date, end = start

    const result: any = { start, end }

    if (selector) return result[selector] || null
    return result
  }
}
