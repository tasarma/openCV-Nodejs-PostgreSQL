const express = require('express')
const app = express()
const db = require('./queries')
const port = 8000

app.use(express.json())
app.use(
  express.urlencoded({
    extended: true,
  })
)

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/images', db.getImages)
app.get('/images/:id', db.getImageById)
app.delete('/images/:id', db.deleteImage)

app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
