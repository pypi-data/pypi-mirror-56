import logging

from web3 import Web3
import skale.contracts as contracts
from skale.wallets import BaseWallet
from skale.contracts_info import CONTRACTS_INFO
from skale.utils.helper import get_abi
from skale.utils.web3_utils import get_provider
from skale.utils.exceptions import InvalidWalletError, EmptyWalletError

logger = logging.getLogger(__name__)


class EmptyPrivateKey(Exception):
    pass


class Skale:
    def __init__(self, endpoint, abi_filepath, wallet=None):
        logger.info(f'Init skale-py, connecting to {endpoint}')
        provider = get_provider(endpoint)
        self.web3 = Web3(provider)
        self.abi = get_abi(abi_filepath)
        self.__contracts = {}
        self.__contracts_info = {}
        self.nonces = {}
        if wallet:
            self.wallet = wallet
        self.__init_contracts_info()
        self.__init_contracts()

    @property
    def wallet(self):
        if not self._wallet:
            raise EmptyWalletError('No wallet provided')
        return self._wallet

    @wallet.setter
    def wallet(self, wallet):
        if issubclass(type(wallet), BaseWallet):
            self._wallet = wallet
        else:
            raise InvalidWalletError(f'Wrong wallet class: {type(wallet).__name__}. \
                                       Must be one of the BaseWallet subclasses')

    def __init_contracts_info(self):
        for contract_info in CONTRACTS_INFO:
            self.__add_contract_info(contract_info)

    def __add_contract_info(self, contract_info):
        self.__contracts_info[contract_info.name] = contract_info

    def __init_contracts(self):
        self.add_lib_contract('contract_manager', contracts.ContractManager)
        for name in self.__contracts_info:
            info = self.__contracts_info[name]
            if info.upgradeable:
                self.init_upgradeable_contract(info)
            else:
                self.add_lib_contract(info.name, info.contract_class)

    def init_upgradeable_contract(self, contract_info):
        address = self.get_contract_address(contract_info.contract_name)
        self.add_lib_contract(contract_info.name, contract_info.contract_class,
                              address)

    def add_lib_contract(self, name, contract_class, contract_address=None):
        address = contract_address or self.get_contract_address_by_name(
            self.abi, name)
        logger.info(f'Initialized: {name} at {address}')
        abi = self.get_contract_abi_by_name(self.abi, name)
        self.add_contract(name, contract_class(self, name, address, abi))

    def get_contract_address_by_name(self, abi, name):
        return abi.get(f'skale_{name}_address') or abi.get(f'{name}_address')

    def get_contract_abi_by_name(self, abi, name):  # todo: unify abi key names
        return abi.get(f'skale_{name}_abi') or abi.get(
            f'{name}_abi') or abi.get(f'{name}_functionality_abi') or abi.get(
            f'{name}_data_abi')

    def add_contract(self, name, skale_contract):
        logger.debug(f'Init contract: {name}')
        self.__contracts[name] = skale_contract

    def get_contract_address(self, name):
        return self.contract_manager.get_contract_address(name)

    def get_contract_by_name(self, name):
        return self.__contracts[name]

    def __getattr__(self, name):
        if name not in self.__contracts:
            return None
        return self.get_contract_by_name(name)
