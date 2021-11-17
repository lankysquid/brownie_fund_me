from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # allows this test to only work for local environments
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # confirms that there is an EVM exception
    # which is what we want
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
