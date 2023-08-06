"""
When an inverse function needs to be estimated, the first step is to find
a detonable starting position. This includes a lower point, which is bellow the
lower bound of the density, an interior point for where density is guarantied
to be grater than zero, and an upper point, which is above the upper bound of
the density.
"""

def find_interior_point(
        distribution,
        parameters=None,
        cache=None,
        iterations=1000,
        retall=False,
        seed=None,
):
    """
    Find interior point of the distribution where forward evaluation is
    guarantied to have:
    ``fwd(lower) <= 0 < fwd(middle) < 1 <= fwd(upper)``.

    Args:
        distribution (Dist):
            Distribution to find interior on.
        parameters (Optional[Dict[Dist, numpy.ndarray]]):
            Parameters for the distribution.
        cache (Optional[Dict[Dist, numpy.ndarray]]):
            Memory cache for the location in the evaluation so far.
        iterations (int):
            The number of iterations allowed to be performed
        retall (bool):
            If provided, lower and upper bound which guaranties that
            ``distribution.fwd(lower) == 0`` and
            ``distribution.fwd(upper) == 1`` is returned as well.
        seed (Optional[int]):
            Fix random seed.

    Returns:
        lower (numpy.ndarray):
            Array of input guarantied to be a lower bound for the distribution.
        middle (numpy.ndarray):
            Array of input guarantied to be inside the interior of the
            distribution.
        upper (numpy.ndarray):
            Array of input guarantied to be an upper bound for the
            distribution.

    Example:
        >>> distribution = chaospy.MvNormal([1, 2, 3], numpy.eye(3)+.03)
        >>> midpoint, lower, upper = find_interior_point(
        ...     distribution, retall=True, seed=1234)
        >>> print(lower.T)
        [[-64. -64. -64.]]
        >>> print(midpoint.round(4).T)
        [[  0.6784 -33.7687 -19.0182]]
        >>> print(upper.T)
        [[16. 16. 16.]]
        >>> distribution = chaospy.Uniform(1000, 1010)
        >>> midpoint, lower, upper = find_interior_point(
        ...     distribution, retall=True, seed=1234)
        >>> print(lower.round(4))
        [[991.2541]]
        >>> print(midpoint.round(4))
        [[1008.4885]]
        >>> print(upper.round(4))
        [[1015.0737]]
    """
    random_state = numpy.random.get_state()
    numpy.random.seed(seed)

    def forward(x_data):
        return evaluation.evaluate_forward(
            distribution=distribution,
            x_data=x_data.reshape(-1, 1),
            parameters=parameters,
            cache=cache,
        ).flatten()

    lower = -numpy.ones(len(distribution))
    upper = numpy.ones(len(distribution))

    for _ in range(100):
        indices = forward(lower) > 0
        if not numpy.any(indices):
            break
        lower[indices] *= 2

    for _ in range(100):
        indices = forward(upper) < 1
        if not numpy.any(indices):
            break
        upper[indices] *= 2

    for _ in range(iterations):

        rand = numpy.random.random(len(distribution))
        proposal = rand*lower + (1-rand)*upper
        evals = forward(x_data=proposal)

        indices = forward(upper) < 1
        upper[indices] += rand[indices]*(upper[indices]-lower[indices])
        upper = numpy.where(evals >= 1, proposal, upper)

        indices = forward(lower) > 0
        lower[indices] += rand[indices]*(upper[indices]-lower[indices])
        lower = numpy.where(evals <= 0, proposal, lower)

        if numpy.all((evals > 0) & (evals < 1)):
            break

    else:
        raise evaluation.DependencyError(
            """Too many iterations required to find interior point.
%s %s %s""" % (lower.flatten(), proposal.flatten(), upper.flatten()))

    numpy.random.set_state(random_state)
    if retall:
        return (
            proposal.reshape(-1, 1),
            lower.reshape(-1, 1),
            upper.reshape(-1, 1),
        )
    return proposal.reshape(-1, 1)
