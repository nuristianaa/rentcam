import { readFile, writeFileSync } from 'fs'

// UPDATE VERSION
const linkfile = './src/services/config/version.ts'
readFile(linkfile, 'utf8', (err, data) => {
  if (err) {
    console.error(err)
    return
  }
  const a = data.split("ver = '")[1]
  const b = a.split("'")[0]
  const parent = parseInt(b.split('.')[1])
  const child = parseInt(b.split('.')[2])
  let version = ''
  if (child > 90) {
    version = `0.${parent + 1}.${1}`
  } else {
    version = `0.${parent}.${child + 1}`
  }
  console.log(version)
  // Date
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const d = new Date()
  const year = d.getFullYear()
  const month = months[d.getMonth()]
  const day = d.getDate() < 10 ? '0' + d.getDate() : d.getDate()
  const date = `${day}-${month}-${year}`
  const content = `
export default {
  version() {
    const ver = '${version}'
    const verdate = '${date}'
    return ver + ' - ' + verdate
  }
}
`
  try {
    writeFileSync(linkfile, content)
    console.error(content)
  } catch (err) {
    console.error(err)
  }
})