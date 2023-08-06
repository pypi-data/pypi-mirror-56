import numpy as np
from typing import Union, Tuple

from ..config import NP_COMPLEX
from .transfermatrix import PairwiseUnitary


class MZI(PairwiseUnitary):
    """Mach-Zehnder Interferometer

    Class simulating the scattering matrix formulation of an ideal phase-shifting Mach-Zehnder interferometer.
    This can implement any :math:`2 \\times 2` unitary operator :math:`U_2 \in \mathrm{U}(2)`.

    The internal phase shifts, :math:`\\theta_1, \\theta_2`, and the external phase shifts :math:`\phi_1, \phi_2`, are
    used to define the final unitary operator as follows (where we define :math:`\\theta := \\theta_1- \\theta_2`
    for convenience):

    In Hadamard convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = H L(\\theta_1) R(\\theta_2) H L(\\phi_1) R(\\phi_2) = e^{i\\frac{\\theta_1 + \\theta_2}{2}}
        \\begin{bmatrix} e^{i \phi_1}\cos \\frac{\\theta}{2} & ie^{i \phi_2}\sin \\frac{\\theta}{2} \\\\
        ie^{i \phi_1}\sin \\frac{\\theta}{2} & e^{i \phi_2}\cos \\frac{\\theta}{2} \\end{bmatrix}

    In beamsplitter convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = B L(\\theta_1) R(\\theta_2) B L(\\phi_1) R(\\phi_2) = i e^{i\\frac{\\theta_1 + \\theta_2}{2}}
        \\begin{bmatrix} e^{i \phi_1}\sin \\frac{\\theta}{2} & e^{i \phi_2}\cos \\frac{\\theta}{2} \\\\
        e^{i \phi_1}\cos \\frac{\\theta}{2} & -e^{i \phi_2}\sin \\frac{\\theta}{2} \\end{bmatrix}

    Args:
        internal_upper: Upper internal phase shift
        internal_lower: Lower internal phase shift
        external_upper: Upper external phase shift
        external_lower: Lower external phase shift
        hadamard: Whether to use Hadamard convention
        epsilon: Beamsplitter error
        dtype: Type-casting to use for the matrix elements
    """

    def __init__(self, internal_upper: float, internal_lower: float, external_upper: float, external_lower: float,
                 hadamard: bool, epsilon: Union[float, Tuple[float, float]] = 0.0, dtype=NP_COMPLEX):
        super(MZI, self).__init__(dtype=dtype)
        self.internal_upper = internal_upper
        self.internal_lower = internal_lower
        self.external_upper = external_upper
        self.external_lower = external_lower
        self.hadamard = hadamard
        self.epsilon = (epsilon, epsilon) if isinstance(epsilon, float) or isinstance(epsilon, int) else epsilon

    @property
    def reflectivity(self):
        return np.cos(self.internal_upper - self.internal_lower) ** 2

    @property
    def transmissivity(self):
        return np.sin(self.internal_upper - self.internal_lower) ** 2

    @property
    def matrix(self):
        return get_mzi_transfer_matrix(
            internal_upper=self.internal_upper,
            internal_lower=self.internal_lower,
            external_upper=self.external_upper,
            external_lower=self.external_lower,
            epsilon=self.epsilon,
            hadamard=self.hadamard,
            dtype=self.dtype
        )


class SMMZI(MZI):
    """Mach-Zehnder Interferometer (single-mode basis)

    Class simulating an ideal phase-shifting Mach-Zehnder interferometer.
    As usual in our simulation environment, we have :math:`\\theta \in [0, \pi]` and :math:`\phi \in [0, 2\pi)`.

    In Hadamard convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = H L(\\theta) H L(\phi) = e^{-i \\theta / 2}
        \\begin{bmatrix} e^{i \phi}\cos \\frac{\\theta}{2} & i\sin \\frac{\\theta}{2} \\\\
        ie^{i \phi}\sin \\frac{\\theta}{2} & \cos \\frac{\\theta}{2} \\end{bmatrix}

    In beamsplitter convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = B L(\\theta) B L(\phi) = ie^{-i \\theta / 2}
        \\begin{bmatrix} e^{i \phi}\sin \\frac{\\theta}{2} & \cos \\frac{\\theta}{2} \\\\
        e^{i \phi}\cos \\frac{\\theta}{2} & -\sin \\frac{\\theta}{2} \\end{bmatrix}

    Args:
        theta: Amplitude-modulating phase shift
        phi: External phase shift,
        hadamard: Whether to use Hadamard convention
        epsilon: Beamsplitter error
        dtype: Type-casting to use for the matrix elements
    """

    def __init__(self, theta: float, phi: float, hadamard: bool,
                 epsilon: Union[float, Tuple[float, float]] = 0.0, dtype=NP_COMPLEX):
        self.theta = theta
        self.phi = phi
        super(SMMZI, self).__init__(
            internal_upper=theta,
            internal_lower=0,
            external_upper=phi,
            external_lower=0,
            epsilon=epsilon,
            hadamard=hadamard,
            dtype=dtype
        )


class BlochMZI(MZI):
    """Mach-Zehnder Interferometer (Bloch basis, named after the Bloch sphere qubit formula)

    Class simulating an ideal phase-shifting Mach-Zehnder interferometer.
    As usual in our simulation environment, we have :math:`\\theta \in [0, \pi]` and :math:`\phi \in [0, 2\pi)`.

    In Hadamard convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = H D(\\theta) H L(\phi) =
        \\begin{bmatrix} e^{i \phi}\cos \\frac{\\theta}{2} & i\sin \\frac{\\theta}{2} \\\\
        ie^{i \phi}\sin \\frac{\\theta}{2} & \cos \\frac{\\theta}{2} \\end{bmatrix}

    In beamsplitter convention, the corresponding transfer matrix is:

    .. math::
        U_2(\\theta, \phi) = B D(\\theta) B L(\phi) = i
        \\begin{bmatrix} e^{i \phi}\sin \\frac{\\theta}{2} & \cos \\frac{\\theta}{2} \\\\
        e^{i \phi}\cos \\frac{\\theta}{2} & -\sin \\frac{\\theta}{2} \\end{bmatrix}

    Args:
        theta: Amplitude-modulating phase shift
        phi: External phase shift,
        hadamard: Whether to use Hadamard convention
        epsilon: Beamsplitter error
        dtype: Type-casting to use for the matrix elements
    """

    def __init__(self, theta: float, phi: float, hadamard: bool,
                 epsilon: Union[float, Tuple[float, float]] = 0.0, dtype=NP_COMPLEX):
        self.theta = theta
        self.phi = phi
        super(BlochMZI, self).__init__(
            internal_upper=theta / 2,
            internal_lower=-theta / 2,
            external_upper=phi,
            external_lower=0,
            epsilon=epsilon,
            hadamard=hadamard,
            dtype=dtype
        )


def get_mzi_transfer_matrix(internal_upper: float, internal_lower: float, external_upper: float, external_lower: float,
                            hadamard: float, epsilon: Tuple[float, float], dtype) -> np.ndarray:
    """

    Args:
        internal_upper: Upper internal phase shift
        internal_lower: Lower internal phase shift
        external_upper: Upper external phase shift
        external_lower: Lower external phase shift
        hadamard: Whether to use Hadamard convention
        epsilon: Beamsplitter error
        dtype: Type-casting to use for the matrix elements

    Returns:
        MZI transfer matrix

    """
    epp = np.sqrt(1 + epsilon[0]) * np.sqrt(1 + epsilon[1])
    epn = np.sqrt(1 + epsilon[0]) * np.sqrt(1 - epsilon[1])
    enp = np.sqrt(1 - epsilon[0]) * np.sqrt(1 + epsilon[1])
    enn = np.sqrt(1 - epsilon[0]) * np.sqrt(1 - epsilon[1])
    iu, il, eu, el = internal_upper, internal_lower, external_upper, external_lower
    if hadamard:
        return 0.5 * np.array([
            [(epp * np.exp(1j * iu) + enn * np.exp(1j * il)) * np.exp(1j * eu),
             (epn * np.exp(1j * iu) - enp * np.exp(1j * il)) * np.exp(1j * el)],
            [(enp * np.exp(1j * iu) - epn * np.exp(1j * il)) * np.exp(1j * eu),
             (enn * np.exp(1j * iu) + epp * np.exp(1j * il)) * np.exp(1j * el)]
        ], dtype=dtype)
    else:
        return 0.5 * np.array([
            [(epp * np.exp(1j * iu) - enn * np.exp(1j * il)) * np.exp(1j * eu),
             1j * (epn * np.exp(1j * iu) + enp * np.exp(1j * il)) * np.exp(1j * el)],
            [1j * (enp * np.exp(1j * iu) + epn * np.exp(1j * il)) * np.exp(1j * eu),
             -(enn * np.exp(1j * iu) - epp * np.exp(1j * il)) * np.exp(1j * el)]
        ], dtype=dtype)
