from backend import *
from basement import *
#/ @title A facet of KittyCore that manages special access privileges.
#/ @author Axiom Zen (https://www.axiomzen.co)
#/ @dev See the KittyCore contract documentation to understand how the various contract facets are arranged.
class KittyAccessControl:
    # This facet controls access control for CryptoKitties. There are four roles managed here:
    #
    #     - The CEO: The CEO can reassign other roles and change the addresses of our dependent smart
    #         contracts. It is also the only role that can unpause the smart contract. It is initially
    #         set to the address that created the smart contract in the KittyCore constructor.
    #
    #     - The CFO: The CFO can withdraw funds from KittyCore and its auction contracts.
    #
    #     - The COO: The COO can release gen0 kitties to auction, and mint promo cats.
    #
    # It should be noted that these roles are distinct without overlap in their access abilities, the
    # abilities listed for each role above are exhaustive. In particular, while the CEO can assign any
    # address to any role, the CEO address itself doesn't have the ability to act in those roles. This
    # restriction is intentional so that we aren't tempted to use the CEO address frequently out of
    # convenience. The less we use an address, the less likely it is that we somehow compromise the
    # account.

    #/ @dev Emited when contract is upgraded - See README.md for updgrade plan
    def ContractUpgrade(newContract: address):
        # The addresses of the accounts (or contracts) that can execute actions within each roles.
        self._ceoAddress = None
        self._cfoAddress = None
        self._cooAddress = None
        # @dev Keeps track whether the contract is paused. When that is true, most actions are blocked
        self._paused = False

    @property
    def ceoAddress(self):
        return self._ceoAddress

    @ceoAddress.setter
    def ceoAddress(self, value):
        self._ceoAddress = value

    @property
    def cfoAddress(self):
        return self._cfoAddress

    @cfoAddress.setter
    def cfoAddress(self, value):
        self._cfoAddress = value

    @property
    def cooAddress(self):
        return self._cooAddress

    @cooAddress.setter
    def cooAddress(self, value):
        self._cooAddress = value

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, value):
        self._paused = value

    #/ @dev Assigns a new address to act as the CEO. Only available to the current CEO.
    #/ @param _newCEO The address of the new CEO
    @onlyCEO
    def setCEO(_newCEO: address):
        require(_newCEO != address(0))
        self.ceoAddress = _newCEO

    #/ @dev Assigns a new address to act as the CFO. Only available to the current CEO.
    #/ @param _newCFO The address of the new CFO
    @onlyCEO
    def setCFO(_newCFO: address):
        require(_newCFO != address(0))
        self.cfoAddress = _newCFO;

    #/ @dev Assigns a new address to act as the COO. Only available to the current CEO.
    #/ @param _newCOO The address of the new COO
    @onlyCEO
    def setCOO(_newCOO: address):
        require(_newCOO != address(0))
        self.cooAddress = _newCOO

    #/*** Pausable functionality adapted from OpenZeppelin ***/

    #/ @dev Called by any "C-level" role to pause the contract. Used only when
    #/  a bug or exploit is detected and we need to limit damage.
    @onlyCLevel
    @whenNotPaused
    def pause(self):
        self.paused = True;

    #/ @dev Unpauses the smart contract. Can only be called by the CEO, since
    #/  one reason we may pause the contract is when CFO or COO accounts are
    #/  compromised.
    #/ @notice This is public rather than external so it can be called by
    #/  derived contracts.
    @onlyCEO
    @whenPaused
    def unpause():
        # can't unpause if contract was upgraded
        self.paused = False
