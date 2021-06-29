import React from 'react'
import Typography from '@material-ui/core/Typography'
import marked from 'marked'
import propTypes from 'prop-types'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles(theme => ({
  root: {
    '& > *': {
      margin: 0,
      padding: 0,
    },
    '& h1, & h2, & h3, & h4, & h5': {
      marginTop: '0.80em',
      marginBottom: '0.35em',
    },
    '& h1': {
      ...theme.typography.h1,
    },
    '& h2': {
      ...theme.typography.h2,
    },
    '& h3': {
      ...theme.typography.h3,
    },
    '& h4': {
      ...theme.typography.h4,
    },
    '& h5': {
      ...theme.typography.h5,
    },
    '& p+p': {
      marginTop: '0.80em',
      marginBottom: '0.35em',
    },
  },
}))

const TypographyMarked = ({ md, ...other }) => {
  const classes = useStyles()
  if (!md) {
    return null
  }
  return (
    <Typography
      component="div"
      {...other}
      className={classes.root}
      dangerouslySetInnerHTML={{ __html: marked(md) }}
    />
  )
}

TypographyMarked.propTypes = {
  md: propTypes.string,
}

export default React.memo(TypographyMarked)
