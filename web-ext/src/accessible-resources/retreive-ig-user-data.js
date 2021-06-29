import { postMessage } from './common'

const additionalData = window.__additionalData
const isLoggedIn = !!additionalData.feed
let igUsername, userData
if (isLoggedIn) {
  igUsername = additionalData.feed.data.user.username
  userData = additionalData.feed.data.user
}
postMessage({ igUsername, isLoggedIn, userData })
