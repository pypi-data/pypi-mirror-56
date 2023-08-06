"""Generated wrapper for StaticCallProxy Solidity contract."""

# pylint: disable=too-many-arguments

import json
from typing import (  # pylint: disable=unused-import
    Any,
    List,
    Optional,
    Tuple,
    Union,
)

from eth_utils import to_checksum_address
from mypy_extensions import TypedDict  # pylint: disable=unused-import
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractFunction
from web3.datastructures import AttributeDict
from web3.providers.base import BaseProvider

from zero_ex.contract_wrappers.bases import ContractMethod, Validator
from zero_ex.contract_wrappers.tx_params import TxParams


# Try to import a custom validator class definition; if there isn't one,
# declare one that we can instantiate for the default argument to the
# constructor for StaticCallProxy below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        StaticCallProxyValidator,
    )
except ImportError:

    class StaticCallProxyValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


class TransferFromMethod(ContractMethod):
    """Various interfaces to the transferFrom method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self._underlying_method = contract_function

    def validate_and_normalize_inputs(
        self, asset_data: bytes, _from: str, to: str, amount: int
    ):
        """Validate the inputs to the transferFrom method."""
        self.validator.assert_valid(
            method_name="transferFrom",
            parameter_name="assetData",
            argument_value=asset_data,
        )
        asset_data = bytes.fromhex(asset_data.decode("utf-8"))
        self.validator.assert_valid(
            method_name="transferFrom",
            parameter_name="from",
            argument_value=_from,
        )
        _from = self.validate_and_checksum_address(_from)
        self.validator.assert_valid(
            method_name="transferFrom", parameter_name="to", argument_value=to,
        )
        to = self.validate_and_checksum_address(to)
        self.validator.assert_valid(
            method_name="transferFrom",
            parameter_name="amount",
            argument_value=amount,
        )
        # safeguard against fractional inputs
        amount = int(amount)
        return (asset_data, _from, to, amount)

    def call(
        self,
        asset_data: bytes,
        _from: str,
        to: str,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> None:
        """Execute underlying contract method via eth_call.

        Makes a staticcall to a target address and verifies that the data
        returned matches the expected return data.

        :param amount: This value is ignored.
        :param assetData: Byte array encoded with staticCallTarget,
            staticCallData, and expectedCallResultHash
        :param from: This value is ignored.
        :param to: This value is ignored.
        :param tx_params: transaction parameters

        """
        (asset_data, _from, to, amount) = self.validate_and_normalize_inputs(
            asset_data, _from, to, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method(asset_data, _from, to, amount).call(
            tx_params.as_dict()
        )

    def send_transaction(
        self,
        asset_data: bytes,
        _from: str,
        to: str,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Makes a staticcall to a target address and verifies that the data
        returned matches the expected return data.

        :param amount: This value is ignored.
        :param assetData: Byte array encoded with staticCallTarget,
            staticCallData, and expectedCallResultHash
        :param from: This value is ignored.
        :param to: This value is ignored.
        :param tx_params: transaction parameters

        """
        (asset_data, _from, to, amount) = self.validate_and_normalize_inputs(
            asset_data, _from, to, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method(asset_data, _from, to, amount).transact(
            tx_params.as_dict()
        )

    def estimate_gas(
        self,
        asset_data: bytes,
        _from: str,
        to: str,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> int:
        """Estimate gas consumption of method call."""
        (asset_data, _from, to, amount) = self.validate_and_normalize_inputs(
            asset_data, _from, to, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method(
            asset_data, _from, to, amount
        ).estimateGas(tx_params.as_dict())

    def build_transaction(
        self,
        asset_data: bytes,
        _from: str,
        to: str,
        amount: int,
        tx_params: Optional[TxParams] = None,
    ) -> dict:
        """Construct calldata to be used as input to the method."""
        (asset_data, _from, to, amount) = self.validate_and_normalize_inputs(
            asset_data, _from, to, amount
        )
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method(
            asset_data, _from, to, amount
        ).buildTransaction(tx_params.as_dict())


class GetProxyIdMethod(ContractMethod):
    """Various interfaces to the getProxyId method."""

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(provider, contract_address, validator)
        self._underlying_method = contract_function

    def call(self, tx_params: Optional[TxParams] = None) -> bytes:
        """Execute underlying contract method via eth_call.

        Gets the proxy id associated with the proxy address.

        :param tx_params: transaction parameters
        :returns: Proxy id.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method().call(tx_params.as_dict())

    def send_transaction(
        self, tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Gets the proxy id associated with the proxy address.

        :param tx_params: transaction parameters
        :returns: Proxy id.
        """
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method().transact(tx_params.as_dict())

    def estimate_gas(self, tx_params: Optional[TxParams] = None) -> int:
        """Estimate gas consumption of method call."""
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method().estimateGas(tx_params.as_dict())

    def build_transaction(self, tx_params: Optional[TxParams] = None) -> dict:
        """Construct calldata to be used as input to the method."""
        tx_params = super().normalize_tx_params(tx_params)
        return self._underlying_method().buildTransaction(tx_params.as_dict())


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class StaticCallProxy:
    """Wrapper class for StaticCallProxy Solidity contract.

    All method parameters of type `bytes`:code: should be encoded as UTF-8,
    which can be accomplished via `str.encode("utf_8")`:code:.
    """

    transfer_from: TransferFromMethod
    """Constructor-initialized instance of
    :class:`TransferFromMethod`.
    """

    get_proxy_id: GetProxyIdMethod
    """Constructor-initialized instance of
    :class:`GetProxyIdMethod`.
    """

    def __init__(
        self,
        provider: BaseProvider,
        contract_address: str,
        validator: StaticCallProxyValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        self.contract_address = contract_address

        if not validator:
            validator = StaticCallProxyValidator(provider, contract_address)

        self._web3_eth = Web3(  # type: ignore # pylint: disable=no-member
            provider
        ).eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address),
            abi=StaticCallProxy.abi(),
        ).functions

        self.transfer_from = TransferFromMethod(
            provider, contract_address, functions.transferFrom, validator
        )

        self.get_proxy_id = GetProxyIdMethod(
            provider, contract_address, functions.getProxyId, validator
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"name":"assetData","type":"bytes"},{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getProxyId","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"pure","type":"function"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
