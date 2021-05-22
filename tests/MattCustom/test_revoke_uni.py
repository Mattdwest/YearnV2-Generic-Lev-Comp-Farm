import pytest

from brownie import Wei, accounts, Contract, config
from brownie import Strategy


def test_revoke_strategy_from_vault(
        chain,
        liveVault,
        strategy,
        unitoken,
        uni_liquidity,
        liveGov,
        rewards,
        guardian,
        strategist,
        alice,
        bob,
        cUni,
        uniLend,
        gov,
):
    # Funding and vault approvals
    # Can be also done from the conftest and remove dai_liquidity from here
    unitoken.approve(uni_liquidity, Wei("1000000 ether"), {"from": uni_liquidity})
    unitoken.transferFrom(
        uni_liquidity, gov, Wei("300000 ether"), {"from": uni_liquidity}
    )
    unitoken.approve(gov, Wei("1000000 ether"), {"from": gov})
    unitoken.transferFrom(gov, bob, Wei("1000 ether"), {"from": gov})
    unitoken.transferFrom(gov, alice, Wei("4000 ether"), {"from": gov})
    unitoken.approve(liveVault, Wei("1000000 ether"), {"from": bob})
    unitoken.approve(liveVault, Wei("1000000 ether"), {"from": alice})

    # users deposit to vault
    liveVault.deposit(Wei("1000 ether"), {"from": bob})
    liveVault.deposit(Wei("4000 ether"), {"from": alice})

    liveVault.setManagementFee(0, {"from": liveGov})
    liveVault.setPerformanceFee(0, {"from": liveGov})
    # liveVault.updateStrategyDebtRatio(uniLend, 1800, {"from": liveGov})
    liveVault.addStrategy(strategy, 3_500, 0, 2 ** 256 - 1, 1_000, {"from": liveGov})

    deposit_amount = unitoken.balanceOf(liveVault)
    # First harvest
    # uniLend.harvest({"from": liveGov})
    strategy.harvest({"from": liveGov})

    # verify deposit successful
    balBefore = cUni.balanceOf(strategy)
    assert balBefore > 0
    # leverage time
    chain.sleep(60)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(60)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(60)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(60)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(60)
    chain.mine(1)
    # verify leverage worked
    balAfter = cUni.balanceOf(strategy)
    assert balAfter > balBefore
    pps_after_first_harvest = liveVault.pricePerShare()
    # wait for profits
    chain.sleep(60)
    chain.mine(300)
    chain.sleep(60)
    chain.mine(300)
    chain.sleep(60)
    chain.mine(300)
    chain.sleep(60)
    chain.mine(300)
    chain.sleep(60)
    chain.mine(300)
    chain.sleep(60)
    chain.mine(300)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(1)
    pps_after_second_harvest = liveVault.pricePerShare()
    assert pps_after_second_harvest > pps_after_first_harvest

    liveVault.revokeStrategy(strategy, {"from": liveGov})
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    #deleverage
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.mine(1)
    assert unitoken.balanceOf(liveVault) > deposit_amount
