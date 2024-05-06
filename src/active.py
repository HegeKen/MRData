from pymysql import Connection
import config
import json

currentStable = ['air', 'blue',
                 'sapphire', 'sapphiren', 'emerald', 'gold', 'garnet', 'zircon', 'gale', 'aristotle',
                 'umi', 'cmi', 'monet', 'vangogh', 'cas', 'thyme', 'venus', 'courbet', 'star', 'renoir', 'agate', 'vili', 'lisa',
                 'pissarroin', 'cupid', 'zeus', 'psyche', 'daumier', 'mayfly', 'unicorn', 'thor', 'taoyao', 'plato',
                 'fuxi', 'nuwa', 'ishtar', 'cetus', 'odin', 'zizhan', 'babylon', 'nabu', 'elish', 'enuma', 'dagu', 'pipa',
                 'liuqin', 'yudi', 'mona', 'zijin', 'ziyi', 'yuechu', 'lancelot', 'dandelion', 'angelica', 'angelican',
                 'cattail', 'dandelion_c3l2', 'fog', 'fire', 'earth', 'biloba', 'merlin', 'lime', 'cannon', 'gauguin', 'joyeuse',
                 'excalibur', 'curtana', 'mojito', 'curtana_in_rf', 'sweet', 'camellia', 'chopin', 'rosemary', 'lilac', 'selene',
                 'evergo', 'pissarro', 'spes', 'spesn', 'veux', 'fleur', 'viva', 'vida', 'light', 'lightcm', 'opal', 'xaga',
                 'sunstone', 'sky', 'ruby', 'redwood', 'marble', 'pearl', 'tapas', 'topaz', 'sweet_k6a', 'sea', 'cezanne',
                 'apollo', 'alioth', 'haydn', 'ares', 'munch', 'ingres', 'rubens', 'matisse', 'diting', 'mondrian', 'socrates',
                 'corot', 'rembrandt', 'yunluo', 'xun', 'ice', 'water', 'angelicain', 'frost', 'evergreen', 'rock',
                 'rosemary_p', 'surya', 'vayu', 'moonstone']
cnx = None
try:
    cnx = Connection(
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
        autocommit=True
    )
    cursor = cnx.cursor()
    for codename in currentStable:
      up_sql = "UPDATE branches SET active = 1 WHERE codename = %s"
      cursor.execute(up_sql, (codename))

except Exception as e:
    print(e)
finally:
    if cnx:
      cnx.close()
