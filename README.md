# SkyFly Backend

## Made by Marharyta Cherednychenko from EIfu-23!

The goal of this coursework is to develop a web application that facilitates the process of buying flight tickets online, providing a convenient and efficient alternative to traditional methods. <br/>
This project aims to streamline the booking process, making it accessible from the comfort of your home, and offering additional features to enhance the user experience.

In today's world, we heavily rely on gadgets and apps to simplify our daily tasks and save time. This project aligns with that trend by creating an application that allows <br/>
users to purchase flight tickets without the need to visit a physical ticket office.

## Key Features

- **User Account Management**: Users can create and manage their accounts, providing a personalized experience.
- **Flight Booking**: Users can search for and book flights easily through the application.
- **User Interaction**: The app allows users to share their thoughts, leave reviews, and contact customer support anytime.
- **Admin Capabilities**: Administrators have the ability to create flights, manage passenger information, and perform other crucial tasks.

By eliminating the need for long lines and simplifying the booking process, this application ensures a hassle-free experience for all users. <br/>
Everything from booking to customer service is made easy with our app, revolutionizing the way people purchase flight tickets.

## Images of SkyFly

#### Detailed flight page

<img src="/uploads/flight_page.png" alt="Flight page" style="width:500px;"/>

#### Search for most suitable flight

<img src="/uploads/flights.png" alt="Flights" style="width:500px;"/>

#### Home page

<img src="/uploads/home_page.png" alt="Home page" style="width:500px;"/>

#### Booking tickets

<img src="/uploads/ticket_creation.png" alt="Booking tickets" style="width:500px;"/>

#### User profile, past and future tickets pages

<img src="/uploads/user_tickets.png" alt="User tickets" style="width:500px;"/>

## Run project locally

1. Install python packages

```bash
sudo apt install python3-pip python3
pip install --user pipenv
```

2. Set python path

   Save the python path variable in the ~/.bashrc file for convenience.
   Replace [username] with your linux user. To see it just use this command:

```bash
echo $USER
```

Then set the variable:

- Open .bashrc file for editing

```bash
nano ~/.bashc
```

- Copy and paste this line at the top of the file

```bash
export PYTHONPATH="${PYTHONPATH}:/home/[username]/"
```

- Press ctrl+X, then Y, then enter. And save file

```bash
source ~/.bashrc
```

Or just do it from your command line every time you open terminal

```bash
export PYTHONPATH="${PYTHONPATH}:/home/[username]/"
```

3. Clone the repository

```bash
git clone git@github.com:margoch24/skyfly-backend.git && cd skyfly-backend
```

4. Install dependencies

```bash
pipenv install
```

5. Create .env file (from .env.example)

6. Run project:

```bash
pipenv run start
```

## Setup mysql database

### Development / Production

1. Enter mysql:

```bash
mysql -u root -p
```

2. Create mysql database:

```bash
CREATE DATABASE skyfly;
```

3. Create new mysql user with a password requirement

```bash
CREATE USER 'skyfly'@'localhost';
ALTER USER 'skyfly'@'localhost' IDENTIFIED WITH mysql_native_password BY '[your password here]';
```

4. grant privileges to this user for database 'skyfly'

```bash
GRANT ALL PRIVILEGES ON skyfly.* TO 'skylfy'@'localhost';
FLUSH PRIVILEGES;
```

5. exit mysql

```bash
exit;
```

### Test

1. Enter mysql:

```bash
mysql -u root -p
```

2. Create mysql database:

```bash
CREATE DATABASE test_skyfly;
```

3. Create new mysql user without a password requirement

```bash
CREATE USER 'test-skyfly'@'localhost';
ALTER USER 'test-skyfly'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
```

4. grant privileges to this user for database 'test_skyfly'

```bash
GRANT ALL PRIVILEGES ON test_skyfly.* TO 'test-skylfy'@'localhost';
FLUSH PRIVILEGES;
```

5. exit mysql

```bash
exit;
```

## Testing

### Run all tests

```bash
pipenv run test
```

### Run single test

1. add `_only` to the end of the method name of the test you want to test.<br>
   _def test_successful(self) ---> def test_successful_only(self)_

2. run single test:

```bash
pipenv run test-only
```

### Create tests

It is important to start all the names of the files you want to test with `test_`.

## Use project locally

To interact with the API routes, navigate to http://localhost:[your_port] after starting the project. You can use tools like Postman, your web browser, or other available resources to send requests and receive responses.

Additionally, the included tests serve as a valuable resource. These tests cover a wide range of scenarios, both successful and failed, providing detailed explanations on how to use the routes. They specify the required data for each request and describe the expected responses, helping you understand and utilize the API effectively.

## Body/Analysis

The application is built using Python, a powerful and versatile programming language known for its simplicity and readability. I utilize Flask, a lightweight web framework, to handle the backend operations and API routes. The application interacts seamlessly with a frontend project, providing a comprehensive solution for users to book flights conveniently from their homes. Below, I provide an analysis and explanation of the program's implementation, demonstrating how it meets the defined objectives and functional requirements. The frontend of the application is developed using modern web technologies (React + Vite + TypeScript) and can be accessed through the provided Github repository: https://github.com/margoch24/skyfky-frontend

### OOP pillars

- **Polymorphism**: olymorphism is a fundamental concept in object-oriented programming that allows objects of different classes to be treated as objects of a common superclass. In simpler terms, it means that different classes can have methods with the same name, but different implementations. `RequestValidator` can be an example of polymorphism exploited through inheritance and method overriding. <br/>
  `RequestValidator` serves as a common interface for its subclasses (`BodyRequestValidator`, `QueryRequestValidator`, and `FilesRequestValidator`). These subclasses provide specific implementations for the abstract methods `validate()` and `load()`, which are defined in the `RequestValidator` base class.
- **Abstraction**: Abstraction is a fundamental concept that focuses on hiding the complex implementation details of a system and exposing only the necessary and relevant aspects of an object. This makes the system easier to understand and use by reducing complexity and allowing the programmer to work at a higher level of thought. <br/>
  For instance, the `RequestValidator` class defines a common interface for all request validators. This ensures that any type of request validator (body, query, files) will have validate and load methods, making the code more predictable and easier to use. <br/>
  The specific details of how validation and loading are performed for body, query, and files are hidden behind the abstract methods. Users of these classes interact with the abstract interface without needing to know the specifics of each implementation.<br/>
  By defining a common interface, it is possible to create new types of request validators easily. Just create a new subclass of `RequestValidator` and implement the required methods.

- **Inheritance**: Inheritance in programming is a feature of Object-Oriented Programming that allows a class (called a subclass or derived class) to inherit attributes and methods from another class (called a superclass or base class). This promotes code reuse and can help in organizing code into hierarchical relationships. <br/>
  `BaseModel` class can be a good example of it. `BaseModel` is the base class that contains common attributes and methods which are expected to be shared among multiple models. For example, it has `created_at` and `updated_at` fields, and various class methods for creating, updating, and deleting records in the database. <br/>
  `User` and other models are subclasses of `BaseModel`. They inherit all the attributes and methods from `BaseModel`, meaning they can use all the functionality defined in `BaseModel` without needing to redefine them.<br/>
  The concept of inheritance is also used in the `TestInitializer` class, which serves as the base class for all other test classes.
- **Encapsulation**: Encapsulation is a fundamental principle that involves bundling the data (attributes) and methods (functions) that operate on the data into a single unit called a class. It restricts direct access to some of an object's components, which can prevent the accidental modification of data. Encapsulation is achieved using access modifiers: `_` (single underscore) for **protected** variables and `__` (double underscore) for **private** variables.<br/>
  In the code, encapsulation is used via private variables in all classes to define the expected request data (e.g., `PostFlightBody`, `PostContactUsBody`, and others). This approach is also applied in main classes such as `FlaskApp`, `AppScheduler`, `Database`, and others. Some of these private variables are intended to be accessible via `@property` decorator, while others are not.

### Design patterns

There are at least 2 design patterns used in the code, namely Singleton and Decorator.

- **Singleton**: The Singleton design pattern was implemented for the `Database` class via `SingletonMeta` metaclass. In this case, using Singleton ensures that there's only one database connection throughout the application. Given that a Flask application typically serves multiple requests simultaneously, having multiple instances of the database connection can lead to inefficiencies, resource wastage, and potential conflicts. By enforcing Singleton, I ensure that all parts of the application use the same database connection, maintaining consistency and reducing overhead.
- **Decorator**: The Decorator design pattern was implemented for the `validate_request` function as middleware to ensure that request data is valid and correct. It is invoked before processing any request, so if the data is invalid, it returns an error first. It is used in all controllers via a decorator sign like this: `@validate_request(PostLoginSchema, RequestValidatorTypes.Body)`, where it validates the expected Schema with all received body properties. It was chosen because it can be easily modified, read and understood in code, which is very good for other programmers and yourself to understand where the validation of the data takes place, looks neat, because it takes only one line and can be reused. It is also very important to check that all data is correct before proceeding with any functionality, and to stop before proceeding if an error is detected.

### Reading from file & writing to file

The project utilizes the MySQL database, seamlessly integrated through Flask with the `flask-sqlalchemy` library. Instead of relying on files for data storage and retrieval, leveraging the database ensures enhanced security and robust protection for the stored data.

### Testing

The project uses tests written with the `unittest` library. They exists for each possible case check both successful and failed responses, where errors are written by programme and can be caused by user carelessness or cyber attacks, simply protecting the project. How to install and run them you can find above. The total number of tests is 131.

## Results and Summary

The SkyFly Backend project has been successfully implemented, providing a robust web application for purchasing flight tickets online. Users can create accounts, book flights, interact with the system, and administrators can manage various aspects of the platform.

Despite facing challenges such as setting up and configuring the database, integrating with the frontend, and ensuring data validation and security, I effectively navigated these hurdles through collaborative problem-solving and diligent testing.

The use of Flask for backend development and modern web technologies for the frontend facilitated a streamlined development process. By leveraging design patterns like Singleton and Decorator, I ensured efficient code organization and maintainability.

## Conclusions

The coursework successfully developed the SkyFly Backend web application, fulfilling its primary objective of providing a convenient and efficient platform for purchasing flight tickets online. By eliminating the need for physical ticket offices and long lines, the program simplifies the booking process, making it accessible from the comfort of users' homes. The program includes a robust suite of tests covering various scenarios, ensuring the reliability and stability of the application.

### Future prospects

The future prospects of the program involve potential enhancements and expansions, such as integrating additional features like:

- **Payment system integraion with Stripe**: This involves integrating the Stripe payment system into the app to enable secure and convenient online transactions. Users can make payments for their flight bookings using various methods such as credit cards, debit cards, and digital wallets.
- **Baggage options, and loyalty programs.**: Adding baggage options to the app allows users to customize their travel experience by selecting and purchasing additional baggage allowance during the booking process. Incorporating loyalty programs incentivizes repeat business by rewarding frequent travelers with points or miles for each booking. These points can be redeemed for discounts, upgrades, or other perks, fostering customer loyalty and increasing user engagement with your app.
- **Expansion to retailers and companies**: Expanding the app's services to retailers and companies opens up new market opportunities and revenue streams. By offering corporate booking solutions, the app can cater to the unique needs of businesses, such as group booking capabilities, corporate travel policies integration, and reporting tools for expense management.

## Format python code VSCode

1. Install vscode extensions

- Black Formatter
- isort

2. Go to Settings (ctrl+Comma) > settings.json (top right corner "Open Settings (JSON)")

Add:

```json
"[python]": {
   "editor.formatOnSave": true,
   "editor.defaultFormatter": "ms-python.black-formatter",
   "editor.codeActionsOnSave": {
      "source.organizeImports": true
   }
},
"isort.args": ["--profile", "black"]
```

3. Upgrade vscode if changes have no effect:

````bash
sudo apt update
sudo apt install code
