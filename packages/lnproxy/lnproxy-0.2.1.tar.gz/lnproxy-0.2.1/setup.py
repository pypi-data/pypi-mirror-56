# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lnproxy']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'hkdf>=0.0.3,<0.0.4',
 'pylightning>=0.0.7.3,<0.0.8.0',
 'secp256k1>=0.13.2,<0.14.0',
 'trio>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['lnproxy = lnproxy.proxy:main']}

setup_kwargs = {
    'name': 'lnproxy',
    'version': '0.2.1',
    'description': "Proxy modified C-Lightning clients' traffic, removing onions for mesh transmission ",
    'long_description': "# Lnproxy\n\nProxy connections from a patched C-Lightning.\n\nProxy removes onions before HTLC transmission and dynamically re-generates them upon receipt.\n\nCurrently hardcoded values for a 3 node regtest, setup. \n\n### Requirements\n\n* Python 3.7.5\n    \n* [pyenv](https://github.com/pyenv/pyenv) \n\n* C-Lightning compiled with noencrypt.patch applied. The patch can be found in clightning dir of this project\n\n\n### General preparation\n\nWe will be cloning one or two code repositories, so let's keep things neat. If you already have a source code directory you can use that, but note that some of the temporary hardcodes in lnproxy.config.py might not work properly... To make a new one and set python version for it (and subdirectories):\n\n    mkdir ~/lnproxy_src && cd ~/lnproxy_src\n    pyenv install 3.7.5 && pyenv local 3.7.5\n\nNow, we are ready to set the projects up...\n\n### C Lightning preparation\n\nPatch C-Lightning with noencrypt patch to disable lightning message encryption. This can either be done by pulling from my branch (recommended), if you followed above instruction you have already done this, or patching C-Lightning manually using the provided patch. To use the pre-patched branch:\n\n    cd ~/lnproxy_src\n    git clone https://github.com/willcl-ark/lightning.git\n    cd lightning\n    git checkout noencrypt-mesh\n\nFollow the remaining installation instructions for your OS as found at [install C-Lightning](https://github.com/willcl-ark/lightning/blob/noencrypt-mesh/doc/INSTALL.md)\n\n### Lnproxy Installation\n\nWe can either clone git repo and install from source, or install via pip.\n\n#### From source\n\nStart by installing the python dependency/package manager poetry (other install methods available, see [website](https://github.com/sdispater/poetry)):\n\n    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n\nNow we can do main clone and setup:\n\n    cd ~/lnproxy_src\n    git clone https://github.com/willcl-ark/lnproxy.git\n    cd lnproxy\n    python3 -m venv .venv\n    source .venv/bin/activate       # bash shell\n    source .venv/bin/activate.fish  # fish shell\n    poetry install\n    \n\n#### Using pip\n\n    mkdir -p ~/lnproxy_src/lnproxy && cd ~/lnproxy_src/lnproxy\n    python3 -m venv .venv\n    source .venv/bin/activate       # bash shell\n    source .venv/bin/activate.fish  # fish shell only\n    pip install lnproxy\n    \n### Fish shell \n\n(Optional, but recommended)\n\nI have added to the C-Lightning contrib startup script in a fish shell version which provides a lot of useful helper functions for regtest environment testing. You can, and I recommend, installing fish shell (no need to make it your default shell, yet!) so that you can use them.\n\nOn macOS, this is as easy as\n\n    brew install fish\n\nBut installation of other platforms is equally easy: [install fish](https://fishshell.com)\n\n        \n## Regtest Testing\n\nTesting currently uses 4 terminal windows, these could also be screen/tmux sessions if you prefer. Lets start, but not connect or use, the 3 C-Lightning nodes:\n\n    cd ~/lnproxy_src/lightning\n    # switch to fish shell\n    fish\n    source contrib/startup_regtest_fish.sh\n    start_ln\n    \nYou will see printed a list of available commands for later reference. Of note you should remember that it is possible to shutdown all three nodes and bitcoind from a single command, `cleanup_ln`.\n\nWe can now start the 3 Lnproxies, one for each node, before connecting the nodes together. In a new terminal window (or screen) for each proxy:\n\n    cd ~/lnproxy_src/lnproxy\n    poetry shell        # alternatively: `source .venv/bin/activate(.fish)`\n    lnproxy 1\n    \nIn the next two terminal windows run the same commands, changing the '1' on the final line to a '2' and a '3' respectively.\n\nNow we can connect the C-Lightning nodes together. In the very first (C-Lightning) terminal window, where we ust sourced the fish shell script and ran `start_ln` above, run the following:\n\n    connect_ln_proxy\n\nThis will connect the three nodes via the python proxies, you should see returned two 'ID' fields. Next, we can try to open some channels, again the fish shell helper function can do this for us easily:\n\n    channel_ln\n    \nIf successful, you will see the channel open transaction IDs and also 6 blocks generated to confirm the channels. At this stage, we can switch to the proxy windows and check for errors and also to see which messages have been exchanged between the nodes. If all looks good, we can try to me a payment:\n\n    l1_pay_l3 1000000\n\n...will attempt to send 1000000 sat from l1 to l3. We use large values as channel size is set to maximum. Other possible combinations to try initially, while the channels are 100% unbalanced, would be:\n\n    l1_pay_l2 1000000\n    l2_pay_l3 1000000\n\nNote that, if it can't find funds or a route C-Lightning polls bitcoind periodically for blockchain info, so usually just wait a few moments and try again.\n\nWith a few initial payments made, the reverse direction payments are possible.\n\n\nAnother useful command I found is waiting for the route from l1 to l3 to be created, for a payment of 100000 this can be watched for using:\n\n    watch $LCLI --lightning-dir=/tmp/l1-regtest getroute (l3-cli getinfo | jq .id) 100000 0\n\n    \n",
    'author': 'willcl-ark',
    'author_email': 'will8clark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willcl-ark/lnproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
