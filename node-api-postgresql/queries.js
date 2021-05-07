const Pool = require('pg').Pool
const pool = new Pool({
  user: 'python',
  host: 'localhost',
  database: 'dbname',
  password: 'password',
  port: 5432,
})

// Get all images
const getImages = (request, response) => {
    pool.query('SELECT * FROM images ORDER BY id', (error, results) => {
      if (error) {
        throw error
      }
      response.status(200).json(results.rows)
    })
  }


//Get image by id
const getImageById = (request, response) => {
    const id = parseInt(request.params.id)
  
    pool.query('SELECT * FROM images WHERE id = $1', [id], (error, results) => {
      if (error) {
        throw error
      }
      response.status(200).json(results.rows)
    })
  }

// Delete image 
const deleteImage = (request, response) => {
    const id = parseInt(request.params.id)
  
    pool.query('DELETE FROM images WHERE id = $1', [id], (error, results) => {
      if (error) {
        throw error
      }
      response.status(200).send(`User deleted with ID: ${id}`)
    })
  }


  module.exports = {
    getImages,
    getImageById,
    deleteImage,
  }