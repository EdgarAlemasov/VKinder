"""
    This vk bot will find a people by your searching params.
    Input your params here and start main.py
    After you can see result in chat with your vk group!
    GOOD LUCK
"""

"""
    DataBase settings.
    Change them if you need.
    
    Default table include 4 fields [id], [user_id], [first_name], [url]
    If you need change them, go to DataBase.py -> create_db function.
"""
user_login = 'postgres'
user_password = 'ImAlive72ae'
host = '127.0.0.1'
port = '5432'
supreme_database_name = 'postgres'
database_name = 'vkinder72'


"""
    VK Token settings.
    Permission for actions your project in net!
"""
# token = group token for starting swap messages between bot and user
token = ''
# token2 = your personal token to use search.params by bot in project
token2 = ''