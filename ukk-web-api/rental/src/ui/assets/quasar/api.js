const token = localStorage.getItem('token')
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
}
const hostname = window.location.hostname
let apiroot = ''
if(hostname === 'localhost') apiroot = 'http://127.0.0.1:8090'

const _api = {
  // HELPERS
  showSuccess: (message = 'Data saved!', timer=3000) => {
    const Toast = Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: timer,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
      }
    })
    Toast.fire({
      icon: "success",
      title: message
    })
  },
  showNotif: (message = 'New Customer!', timer=3000) => {
    const Toast = Swal.mixin({
      toast: true,
      position: "bottom",
      showConfirmButton: false,
      timer: timer,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
      }
    })
    Toast.fire({
      icon: "info",
      title: message
    })
  },
  showError: (message, timer = 10000) => {
    console.log(message)
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: message ?? '',
      showConfirmButton: true,
      timer,
      timerProgressBar: true,
    })
  },
  // API
  req: async (protocol, path, reqbody, callback) => {
    let request = {
      method: protocol,
      headers: headers,
    }
    if (reqbody) request.body = JSON.stringify(reqbody)
    const response = await fetch(path, request)
    const result = await response.json()
    const message = result?.message ?? result?.detail ?? 'success'
    if (response.status != 200) _api.showError(message)
    callback(response.status, result, message, response)
  },
  get: (path, callback) => {
    return _api.req('GET', path, null, callback)
  },
  post: (path, reqbody, callback) => {
    return _api.req('POST', path, reqbody, callback)
  },
  put: (path, reqbody, callback) => {
    return _api.req('PUT', path, reqbody, callback)
  },
  delete: (path, reqbody, callback) => {
    return _api.req('DELETE', path, reqbody, callback)
  },
}