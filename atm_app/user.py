from hashlib import sha512

salt = "hello world"

class User:
  def __init__(self, account, pin, balance):
    self.account = account
    self.pin = pin
    self.balance = balance

user_dictionary = {}

# if the user exists in the dictionary, ensure the pin matches then return it
# if the pins do not match, then return `None`
# if the user isn't in the dictionary, create & return a new user with this info
def login(account, pin, request):
  if account in user_dictionary:
    user = user_dictionary[account]
    if (pin == user.pin):
      generate_auth_token(user, request)
      return True
    else:
      return False

  else:
    new_user = User(account, pin, 100000000)
    user_dictionary[account] = new_user
    generate_auth_token(new_user, request)

    return True

def generate_auth_token(user, request):
  auth_token = user.account + "." + make_hash(user.account)
  request.session['auth_token'] = auth_token

def authenticate(request):
  if ('auth_token' not in request.session):
    return None

  auth_token = request.session['auth_token']
  components = auth_token.split('.')
  if make_hash(components[0]) == components[1]:
    return user_dictionary[components[0]]
  
def make_hash(account):
  return sha512(str(account + salt).encode('utf-8')).hexdigest()