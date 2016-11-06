from leantesting.Client import Client as LeanTestingClient

LT = LeanTestingClient()

generatedURL = LT.auth.generateAuthLink(
    'GR3BXtSD3YZ90XOpclT7ZVn42U2pnJ3IivVCcWFa',
    'http://54.243.245.122:8282/',
    'write',
    'teste123'
)
print( generatedURL )