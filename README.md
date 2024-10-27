# 🎖️ Champs Fund 🎖️

Hi! This is my Django Final Project for She Codes Plus Australia '24-'25!


### What is Champs Fund? 🏋️
 A crowdfunding platform dedicated to supporting aspiring young athletes in the Philippines who demonstrate exceptional talent but lack the financial means to participate in national competitions. Our platform will bridge the gap between passionate sports enthusiasts and these promising athletes, providing an avenue to directly contribute to their dreams and ambitions. 
 
 Champs Fund platform specifically focuses on supporting aspiring young athletes between the ages of 5-18 years old, helping them to overcome financial barriers and pursue their potential in sports.

### Intended Audience/User Stories
The intended audience for the "Champs Fund" crowdfunding platform includes:

🏃 Sports Enthusiasts: Individuals who are passionate about sports and want to directly support the growth and development of young Filipino athletes. They will use the platform to discover athletes, learn about their backgrounds and achievements, and contribute financially to help them reach their goals.

🕺 Philanthropists: Those who are interested in making a meaningful impact on the lives of underprivileged youth. They will use the website to find athletes whose stories resonate with them and donate towards their training and competition expenses.

🏄‍♀️ Corporations: Businesses looking to support community initiatives, foster positive brand associations, and fulfill their social responsibility goals. They will use the platform to make contributions or sponsor specific athletes or events, gaining visibility and goodwill in the process.

🏄‍♀️ Filipino Diaspora: Filipinos living abroad who wish to contribute to the growth of sports in the Philippines. They can use the platform to support young talents from their home country, helping them pursue their athletic dreams on a national or international stage.}}


### API Spec
| URL                       | HTTP Method | Purpose                                             | Request Body                                             | Success Response Code | Authentication/Authorization |
|---------------------------|-------------|-----------------------------------------------------|----------------------------------------------------------|-----------------------|------------------------------|
| /athletes/                | GET         | Retrieves a list of all athlete profiles.            | None                                                     | 200                   | None                         |
| /athletes/                | POST        | Creates a new athlete profile.                       | `{ "first_name": "string", "last_name": "string", "age": integer, ... }` | 201                   | Authentication required     |
| /athletes/{id}/           | GET         | Retrieves a specific athlete profile by its ID.      | None                                                     | 200                   | None                         |
| /athletes/{id}/           | PUT         | Updates a specific athlete profile by its ID.        | `{ "first_name": "string", "last_name": "string", "age": integer, ... }` | 200                   | Authentication required     |
| /athletes/{id}/           | DELETE      | Deletes a specific athlete profile by its ID.        | None                                                     | 204                   | Authentication required     |
| /pledges/                 | GET         | Retrieves a list of all pledges.                     | None                                                     | 200                   | None                         |
| /pledges/                 | POST        | Creates a new pledge.                                | `{ "amount": integer, "message": "string", "athlete_id": integer, ... }` | 201                   | Authentication required     |
| /pledges/{id}/            | GET         | Retrieves a specific pledge by its ID.               | None                                                     | 200                   | None                         |
| /pledges/{id}/            | PUT         | Updates a specific pledge by its ID.                 | `{ "amount": integer, "message": "string", ... }`        | 200                   | Authentication required     |
| /pledges/{id}/            | DELETE      | Deletes a specific pledge by its ID.                 | None                                                     | 204                   | Authentication required     |
| /progress-updates/        | GET         | Retrieves a list of all progress updates.            | None                                                     | 200                   | None                         |
| /progress-updates/        | POST        | Creates a new progress update.                       | `{ "title": "string", "content": "string", "athlete_id": integer, ... }` | 201                   | Authentication required     |
| /progress-updates/{id}/   | GET         | Retrieves a specific progress update by its ID.      | None                                                     | 200                   | None                         |
| /progress-updates/{id}/   | PUT         | Updates a specific progress update by its ID.        | `{ "title": "string", "content": "string", ... }`        | 200                   | Authentication required     |
| /progress-updates/{id}/   | DELETE      | Deletes a specific progress update by its ID.        | None                                                     | 204                   | Authentication required     |
| /badges/                  | GET         | Retrieves a list of all badges.                      | None                                                     | 200                   | None                         |
| /badges/                  | POST        | Creates a new badge.                                 | `{ "name": "string", "description": "string", ... }`     | 201                   | Authentication required     |

### DB Schema
![]( {{ ./AthleteProfile.png}})