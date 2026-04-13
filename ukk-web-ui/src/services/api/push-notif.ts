import { authStore } from 'src/stores/auth'
import { Config } from 'src/services/config'

export async function subscribePush(username: string, user_id: number, force: boolean = true) {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    try {
      const permission = await Notification.requestPermission()

      if (permission !== 'granted') {
        console.warn('Push permission denied')
        if (force) return
      }

      // ❗ WAJIB: Tunggu sampai SW aktif
      const registration = await navigator.serviceWorker.ready
      if (!registration) {
        console.error('Service Worker registration not found')
        return
      }

      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: 'BK0h2ORJ4ycyBSI2nbsy2KcszjLS6weoI-Db6YcDpfC0OBwkOnis1uk6gSkCW3qV2WHhKS638LhRPkqsbf3uLYM'
      })

      const token = authStore().getToken()
      const url = Config.getApiRoot('main') + 'auth/notifications/subscribe'
      const payload = {
        username,
        user_id,
        subscription
      }

      await fetch(url, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      console.log('Push subscription registered.')
    } catch (err) {
      console.error('Error subscribing to push', err)
    }
  }
}
