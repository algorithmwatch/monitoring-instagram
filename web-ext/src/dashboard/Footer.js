import React from 'react'
import Box from '@material-ui/core/Box'
import Typography from '@material-ui/core/Typography'
import I18n, { getMessage } from './I18n'

const Footer = () => {
  return (
    <Box component="footer" bgcolor="grey.200" mt={8}>
      <Box maxWidth={800} margin="auto" mt={4} px={2} pt={4} pb={10}>
        <Typography variant="h1">{getMessage('extension_name')}</Typography>
        <Box mt={5}>
          <I18n name="dashboard_footer" />
        </Box>
      </Box>
    </Box>
  )
}

export default Footer
