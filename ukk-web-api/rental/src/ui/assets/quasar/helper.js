const _globalHelper = {
  formatNumber (num, precision = null) {
    return num ? num.toFixed(precision).replace(/\B(?=(\d{3})+(?!\d))/g, ",") : num
  },
  formatMoney (value, currency = null) {
    let prec = 0
    if(!currency) prec = Constant.moneyPrecision
    else {
      if (currency == 'IDR') prec = 0
      else prec = Constant.moneyPrecision
    }
    const val = parseFloat(value).toFixed(prec).replace(',', '.')
    const formatted = val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    if (formatted === 'NaN') return null
    else return formatted
  },
  formatDate(tanggal, format = 'YYYY-MM-DD') {
    const strMonth = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if (!tanggal) return null
    let arr = tanggal.split('-')
    let year = '20' + arr[2]
    let monthInt = strMonth.indexOf(arr[1])
    let month = monthInt > 9 ? monthInt : '0' + monthInt
    let day = arr[0]
    let tgl = year + '-' + month + '-' + day
    return this.formatDate(tgl, format)
  },
  formatTimestamp(timestamp, format) {
    try {
      const date = new Date(timestamp)
      const options = {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }
      const dateParts = {
        DD: String(date.getDate()).padStart(2, '0'),
        MMM: date.toLocaleString('en-US', { month: 'short' }),
        YYYY: date.getFullYear(),
        H: String(date.getHours()).padStart(2, '0'),
        i: String(date.getMinutes()).padStart(2, '0'),
        s: String(date.getSeconds()).padStart(2, '0')
      }
      return format.replace(/DD|MMM|YYYY|H|i|s/g, match => dateParts[match])
    } catch {
      return timestamp
    }
  },
  toDate(_date, format = 'YYYY-MM-DD', ina = false) {
    if (ina) return `${this.toDate(_date, 'DD')}-${this.months(this.toDate(_date, 'M'))}-${this.toDate(_date, 'YYYY')}`
    return this.formatDate(_date, format)
  },
  readDate(timestamp, time = false) {
    const date = new Date(timestamp);
    let opt = {
      day: '2-digit',
      month: 'short',
      year: '2-digit',
      hour: false,
      minute: false,
      hour12: false
    }
    if (time) {
      opt.hour = '2-digit'
      opt.minute = '2-digit'
      opt.hour12 = false
    }
    return date.toLocaleString('en-GB', opt).replace(',', '').replaceAll('at', '');
  },
  readTimestamp (value, datetime = false) {
    let result = this.formatTimestamp(value, 'DD MMM YYYY')
    if (datetime) result = this.formatTimestamp(value, 'DD MMM YYYY - H:i')
    // return `${value} ${result}`
    return result
  },
  toHoursAndMinutes(totalMinutes = 0, type = 'minutes', separator = ':') {
    if (type == 'ms') {
      totalMinutes = totalMinutes / 60000
      if(totalMinutes > 1440) return '23:59:59'
    }
    const hours = Math.floor(totalMinutes / 60)
      .toString()
      .padStart(2, '0')
    const minutes = parseInt(totalMinutes % 60)
      .toString()
      .padStart(2, '0')
    const seconds = parseInt(totalMinutes * 60 % 60)
      .toString()
      .padStart(2, '0')
    return totalMinutes ? `${hours}${separator}${minutes}${separator}${seconds}` : ''
  },
  loadingOverlay: (show = true, text = 'Please Wait ...', icon = 'info') => {
    if (!show) Swal.close()
    Swal.fire({
      text,
      icon,
      allowOutsideClick: false,
      showConfirmButton: false
    })
  },
  showNotif: (title = 'Success', icon = 'success') => {
    Swal.fire({
      title: title,
      icon: icon,
      draggable: true
    })
  }
}