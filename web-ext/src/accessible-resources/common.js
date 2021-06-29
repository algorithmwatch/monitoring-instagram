import { IMPLANTED_SCRIPT_RESULT_MESSAGE } from '../constantes'

export const postMessage = payload =>
  window.postMessage({ message: IMPLANTED_SCRIPT_RESULT_MESSAGE, payload }, '*')
