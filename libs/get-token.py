from leantesting import Client as LT
import sys

LT = LT.Client()

code = sys.argv[1]

print( 'CODIGO: '+code )

token = LT.auth.exchangeAuthCode(
    'oqMpIkSZDBnw5wvd1XAAzihEBCATDDy0JMOlvS9J',
    'knQTzlMuHAUtBcJbSz9rDNoJDP2hWMRhXWAvd5PZ',
    'authorization_code',
    code,
    'http://54.243.245.122:8282/',
)
print( 'TOKEN: ' + token )