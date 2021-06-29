import React from 'react'
import { useAddonState } from './useAddonState'

const useCurrentProject = () => {
  const [currentProject, setProject] = React.useState()
  const {
    sharedState: { project },
  } = useAddonState()

  React.useEffect(() => {
    if (project) {
      fetch(`${process.env.BACKEND_URL}/api/v2/project/${project}/`)
        .then(req => req.text())
        .then(JSON.parse)
        .then(setProject)
    }
  }, [project])

  return currentProject
}

export default useCurrentProject
