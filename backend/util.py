from flask_jwt_extended import (
  get_jwt_identity,
)

import models
from models import User

class UserError(Exception):
    def __init__(self, message="User Error"):
        self.message = message

def get_user_from_jwt():
    user_id = get_jwt_identity()
    # check the user exists
    try:
        user = User.get(User.id == user_id)
    except models.DoesNotExist:
        raise UserError("User does not exist")
    if not user:
        raise UserError("User does not exist")
    
    return user