import browser from 'webextension-polyfill'
export default function registerOnInstalledhandler() {
  browser.runtime.onInstalled.addListener(({ reason, temporary }) => {
    if (temporary) return // skip during development
    switch (reason) {
      case 'install':
        {
          setTimeout(() => {
            const url = browser.runtime.getURL('./dashboard/main.html')
            browser.tabs.create({ url })
          }, 1000)
        }
        break
    }
  })
}
