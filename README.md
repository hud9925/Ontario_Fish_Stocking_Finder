# Ontario Fish Stocking Finder

The Ontario Fish Stocking Finder is a Python-based web application that helps users find the closest waterbodies stocked with fish by the Ontario Ministry of Natural Resources and Fisheries. 

You can access the application [here](https://3.17.178.206/).


### Search Results

![image](https://github.com/user-attachments/assets/734a77a7-0882-49a5-a173-060b919471f5)

![image](https://github.com/user-attachments/assets/9082880e-3cb6-42a5-a6ff-bdbb362f3948)


## Technologies Used

- **Backend Framework:** Python with Flask for server-side logic.
- **Database:** PostgreSQL hosted on AWS RDS for managing and storing waterbody and fish stocking data.
- **Geocoding API:** Utilized for converting addresses into geographical coordinates.
- **Hosting:** The application is hosted on an AWS EC2 instance
- **Reverse Proxy:** Nginx is used as a reverse proxy server to handle incoming web requests.
- **Gunicorn:** For managing multiple worker processes to handle concurrent requests.

## How It Works

1. **User Input:** Users enter their Ontario address.
2. **Address Geocoding:** The application converts the address into latitude and longitude coordinates.
3. **Database Query:** The app queries the PostgreSQL database hosted on AWS RDS to find the closest stocked waterbodies.
4. **Results Display:** The closest waterbodies, along with their distances, are displayed on the frontend.

## Deployment and Hosting Details

- **AWS EC2:** The web application is deployed on an Amazon EC2 instance, which serves the frontend and backend to users.
- **PostgreSQL on AWS RDS:** The relational database management system is hosted on AWS RDS, providing reliable storage and query performance for the waterbody data.
- **Nginx:** Configured as a reverse proxy to direct incoming traffic to the appropriate services and enhance security.

## Accessing the Application


