import { getState, dispatch } from './store'
import { LOCAL_STATE_SET_PROJECT_STATUS } from '../constantes'

export default async function checkProjectStatus() {
  if (getState().project && getState().isAllowedToRun) {
    await fetch(
      `${process.env.BACKEND_URL}/api/v2/project/${getState().project}/`
    )
      .then(req => req.text())
      .then(JSON.parse)
      .then(project => {
        dispatch({
          type: LOCAL_STATE_SET_PROJECT_STATUS,
          payload: project.active,
        })
      })
  }
  setTimeout(checkProjectStatus, 1000 * 60 * 60 * 3)
}
