import React from 'react'
import Radio from '@material-ui/core/Radio'
import RadioGroup from '@material-ui/core/RadioGroup'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import FormControl from '@material-ui/core/FormControl'
import FormLabel from '@material-ui/core/FormLabel'
import Collapse from '@material-ui/core/Collapse'
import Button from '@material-ui/core/Button'
import Box from '@material-ui/core/Box'
import { useAddonState } from './hooks/useAddonState'
import sendDispatchMsg from '../utils/sendDispatchMsg'
import { LOCAL_STATE_SET_PROJECT } from '../constantes'
import { getMessage } from './I18n'

const ChangeProjectLink = () => {
  const [showProjectList, setShowProjectList] = React.useState(false)
  const [selectedProject, setSelectedProject] = React.useState('')
  const [projects, setProjects] = React.useState([])
  const {
    sharedState: { project },
  } = useAddonState()

  React.useEffect(() => {
    setSelectedProject(project)
  }, [project])

  React.useEffect(() => {
    if (!projects.length && showProjectList) {
      fetch(`${process.env.BACKEND_URL}/api/v2/project/?active=true`)
        .then(req => req.text())
        .then(JSON.parse)
        .then(setProjects)
    }
  }, [showProjectList, projects])

  const handleSave = e => {
    e.preventDefault()
    sendDispatchMsg({ type: LOCAL_STATE_SET_PROJECT, payload: selectedProject })
    setShowProjectList(false)
  }

  return (
    <>
      {!showProjectList && (
        <Button onClick={() => setShowProjectList(true)}>
          {getMessage('dashboard_changeProject_buttonLabel')}
        </Button>
      )}
      <Collapse in={showProjectList}>
        <Box my={3}>
          <form onSubmit={handleSave}>
            <FormControl component="fieldset">
              <FormLabel component="legend">
                {getMessage('dashboard_changeProject_projectsListTitle')}
              </FormLabel>
              <RadioGroup
                aria-label="project"
                name="project"
                value={selectedProject}
                onChange={e => setSelectedProject(parseInt(e.target.value, 10))}
              >
                {projects.map(project => (
                  <FormControlLabel
                    key={project.id}
                    value={project.id}
                    control={<Radio />}
                    label={project.name}
                  />
                ))}
              </RadioGroup>
              <Box display="flex" mt={2} mb={3}>
                <Box mr={3}>
                  <Button
                    type="submit"
                    color="primary"
                    disabled={selectedProject === project}
                  >
                    {getMessage('dashboard_changeProject_saveButton')}
                  </Button>
                </Box>
                <Button
                  onClick={() => {
                    setShowProjectList(false)
                    setSelectedProject(project)
                  }}
                >
                  {getMessage('dashboard_changeProject_cancelButton')}
                </Button>
              </Box>
            </FormControl>
          </form>
        </Box>
      </Collapse>
    </>
  )
}

export default ChangeProjectLink
