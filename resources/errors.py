class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class InstitutionExistsError(Exception):
    pass

class UserExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class MissingInputError(Exception):
    pass

class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "InstitutionExistsError": {
         "message": "There already is a institution by that name",
         "status": 400
     },
     "UserExistsError": {
         "message": "There already is a user by that name",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "This email already exists in database",
         "status": 400
     },
     "MissingInputError": {
       "message": "Missing input",
       "status": 400  
     },
     "UnauthorizedError": {
         "message": "Invalid email or password",
         "status": 401
     }
}
