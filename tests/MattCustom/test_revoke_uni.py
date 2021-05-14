import pytest

from brownie import Wei, accounts, Contract, config
from brownie import StrategyPoolTogether


def test_revoke_strategy_from_vault(
    chain,
    vault,
    strategy,
    ticket,
    unitoken,
    uni_liquidity,
    gov,
    rewards,
    guardian,
    strategist,
    alice,
    bob,
    tinytim,
):
    # Deposit to the vault and harvest
    # Funding and vault approvals
    # Can be also done from the conftest and remove dai_liquidity from here
    unitoken.approve(uni_liquidity, Wei("1000000 ether"), {"from": uni_liquidity})
    unitoken.transferFrom(
        uni_liquidity, gov, Wei("300000 ether"), {"from": uni_liquidity}
    )
    unitoken.approve(gov, Wei("1000000 ether"), {"from": gov})
    unitoken.transferFrom(gov, bob, Wei("1000 ether"), {"from": gov})
    unitoken.transferFrom(gov, alice, Wei("4000 ether"), {"from": gov})
    unitoken.transferFrom(gov, tinytim, Wei("10 ether"), {"from": gov})
    unitoken.approve(vault, Wei("1000000 ether"), {"from": bob})
    unitoken.approve(vault, Wei("1000000 ether"), {"from": alice})
    unitoken.approve(vault, Wei("1000000 ether"), {"from": tinytim})

    # users deposit to vault
    vault.deposit(Wei("1000 ether"), {"from": bob})
    vault.deposit(Wei("4000 ether"), {"from": alice})
    vault.deposit(Wei("10 ether"), {"from": tinytim})

    vault.setManagementFee(0, {"from": gov})
    vault.setPerformanceFee(0, {"from": gov})

    deposit_amount = unitoken.balanceOf(vault)

    # First harvest
    strategy.harvest({"from": gov})

    assert ticket.balanceOf(strategy) > 0
    chain.sleep(3600 * 24 * 14)
    chain.mine(1)

    vault.revokeStrategy(strategy, {"from": gov})
    strategy.harvest({"from": gov})
    assert unitoken.balanceOf(vault) > deposit_amount
