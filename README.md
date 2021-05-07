# openCV-Nodejs-PostgreSQL
In this repository, I tried to detect people and vehicles in images using <a href="https://opencv.org/">openCV</a>. I take snapshots of the images and stored them in the <a href="https://www.postgresql.org/">postgresql database</a>. Finally, I used <a href="https://nodejs.org/en/">Node.js</a> and <a href="https://expressjs.com/">Express.js</a> to create an API for displaying images' information.

You can download <strong> YOLOv3-tiny</strong> from <a href="https://pjreddie.com/darknet/yolo/"> here</a>.

To run API you should run commands below in the directory <strong style="back-ground: white">node-api-postgresql</strong>:

1. run  <strong style="back-ground: white">npm init -y</strong>
2. run  <strong style="back-ground: white">npm i express pg</strong>
