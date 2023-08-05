The _mu_ function is defined so that _mu(G, k, l)_ is the maximum size of a set _A_ such that _kA_ is disjoint from _lA_.

ARGUMENTS:

* G - Either an integer _n_ (representing G = Z\_n) or a tuple _(n1, n2, ..., nm)_ (representing G = Z\_n1 * Z\_n2 * ... * Z\_nm)

* k - An integer

* l - An integer

* (optional) verbose \[default: False\] - Print extra information
This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.