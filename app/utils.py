# i want to extract all the hashing logic and stored in its own function. this file is gonna store bunch of utility functions.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")          # for the security of our users we shouldn't save and store the actual password of them and we have to hash them and store them. to do that we install two library (pip install passlib[bccrypt]) and execute this line of code.all we're doing here is we're telling the passlib what is the default algoritem of hashing?.


def hash(password: str):
    return pwd_context.hash(password)          # we're going to hash what the user pass as a password


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)       # this little fucntion is gonna compare the hashed password that sotred in
               # our database to the attempted password by user .we import utils file to auth.py and do the rest.

# (.verify is gonna verify secret against an existing hash.)