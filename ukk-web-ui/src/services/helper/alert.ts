import { Dialog, Notify, Loading, LoadingBar, BottomSheet } from 'quasar'

type Position = 'top' | 'right' | 'bottom' | 'left' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center' | undefined

export default {
  loadingOverlay(show = true, msg = '') {
    // const spinner = typeof QSpinnerIos !== 'undefined' ? QSpinnerIos : Quasar.components.QSpinnerIos
    Loading.show({
      // spinner,
      // spinnerColor: 'white',
      // spinnerSize: 140,
      // backgroundColor: 'primary',
      message: msg
      // messageColor: 'white'
    })
    if (show === false) {
      setTimeout(() => {
        Loading.hide()
      }, 300)
    }
  },
  loading(show = true) {
    LoadingBar.setDefaults({
      color: 'red',
      size: '3px',
      position: 'top'
    })
    if (show === false) {
      setTimeout(() => {
        LoadingBar.stop()
      }, 300)
    } else LoadingBar.start()
  },
  showToast(msg: string, color = 'dark', timeout = 5000, position: Position = 'bottom', caption = '') {
    Notify.create({
      progress: true,
      message: msg,
      position: position,
      icon: 'info',
      color: color,
      timeout: timeout,
      caption: caption,
      actions: [
        {
          label: 'x',
          color: 'yellow',
          handler: () => {
            /* console.log('wooow') */
          }
        }
      ]
    })
  },
  showSuccess(title: string, msg = '') {
    Notify.create({
      type: 'positive',
      message: title,
      caption: msg,
      position: 'top-right',
      timeout: 5000,
      actions: [
        {
          label: 'x',
          color: 'white',
          handler: () => {
            /* console.log('wooow') */
          }
        }
      ]
    })
  },
  showNotif(title: string, msg = '', type = 'negative') {
    Notify.create({
      type: type,
      message: title,
      caption: msg,
      position: 'center',
      timeout: 5000,
      actions: [
        {
          label: 'x',
          color: 'yellow',
          handler: () => {
            /* console.log('wooow') */
          }
        }
      ]
    })
  },
  showAlert(title: string, msg = '', persistent = false) {
    let judul = title
    let pesan = msg
    if (title === 'try') {
      judul = 'Opps!'
      pesan = 'Terjadi kesalahan saat menghubungkan ke server, harap coba lagi atau tekan Refresh!'
    }
    Dialog.create({
      transitionShow: 'jump-up',
      transitionHide: 'jump-down',
      title: judul,
      message: pesan,
      html: true,
      persistent: persistent
    })
      .onOk(() => {
        // console.log('OK')
      })
      .onCancel(() => {
        // console.log('Cancel')
      })
      .onDismiss(() => {
        // console.log('I am triggered on both OK and Cancel')
      })
  },
  showError(e: string, json: JSON) {
    let err = e
    if (json) err = JSON.stringify(e)
    this.showAlert('ERROR', err)
  },
  showBottomSheet(message = '', actions = [], callback: any) {
    BottomSheet.create({
      message: message,
      actions: actions
    })
      .onOk((action) => {
        callback(action.id)
      })
      .onCancel(() => {
        // console.log('Dismissed')
      })
      .onDismiss(() => {
        // console.log('I am triggered on both OK and Cancel')
      })
  },
  confirm(message: string, callback: any, options: any = undefined, prompt: any = undefined) {
    Dialog.create({
      transitionShow: 'jump-up',
      transitionHide: 'jump-down',
      title: 'Confirm',
      message: message,
      html: true,
      cancel: true,
      options: options,
      prompt: prompt
    })
      .onOk((data) => {
        callback(true, data)
      })
      .onCancel(() => {
        callback(false)
        // console.log('Cancel clicked');
      })
      .onDismiss(() => {
        // console.log('Dialog dismissed');
      })
  }
}
