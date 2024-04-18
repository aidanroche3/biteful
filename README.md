
<h1 align="center">Biteful</h1>
  <p align="center">
  <img width="300" alt="biteful" src="https://github.com/aidanroche3/biteful/assets/123038068/d99e2aef-20b3-4466-8ca0-d159fca8de91">
  </p>

Biteful is a user-centric hub connecting diners, restaurant owners, food critics, and administrators. Diners can find, review, and receive recommendations for restaurants. Owners manage listings and engage with feedback, while critics contribute reviews and articles. Administrators oversee data integrity and platform enhancements, by moderating reviews and approving restaurants to the platform. With tailored features for each user, the platform aims to redefine dining experiences through transparency and community engagement, allowing users to find the best restaurants based on the cuisine, price, location, and reviews.

[Video Demo](https://www.youtube.com/watch?v=camQAQ3V9Qg)

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

## Authors
- [Aidan Roche](https://github.com/aidanroche3)
- [Ethan Moskowitz](https://github.com/EthanMoskowitz)
- [Ray Kong](https://github.com/Ray-kong)
- [Matthew Tung](https://github.com/MatthewRTung)
- [Daniel Rachev](https://github.com/stendeze)
