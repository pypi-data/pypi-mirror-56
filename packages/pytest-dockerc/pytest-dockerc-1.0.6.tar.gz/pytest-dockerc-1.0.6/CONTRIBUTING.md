# With docker

## Create the python environment

    docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/ws -w /ws python:3.7 sh
    pip install docker-compose pytest ipdb ipython

## Run the test

    PYTHONPATH=$(pwd) PYTEST_PLUGINS=pytest_dockerc.plugin pytest --pdb --pdbcls IPython.terminal.debugger:TerminalPdb -s --dockerc-attach-network
