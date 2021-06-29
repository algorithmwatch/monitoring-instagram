import { dispatch, getState } from './store'
import { LOCAL_STATE_SET_PROJECT } from '../constantes'
import browser from 'webextension-polyfill'

async function detectProject() {
  if (getState().project === undefined) {
    const projects = await fetch(
      `${process.env.BACKEND_URL}/api/v2/project/?active=true`
    )
      .then(req => req.text())
      .then(JSON.parse)
    let userLocale = browser.i18n.getUILanguage()
    let projectId
    // look at projects default locales and check if the user locale matches
    for (let index = 0; index < projects.length; index++) {
      const project = projects[index]
      if (project.default_for_locale) {
        let projectLocales = project.default_for_locale.split(',')
        for (let index = 0; index < projectLocales.length; index++) {
          const projectLocale = projectLocales[index]
          if (userLocale.indexOf(projectLocale) > -1) {
            projectId = project.id
            break
          }
        }
      }
      if (projectId !== undefined) {
        break
      }
    }
    // default project is the first one
    projectId = projectId === undefined ? projects[0].id : projectId
    dispatch({
      type: LOCAL_STATE_SET_PROJECT,
      payload: projectId,
    })
  }
}
export default detectProject
