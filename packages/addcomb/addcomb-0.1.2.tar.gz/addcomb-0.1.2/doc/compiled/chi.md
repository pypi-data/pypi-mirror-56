The _chi_ function is defined so that _chi(G, h)_ is the smallest _m_ for which every _m_ size subset of _G_ spans _G_.

ARGUMENTS:

* G - Either an integer _n_ (representing G = Z\_n) or a tuple _(n1, n2, ..., nm)_ (representing G = Z\_n1 * Z\_n2 * ... * Z\_nm)

* h - An integer

* (optional) verbose \[default: False\] - Print extra computational information
This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.