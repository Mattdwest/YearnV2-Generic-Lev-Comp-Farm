# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")

import pytest

from brownie import Wei, accounts, Contract, config
from brownie import Strategy


@pytest.mark.require_network("mainnet-fork")
def test_operation(
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
    liveVault.updateStrategyDebtRatio(uniLend, 3800, {"from": liveGov})
    liveVault.addStrategy(strategy, 3_000, 0, 2 ** 256 - 1, 1_000, {"from": liveGov})

    # First harvest
    uniLend.harvest({"from": liveGov})
    strategy.harvest({"from": liveGov})

    #verify deposit successful
    balBefore = cUni.balanceOf(strategy)
    assert balBefore > 0
    #leverage time
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600)
    chain.mine(1)
    #verify leverage worked
    balAfter = cUni.balanceOf(strategy)
    assert balAfter > balBefore
    pps_after_first_harvest = liveVault.pricePerShare()
    #wait for profits
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(1)
    pps_after_second_harvest = liveVault.pricePerShare()
    assert pps_after_second_harvest > pps_after_first_harvest

    #daily harvests for a week
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 7)
    chain.mine(300 * 24)
    chain.sleep(3600)
    chain.mine(1)
    strategy.harvest({"from": liveGov})

    # 6 hours for pricepershare to go up
    strategy.harvest({"from": liveGov})
    chain.sleep(3600 * 6)
    chain.mine(1)

    alice_vault_balance = liveVault.balanceOf(alice)
    liveVault.withdraw(alice_vault_balance, alice, 75, {"from": alice})
    assert unitoken.balanceOf(alice) > 0
    assert unitoken.balanceOf(bob) == 0

    bob_vault_balance = liveVault.balanceOf(bob)
    liveVault.withdraw(bob_vault_balance, bob, 75, {"from": bob})
    assert unitoken.balanceOf(bob) > 0
    assert unitoken.balanceOf(strategy) == 0

    # We should have made profit
    assert liveVault.pricePerShare() > 1e18
