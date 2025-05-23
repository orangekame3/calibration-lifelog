from pydantic import BaseModel, Field
from .coupling import CouplingModel
from .qubit import QubitModel
from .system_info import SystemInfoModel


class ChipModel(BaseModel):
    """Data model for a chip.

    Attributes
    ----------
        chip_id (str): The chip ID. e.g. "chip1".
        size (int): The size of the chip.
        qubits (dict): The qubits of the chip.
        couplings (dict): The couplings of the chip.
        system_info (SystemInfo): The system information. e.g. {"created_at": "2021-01-01T00:00:00Z", "updated_at": "2021-01-01T00:00:00Z"}.

    """

    chip_id: str = Field(..., description="The chip ID")
    username: str = Field(..., description="The username of the user who created the chip")
    size: int = Field(..., description="The size of the chip")
    qubits: dict[str, QubitModel] = Field(..., description="The qubits of the chip")
    couplings: dict[str, CouplingModel] = Field(..., description="The couplings of the chip")
    installed_at: str = Field(..., description="The time when the system information was created")

    system_info: SystemInfoModel = Field(..., description="The system information")
