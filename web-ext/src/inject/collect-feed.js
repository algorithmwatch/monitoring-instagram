import { MESSAGE_COLLECTED_DATA } from '../constantes'
import checkLogin from './utils/checkLogin'
import sendMsg from './utils/sendMsg'

async function init() {
  // checks and notify bg if logged in
  const { isLoggedIn, userData } = await checkLogin()
  // if logged in, collect data
  if (isLoggedIn) {
    return sendMsg(MESSAGE_COLLECTED_DATA, userData)
  }
}

init()

export default 'ok'
