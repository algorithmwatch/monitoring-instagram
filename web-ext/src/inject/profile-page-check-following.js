import sendDispatchMsg from '../utils/sendDispatchMsg'
import injectScript from './utils/injectScript'
import {
  LOCAL_STATE_UPDATE_FOLLOWING,
  INJECT_SCRIPT_END_MESSAGE,
} from '../constantes'
import sendMsg from '../utils/sendMsg'

injectScript('dist/resource-retreive-donor-is-following.js').then(
  ({ isFollowing, igUsername, userData }) => {
    // updates state
    sendDispatchMsg({
      type: LOCAL_STATE_UPDATE_FOLLOWING,
      payload: {
        igUsername,
        isFollowing,
        userData,
      },
    })
    // we're done
    sendMsg(INJECT_SCRIPT_END_MESSAGE)
  }
)

export default 'ok'
