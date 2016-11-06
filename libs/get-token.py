from leantesting import Client as LT
import sys

LT = LT.Client()

code = sys.argv[1]

print( 'CODIGO: '+code )

token = LT.auth.exchangeAuthCode(
    'GR3BXtSD3YZ90XOpclT7ZVn42U2pnJ3IivVCcWFa',
    'SgUge4O34cZoNsa314m8izJDZ33swR7XCLBQ6xAF',
    'authorization_code',
    code,
    'http://54.243.245.122:8282/',
)
print( 'TOKEN: ' + token )