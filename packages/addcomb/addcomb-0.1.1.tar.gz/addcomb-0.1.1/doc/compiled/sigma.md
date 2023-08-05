The _sigma_ function is defined so that _sigma(G, h)_ is the maximum size of a sidon set_ of _G_. A sidon set is defined precisely in Chapter C of Bela's book.

ARGUMENTS:

* G - Either an integer _n_ (representing G = Z\_n) or a tuple _(n1, n2, ..., nm)_ (representing G = Z\_n1 * Z\_n2 * ... * Z\_nm)

* h - An integer

* (optional) verbose \[default: False\] - Print a sidon set _A_ of size _sigma(G, h)_
This function uses the _unsigned_, _unrestricted_ variation of sumsets. This means that in the sumset, terms are allowed to repeat and are not allowed to be subtracted. For more information, read the (link forthcoming) master page of details on sumsets.