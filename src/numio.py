"""
models of numio
"""

import global_vars


class NumioHandle:
    """
    class for handling numio
    """

    def __init__(
        self,
    ):
        pass

    def generate_command(self) -> bytes:
        """
        get corresponding command for this
        instance of numio handle
        """
        return (
            # global_vars.SRUN_PATH + "-m iter=1000,size=1000,pert=2"
            "hostname"
        ).encode()
