import pywt

ahaar = pywt.Wavelet(name="Average Haar",
                     filter_bank=[[0.5, 0.5], [-0.5, 0.5],
                                  [1, 1], [1, -1]])

uhaar = pywt.Wavelet(name="Unnormalized Haar",
                     filter_bank=[[1, 1], [-1, 1],
                                  [0.5, 0.5], [0.5, -0.5]])


def wavelet_grad_thresholds(shape, levels):
    x = np.random.normal(size=shape)
    norm_grad = normalized_gradient(x)
    coeffs = pywt.swtn(norm_grad, ahaar, levels, axes=(-2, -1))
    for coeff in coeffs:
        for key, value in coeff.items():
            coeff[key] = Empiric_RV(np.linalg.norm(value, axis=0))

    return coeffs


def wavelet_grad(grad, levels, t, thresholds, tree=False):
    coeffs = pywt.swtn(grad, ahaar, levels, axes=(-2, -1))
    for i, coeff in enumerate(reversed(coeffs)):
        # Tree pruning
        if i > 0 and tree:
            condA = pywt.swtn(condA, uhaar, 1, start_level=i)[0]['aa'] == 4
        else:
            condA = True
        for key, value in coeff.items():
            norm = np.linalg.norm(value, axis=0)
            cond = norm < thresholds[::-1][i][key].ppf(t)
            value[:, cond & condA] = 0  # Thresholding
            if key == 'aa':
                save_cond = cond
        else:
            condA &= save_cond
    grad_rec = pywt.iswtn(coeffs, ahaar, axes=(-2, -1))
    return grad_rec


def smo_advanced(im, levels, t, thresholds, tree=False):
    norm_grad = normalized_gradient(im)
    grad_rec = wavelet_grad(norm_grad, levels, t, thresholds, tree=tree)
    return np.linalg.norm(grad_rec, axis=0)