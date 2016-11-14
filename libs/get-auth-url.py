from leantesting.Client import Client as LeanTestingClient

LT = LeanTestingClient()

generatedURL = LT.auth.generateAuthLink(
    'oqMpIkSZDBnw5wvd1XAAzihEBCATDDy0JMOlvS9J',
    'http://54.243.245.122:8282/',
    'admin',
    'teste123'
)
print( generatedURL )