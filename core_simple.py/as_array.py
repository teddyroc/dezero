def as_array(x):
    if np.isscalar(x):
        x = np.array(x)
    return x