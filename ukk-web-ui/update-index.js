import { readFile, writeFileSync } from 'fs'

const version = Date.now()
const distPath = './dist/pwa/index.html'

readFile(distPath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading index.html:', err)
    return
  }

  // Append ?v=Date.now() to all .js and .css files
  data = data.replace(/(href)=(.*?\.(css))/g, `$1=$2?v=${version}`)
  data = data.replace(/(src)=(.*?\.(js))/g, `$1=$2?v=${version}`)
  try {
    writeFileSync(distPath, data)
    // console.error(updatedHtml)
  } catch (err) {
    console.error(err)
  }
})
