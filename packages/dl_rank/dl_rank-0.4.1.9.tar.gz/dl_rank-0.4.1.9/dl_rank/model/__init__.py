from .BaseModel import baseModel

import socket
from tensorflow import gfile
from dl_rank.file import wfile
from dl_rank.file import pathStr
wfile.init_hdfs(socket.gethostname() + '.us-west-2.compute.internal' + ':50070')

gfile.Exists(str(pathStr('hdfs:///user/hadoop')))

