# ******************** MINING SETTINGS ***************

# Specify pool target as int >= 1
POOL_TARGET = 10


# ******************** GENERAL SETTINGS ***************

# Enable some verbose debug (logging requests and responses).
DEBUG = False

# Destination for application logs, files rotated once per day.
LOGDIR = 'log/'

# Main application log file.
LOGFILE = None#'stratum.log'

# Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGLEVEL = 'INFO'

# How many threads use for synchronous methods (services).
# 30 is enough for small installation, for real usage
# it should be slightly more, say 100-300.
THREAD_POOL_SIZE = 50

ENABLE_EXAMPLE_SERVICE = False

# ******************** TRANSPORTS *********************

# Hostname or external IP to expose
HOSTNAME = 'localhost'

# Port used for Socket transport. Use 'None' for disabling the transport.
LISTEN_SOCKET_TRANSPORT = 3332

# Port used for HTTP Poll transport. Use 'None' for disabling the transport
LISTEN_HTTP_TRANSPORT = None

# Port used for HTTPS Poll transport
LISTEN_HTTPS_TRANSPORT = None

# Port used for WebSocket transport, 'None' for disabling WS
LISTEN_WS_TRANSPORT = None

# Port used for secure WebSocket, 'None' for disabling WSS
LISTEN_WSS_TRANSPORT = None

# Hostname and credentials for one trusted Bitcoin node ("Satoshi's client").
# Stratum uses both P2P port (which is 8333 already) and RPC port
BITCOIN_TRUSTED_HOST = 'localhost'
BITCOIN_TRUSTED_PORT = 8330
BITCOIN_TRUSTED_USER = 'bitcoinrpc'
BITCOIN_TRUSTED_PASSWORD = '3uxMBBTgSPF6PNxixcPXP8wMddpuA6NvjfJPLGTivroR'

# Use "echo -n '<yourpassword>' | sha256sum | cut -f1 -d' ' "
# for calculating SHA256 of your preferred password
#ADMIN_PASSWORD_SHA256 = None
ADMIN_PASSWORD_SHA256 = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' # SHA256 of the password

IRC_NICK = None


MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'pooldb'
MYSQL_USER = 'pooldb'
MYSQL_PASSWORD = 'pooldb'


# Pool related settings
INSTANCE_ID = 31
CENTRAL_WALLET = '16tZAGyGy7Mknz8uSEHjsHqfqZNMqrGqSm'
PREVHASH_REFRESH_INTERVAL = 5 # in sec
MERKLE_REFRESH_INTERVAL = 60 # How often check memorypool
COINBASE_EXTRAS = '/srs/'
