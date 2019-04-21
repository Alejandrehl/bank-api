### Instalación
- Clone repository
- docker-compose build
- docker-composer up

### Important
- web/app.py.
- For test "production server" use ec2-35-165-231-168.us-west-2.compute.amazonaws.com:5000/ instead of http://0.0.0.0:5000/

### In the following APIS, you must pass two arguments: username and password.
- In Postman send as { "username" : "Alejandro", "password" : "Alejandro"} // JSON(application/json)
- http://0.0.0.0:5000/register to register an user.
- http://0.0.0.0:5000/balance to get balance of user.

### In the following APIS, you must pass three arguments: username, password and amount.
- In Postman send as { "username" : "Alejandro", "password" : "Alejandro", "amount" : 2500} // JSON(application/json)
- http://0.0.0.0:5000/add to add amount to user account.
- http://0.0.0.0:5000/takeloan to take a loan.
- http://0.0.0.0:5000/payloan to pay loan.

### In the following APIS, you must pass four arguments: username, password, to and amount.
- In Postman send as { "username" : "Alejandro", "password" : "Alejandro", "to": "Fernanda", "amount" : 2500} // JSON(application/json)
- http://0.0.0.0:5000/transfer to transfer amount to other user account.
