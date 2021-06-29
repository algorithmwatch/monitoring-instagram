import { MESSAGE_IS_LOGGED } from '../../constantes'
import sendMsg from './sendMsg'
import injectScript from './injectScript'

export default async function checkLogin() {
  let { isLoggedIn, igUsername, userData } = await injectScript(
    '/dist/resource-retreive-ig-user-data.js'
  )
  sendMsg(MESSAGE_IS_LOGGED, { isLoggedIn, igUsername })
  return { isLoggedIn, igUsername, userData }
}
