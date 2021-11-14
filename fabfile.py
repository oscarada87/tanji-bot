import os
from dotenv import load_dotenv

load_dotenv()

from fabric import task

@task
def deploy(c, branch='main'):
    # server = os.getenv('SERVER')
    # c = Connection(server)
    print('Start deploying!')
    # stop container
    result = c.run('cd tanjimeow && docker-compose down', warn=True)
    print(result.stdout)

    # remove folder
    result = c.run('rm -rf tanjimeow', warn=True)
    print('remove old folder...')

    # clone from github
    result = c.run("git clone -b {} --single-branch git@github.com:oscarada87/tanjimeow.git".format(branch), warn=True)
    print(result.stdout)

    # clone env file
    result = c.run('cp .env tanjimeow/', warn=True)
    print('copy env file...')

    # run docker compose
    result = c.run('cd tanjimeow && docker-compose up --force-recreate --build --remove-orphans -d', warn=True)
    print(result.stdout)
    print('Done!')
