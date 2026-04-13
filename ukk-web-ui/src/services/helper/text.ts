import { format } from 'quasar'

export default {
  findString(string: string, keyword: string) {
    const result = string.search(keyword)
    let res = false
    if (result < 0) res = false
    else res = true
    return res
  },
  replace(target: string, replace: string, str: string) {
    const string = '' + str
    const regex = new RegExp(target, 'g')
    return string.replace(regex, replace)
  },
  delStr(str: string, fromRight = 1) {
    return str.substr(0, str.length - fromRight)
  },
  capitalize(string: string) {
    return format.capitalize(string)
  },
  formatCamelCase(text: string, withS = true) {
    let res = text.replace(/[A-Z]/g, (str) => `-${str.toLowerCase()}`)
    res = `${res.substring(1)}${withS ? 's' : ''}`
    return res
  },
  base64(str: string, type: string) {
    if (type === 'enc') return btoa(str)
    else return atob(str)
  },
  getFirstChar(str: string) {
    return str.charAt(0)
  },
  // new
  arrToStr(arr: any) {
    let str = ''
    for (let i = 0; i < arr.length; i++) {
      const element = arr[i]
      str += element + ','
    }
    str = this.delStr(str)
    return str
  },
  acronym(phrase: string | null): string {
    if (!phrase) return ''

    return phrase
      .replace(/[^a-zA-Z\s]/g, '') // Remove non-alphabet characters except spaces
      .split(/\s+/) // Split by spaces
      .map((word) => word[0]?.toUpperCase() || '') // Get first letter and capitalize
      .join('') // Join letters together
  },
  strArr2ValLabel(strArr: string[]): any[] {
    const options: any[] = []
    for (let i = 0; i < strArr.length; i++) {
      const e = strArr[i]
      options.push({ value: e, label: e })
    }
    return options
  },
  slug2label(slug: string) {
    let clean = slug.replace(/[-_]/g, ' ')
    clean = clean.replace(/([a-z])([A-Z])/g, '$1 $2')
    return clean
      .toLowerCase()
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  },
  label2slug(label: string, separator: string = '_'): string {
    return label
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .trim()
      .replace(/\s+/g, separator)
  },
  truncateText(text: string, maxLength: number = 50): string {
    if (!text) return ''
    return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
  },
  gen_ref_id(company_code: string, year: string, month: string) {
    return `${company_code}-${year}-${month}`
  },
  schema2label(str: any) {
    return str
      .split('.') // pisah berdasarkan titik
      .map(
        (part: any) =>
          part
            .replace(/_/g, ' ') // ganti _ jadi spasi
            .replace(/\b\w/g, (c) => c.toUpperCase()) // kapital tiap kata
      )
      .join(' > ') // gabung pakai " > "
  }
}
