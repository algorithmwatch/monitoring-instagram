import { getState, selectorThereIsReallyAProblem } from './store'
import { runScriptOnce } from './igContentScript'
import checkLoginAndFollowing from './checkLoginAndFollowing'

const randInt = () => Math.ceil(Math.random() * 10)
const secondsInOneHour = () => (randInt() + 50) * (randInt() + 50)
const secondsInOneDay = () => secondsInOneHour() * 24

let collect_timeout_id
let checker_timeout_id

async function startCollectionIfReady() {
  if (collect_timeout_id) {
    clearTimeout(collect_timeout_id)
  }
  const state = getState()
  const hasProblem = selectorThereIsReallyAProblem(state)
  const projectIsActive = state.projectIsActive
  if (projectIsActive) {
    if (!hasProblem) {
      await runScriptOnce()
    } else {
      console.warn('there is a problem...')
    }
  }
  collect_timeout_id = setTimeout(
    startCollectionIfReady,
    1000 * secondsInOneHour()
  )
}

async function startChecker() {
  if (checker_timeout_id) {
    clearTimeout(checker_timeout_id)
  }
  if (getState().projectIsActive) {
    await checkLoginAndFollowing()
  }
  checker_timeout_id = setTimeout(startChecker, 1000 * secondsInOneDay())
}

export default async function startCron() {
  // start the checker in 24h
  checker_timeout_id = setTimeout(startChecker, 1000 * secondsInOneDay())
  // start the collector
  return startCollectionIfReady()
}
