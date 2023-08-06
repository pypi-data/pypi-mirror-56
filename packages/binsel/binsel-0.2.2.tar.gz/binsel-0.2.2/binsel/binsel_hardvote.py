from .bootstrap_solutions import bootstrap_solutions
from .enumerate_negations import enumerate_negations
import numpy as np
from .negate_bool_features import negate_bool_features
from .hard_voting import hard_voting
from korr import confusion, confusion_to_mcc


def binsel_hardvote(X: np.array,
                    y: np.array,
                    n_select: int = 5,
                    max_rho: float = 0.4,
                    preselect: float = None,
                    n_draws: int = 50,
                    subsample: float = 0.7,
                    replace: bool = False,
                    random_state: int = 42,
                    unique: bool = True,
                    oob_score: bool = True,
                    verbose: bool = False) -> (list, list, float, list):
    # bootstrap some possible solutions
    solutions, oob = bootstrap_solutions(
        X, y=y, n_select=n_select, max_rho=max_rho,
        preselect=preselect, n_draws=n_draws,
        subsample=subsample, replace=replace,
        random_state=random_state, unique=unique,
        verbose=verbose)

    # find best way to negate features and store evaluation
    results = []
    for i, indicies in enumerate(solutions):
        # convert back to in-sample indicies
        rowidx = list(set(range(len(X))) - set(oob[i]))
        # fit negations based on in-sample
        negate, rho = enumerate_negations(
            X[:, indicies][rowidx, :], y[rowidx])
        # re-evaluate with oob
        if oob_score:
            Xtmp = negate_bool_features(X[:, indicies][oob[i], :], negate)
            Yvote = hard_voting(Xtmp)
            rho = confusion_to_mcc(confusion(y[oob[i]], Yvote))
        # save it
        results.append([tuple(indicies), negate, rho])

    # order results
    results = np.array(results)
    idx_sorted = np.flip(np.argsort(results[:, 2]))
    results = results[idx_sorted]

    # done
    results = results.tolist()
    idx, neg, rho = results[0]
    return idx, neg, rho, results
