This application uses Firebase Realtime Database.

### RULES

The Rules configuration on the Firebase Console

    {
    "rules": {
        "<<A_DISTRICT_NAME>>": {
            ".read": "'<<A_USER_ID>>' === auth.uid || '<<A_USER_ID>>' === auth.uid ||'<<A_USER_ID>>' === auth.uid || '<<A_USER_ID>>' === auth.uid",

            ".write": "'<<A_USER_ID>>' === auth.uid",
        "$<<VAR_NAME>>": { //this could be named anything
            "<<A_KEY>>": {
            ".write": "'<<A_USER_ID>>' === auth.uid ||'<<A_USER_ID>>' === auth.uid || '<<A_USER_ID>>' === auth.uid"
            }
        }
        }
    }
    }

### DATA STRUCTURE

Districts and routes must be manually added to the firebase structure, as follows:

    generated_name_of_database
        INSERT_DISRTICT_NAME
            INSERT_ROUTE_NAME_1
            INSERT_ROUTE_NAME_2
            ...

### SETUP

You will also need a username and password to match your configuration info.

Configuration info should be placed in a .env file
