# Claim 1 evaluation

Verdict: **VERIFIED**

The implemented Wasserstein log-sum-exp energy equals an independently
evaluated expression exactly on the deterministic fixture. The analytic
mean gradient agrees with central finite differences to
`8.703970877377287e-11`, well inside the `1e-6` tolerance. All five
stored-pattern energies are within floating-point noise of zero and are
below the centroid energy `8.142790314124024`.

The sign-reversed-gradient negative control is rejected with maximum
absolute error `14.227561462768701`.

Evidence comes from immutable OpenResearch run
`4b824e0c-a9f3-4ace-b39c-706057da9992` at Git SHA
`3612f94158c9da860d7b09733266994176e098db`.
