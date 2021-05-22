import pytest
from brownie import config, Contract

# Snapshots the chain before each test and reverts after test completion.
@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def gov(accounts):
    yield accounts[0]

@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def alice(accounts):
    yield accounts[6]


@pytest.fixture
def bob(accounts):
    yield accounts[7]

@pytest.fixture
def uni_liquidity(accounts):
    yield accounts.at("0xbe0eb53f46cd790cd13851d5eff43d12404d33e8", force=True)

@pytest.fixture
def unitoken():
    token_address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
    yield Contract(token_address)

@pytest.fixture
def cUni():
    token_address = "0x35A18000230DA775CAc24873d00Ff85BccdeD550"
    proxy = "0xa1849880593E96d2f7dF77D0D38a7f2372aE10E0"
    yield Contract.from_explorer(token_address, as_proxy_for=proxy)

@pytest.fixture
def strategy(
    strategist,
    guardian,
    keeper,
    liveVault,
    Strategy,
    cUni,
):
    strategy = guardian.deploy(
        Strategy,
        liveVault,
        cUni
    )
    strategy.setKeeper(keeper)
    yield strategy


@pytest.fixture
def uni():  # unirouter contract
    yield Contract("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

@pytest.fixture
def newstrategy(
    strategist,
    guardian,
    keeper,
    liveVault,
    Strategy,
    cUni,
):
    newstrategy = guardian.deploy(
        Strategy,
        liveVault,
        cUni
    )
    newstrategy.setKeeper(keeper)
    yield newstrategy

@pytest.fixture
def uniLend():
    address = "0x5e882c9f00209315e049B885B9b3dfbEe60D80A4"
    yield Contract.from_explorer(address)


@pytest.fixture
def me(accounts):
    yield accounts.at("0x1a123d835B006d27d4978C8EB40B14f08e0b8607", force=True)

@pytest.fixture
def liveGov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)

@pytest.fixture
def liveVault():
    address = "0xFBEB78a723b8087fD2ea7Ef1afEc93d35E8Bed42"
    yield Contract.from_explorer(address)
