In this report we explain how we implemented our solution for the
Maximum Diversity Problem, why we calibrated the alpha parameter before
comparing algorithms, and what our experimental data say about the real
contribution of Tabu Search under fixed time limits.

# 1. Project Goals and Problem Context

We worked on the Maximum Diversity Problem, where we must choose exactly
p elements from a set of n candidates so that the total pairwise
distance inside the selected subset is as large as possible. We keep the
theoretical introduction short because the main value of this project is
not a generic description of metaheuristics, but the way we implemented
the algorithms, calibrated them, and interpreted the data that came out
of the experiments.

From the beginning, we focused on two practical questions. First, which
construction policy should we use for each algorithm, especially through
the alpha parameter in GRASP. Second, does adding Tabu Search really
improve the basic GRASP when both methods are forced to work with the
same wall-clock budget. These two questions shaped both the code and the
experimental pipeline, because they forced us to separate construction,
improvement, calibration, and final comparison very clearly.

We also knew that the value of alpha could not be discussed in
isolation. In our implementation, alpha controls how wide the restricted
candidate list becomes during construction. A low alpha makes the
construction more greedy, while a high alpha makes it more exploratory.
That decision matters because the quality of the starting solution
strongly affects the local search behavior, and we expected the effect
to be different for plain GRASP and for GRASP combined with Tabu Search.

For that reason, we treated calibration as part of the experiment itself
and not as a cosmetic tuning step. If we had compared both algorithms
with arbitrary parameter values, the final conclusion would have been
unreliable. A poor choice of alpha or tabu tenure can make an algorithm
look weaker than it actually is, so before drawing any conclusion we
first needed to identify settings that were genuinely suitable for each
method.

# 2. How We Organized the Repository

We organized the repository as a modular experimental project because we
wanted to keep the optimization logic separate from the experiment
logic. We placed data loading, solution handling, constructive search,
local improvement, time-controlled algorithm wrappers, and experiment
scripts in different modules so that we could change one part without
silently affecting the others. This helped us a lot when we had to debug
the algorithms and later explain what each component was doing.

  ----------------------------------------------------------------------------
  **Component**                **Purpose in the repository**
  ---------------------------- -----------------------------------------------
  structure/instance.py        Parses MDG benchmark instances and builds the
                               symmetric distance matrix.

  structure/solution.py        Stores the selected subset, objective value,
                               and incremental add/remove operations.

  constructives/cgrasp.py      Implements greedy-randomized construction
                               controlled by alpha.

  localsearch/lsbestimp.py     Applies exhaustive best-improvement swap search
                               until a local optimum is reached.

  localsearch/tabu_search.py   Applies memory-based swap search with FIFO
                               tenure and aspiration.

  algorithms/grasp_timed.py    Wrap the two final algorithms under a global
  and algorithms/grasp_ts.py   time budget.

  experiments/calibration.py   Drive calibration, final comparison, and export
  and                          of reproducible summaries.
  experiments/comparison.py    
  ----------------------------------------------------------------------------

We chose this structure because we wanted every stage of the project to
be inspectable. By reading the repository, it is easy to see where
instances are parsed, where solutions are updated, where construction
takes place, where the improvement phase is applied, and where
calibration and final comparison are executed. That separation was
useful not only for cleanliness, but also for reproducibility, because
the experiment scripts could import stable algorithm modules instead of
containing modified copies of the search procedures.

We also kept a small main entry point for demonstration and smoke
testing. It allowed us to launch a representative run quickly and verify
that the repository still behaved sensibly after code changes. However,
we did not use that entry point to support our conclusions. All the
claims in the report come from the dedicated calibration and comparison
scripts.

We paid special attention to instance loading because many later
computations depend on it. Instead of reading distances lazily, we built
a symmetric distance matrix as soon as we parsed each file. We did this
for two reasons. First, constant-time lookups are essential when the
algorithms evaluate many candidates and many swaps. Second, centralizing
the creation of the matrix in one module reduced the risk of subtle
inconsistencies between algorithms. Once the matrix was built, both
GRASP and GRASP plus Tabu Search were guaranteed to work on exactly the
same internal representation.

We were also careful not to duplicate algorithm code inside the
experiment scripts. The calibration script imports the same algorithm
modules that the comparison script later imports. This was an important
design decision because duplicated algorithm logic often drifts over
time and makes the final report hard to trust. By forcing both
experiment stages to use the same implementations, we made it easier to
argue that differences in the results came from parameter choices and
algorithm behavior, not from hidden discrepancies between scripts.

We also made a decision that later became essential for the write-up: we
exported the results systematically. We did not want the project to
depend on reading console output by hand, so we wrote calibration
summaries, per-configuration results, per-run data, and final comparison
outputs to CSV and JSON files. This made the project much easier to
analyse afterwards, and it also allowed us to generate spreadsheet
summaries without rerunning all the experiments. In practice, those
exported artifacts became the backbone of the report because they
preserved the evidence behind every table and conclusion.

Looking back, we think this organization was one of the strengths of the
project. We were not only trying to solve instances; we were trying to
produce a repository from which we could defend a conclusion. The
modular layout, the explicit parameter lists, the separate calibration
and comparison stages, and the machine-readable exports all helped us
turn the project into an experimental study rather than a loose
collection of scripts.

# 3. Key Implementation Decisions

## 3.1 Solution representation and incremental evaluation

We represented each solution as a Python dictionary with three main
fields: the selected subset, the current objective value, and the
instance itself. Inside that dictionary, we stored the selected nodes as
a set because we needed very frequent membership checks during
construction and neighborhood evaluation. We chose this representation
because it was simple enough to manipulate everywhere in the project
while still being efficient on the operations that mattered most.

We also decided very early that we could not afford to recompute the
full objective function from scratch after every tentative move. For
that reason, we implemented helper operations that update the objective
incrementally when a node is added or removed. This was one of the
practical choices that made the large-instance experiments feasible,
because both local search and Tabu Search evaluate many swaps and would
have become much slower with repeated full recomputation.

## 3.2 GRASP construction and alpha control

We implemented the constructive phase so that it starts from a random
first element and then expands the partial solution with a restricted
candidate list. We scored each candidate by its current marginal
contribution and used alpha to control how wide the restricted list
becomes. We also kept the special value alpha equal to minus one so that
we could test a random alpha per iteration against fixed alpha values.
This gave us a broader calibration space without changing the
construction logic itself.

We liked this design because it made the construction policy explicit.
When we later calibrated alpha, we knew that the measured effect really
came from the width of the restricted candidate list and not from some
hidden source of randomness elsewhere in the code.

## 3.3 Best-improvement local search

We implemented local search as exhaustive best improvement over the full
one-out one-in swap neighborhood. We chose this instead of a lighter
first-improvement variant because we wanted the baseline to be a serious
benchmark and not an intentionally weak version of GRASP. The cost of
this choice is that each restart becomes more expensive, but the benefit
is that every finished run ends in a genuine local optimum with respect
to the swap neighborhood. This later helped us interpret why low alpha
works well for the baseline on large instances.

## 3.4 Tabu Search and memory

We built the Tabu Search phase on top of the same swap neighborhood, but
we changed the movement rule by adding a FIFO tabu list and an
aspiration criterion. In our implementation, recently removed nodes
cannot re-enter immediately unless the move would improve the best
objective value found so far. We deliberately kept aspiration
conservative because we wanted memory to remain meaningful instead of
being bypassed too often.

We also recorded node frequencies even though we did not end up using
them for long-term diversification in the final version. We left that
information in place because it gave us room for future improvements
without changing the current comparison. In other words, our final Tabu
Search uses short-term memory only, but the code already preserves
information that could support a stronger diversification strategy
later.

## 3.5 Global time budgeting and reproducibility

We enforced a global wall-clock budget in both final algorithms. In the
GRASP baseline, we simply repeated construction and best-improvement
local search until time was exhausted. In the GRASP plus Tabu Search
variant, we passed the remaining time budget into each Tabu Search call.
We considered this essential because we wanted the comparison to be fair
in actual runtime, not in iteration counts.

We exported calibration results to CSV and JSON and made the comparison
script read those artifacts directly. This saved us from manual
parameter transcription and made the workflow much more reliable. Once
calibration finished, the final comparison automatically reused the
selected values, so we could be confident that the reported experiment
really corresponded to the tuned configuration.

We know that using a set for the selected nodes may look like a small
detail, but for us it became an important optimization. Membership is
queried constantly when we decide whether a node remains available as an
insertion candidate or already belongs to the current solution. A slower
representation would still be correct, but it would reduce the number of
restarts and neighborhood scans we could complete under the same time
budget. Since our whole comparison is based on equal runtime, those
data-structure decisions directly affect the quality of the experiment.

Our incremental treatment of the objective function plays the same role.
Instead of recalculating the whole pairwise sum after every tentative
move, we compute how much value is gained or lost relative to the
current subset. This makes each swap evaluation much cheaper and allows
us to keep the local search exhaustive where we wanted it to be
exhaustive. It also makes the code easier to interpret, because each
move is evaluated through its direct marginal effect.

We also made a conscious decision to choose the first node at random.
This avoids starting every restart from the same deterministic condition
and helps keep the construction phase genuinely stochastic. After that
first choice, alpha controls the width of the restricted candidate list.
We liked this design because it gives us a continuous spectrum between
greedier and more exploratory constructions, which later makes
calibration much more informative.

We want to stress again that exhaustive best-improvement local search
was a deliberate choice. It makes each restart slower than simpler
alternatives, but it also gives the baseline method more credibility. If
we had used a weak improver, we could not have interpreted the alpha
results confidently because a good construction might simply have been
compensating for a poor local search. By keeping the baseline local
improver reasonably strong, we made the later calibration and comparison
much easier to justify.

Our Tabu Search implementation is also conservative by design. We do not
override tabu status just because a move improves the current solution.
We only override it when the move improves the best solution seen so
far. That stricter aspiration rule helped us preserve the role of memory
and prevented the tabu mechanism from becoming too weak.

# 4. Difficulties We Encountered During Programming and Experimentation

One of the first practical difficulties we faced was making sure that
instance loading was completely reliable. Each input file gives
distances for undirected pairs, so when we built the matrix we had to be
certain that every value written into d\[u\]\[v\] was mirrored
immediately into d\[v\]\[u\]. A small asymmetry here would have
corrupted both construction and swap evaluation in a way that would be
very difficult to detect later. This is why we kept the parsing logic
concentrated in a single module and reused that matrix everywhere else.

In fact, during the first implementation attempts we ran into exactly
this kind of bug. We initially suspected the problem was in the local
search because some objective values looked inconsistent between
repeated runs, but after checking the code more carefully we found that
the real issue came from the distance structure itself. Once we verified
the symmetry of the matrix systematically, the rest of the behavior
became much more stable and much easier to debug.

A second difficulty was runtime control. The baseline GRASP and the
GRASP plus Tabu Search variant do not spend time in the same way. The
Tabu Search version can invest much more effort inside one restart, so
if we had assigned naive local budgets the comparison could have become
unfair very easily. We solved this by treating time as a global resource
and by passing the remaining time to the Tabu Search phase. This design
took more care than a simple fixed-loop implementation, but it was
necessary if we wanted the final comparison to answer the professor\'s
question honestly.

A third difficulty appeared during calibration. At first, the natural
idea was to test all alpha values against all tenure values for the
GRASP plus Tabu Search method. In practice, that produced too many
configurations once we combined instance groups, multiple runs, and
nontrivial time budgets. We therefore moved to a sequential calibration
strategy: first we fixed a reasonable anchor tenure and searched for
alpha, and then we fixed the best alpha and searched for tenure. This
reduced the computational burden while still giving us interpretable
results.

We also had some confusion at the beginning when interpreting the effect
of alpha. In a first intuitive reading, it was tempting to expect that
lower alpha would always be better because the construction would be
greedier. The experiments forced us to abandon that assumption. Once we
observed that GRASP plus Tabu Search preferred a very high alpha on the
large instances, we had to go back to the code and to the logs and think
more carefully about what the improvement phase was actually doing. That
moment was useful because it pushed us to formulate the
breadth-versus-depth conjecture instead of relying on a simplistic rule
of thumb.

We also had to make the experiments reproducible enough to compare runs
meaningfully. That was harder than it sounds, because once calibration
and comparison were split into different scripts, it became easy to lose
track of which parameters and seeds had actually been used. We solved
this in two ways: we paired the random seeds by run index, and we
exported the calibration output to JSON so that the final comparison
script could read the chosen parameters automatically. Without that
step, the project would have depended too much on manual bookkeeping.

Before moving to the calibration results, we should also mention three
additional implementation difficulties that became especially important
in the Tabu Search version. The first one was the tabu tenure dilemma.
We quickly saw that tenure could not be chosen casually. If we made the
tabu list too short, the search intensified too aggressively, revisited
very similar structures, and got stuck in narrow regions of the search
space. If we made tenure too long, the search over-diversified, blocked
too many potentially useful returns, and ended up damaging average
solution quality. This is exactly why we treated tenure as a real
calibration problem instead of a fixed constant.

The second difficulty was related to data structures in Python. In
theory, a tabu list sounds simple, but in practice we needed membership
checks to be cheap because they happen again and again during
neighborhood exploration. We considered several ways of representing the
tabu information, including treating it like a circular list and
combining it with dictionaries or set-like checks so that asking whether
a candidate was tabu would not consume too much execution time. In the
final code we kept the structure simple enough to remain readable, but
throughout the implementation we were very aware that a slow
tabu-membership test could waste a meaningful part of the runtime
budget.

The third difficulty was the time budget itself. Tabu Search does not
naturally stop just because it reaches a local optimum, so making it
stop exactly at 10 seconds during calibration or 30 seconds during the
final comparison required more care than the baseline GRASP. We had to
place explicit time checks inside the main while-loop so that the
algorithm would stop when the global wall-clock limit was exhausted.
Without those checks, the Tabu Search version could easily overrun the
assigned budget and make the comparison unfair.

All these difficulties affected how we interpreted the experiments as
well as how we wrote the code. The tenure dilemma helped us understand
why intermediate memory depth worked better than extreme settings. The
Python data-structure issue reminded us that runtime-limited experiments
depend on implementation efficiency and not only on high-level algorithm
design. The time-budget issue reinforced the same lesson from another
angle: if we wanted to answer honestly whether Tabu Search improved
GRASP under equal limits, then respecting those limits in the code was
just as important as designing the search itself.

# 5. Calibration of Alpha and Tabu Tenure

We calibrated the parameters because we did not want the final
comparison to be biased by arbitrary choices. In our case, calibration
was especially important because the two algorithms do not exploit
construction quality in the same way. We therefore calibrated the GRASP
baseline directly and calibrated GRASP plus Tabu Search sequentially in
alpha and tenure.

We treated small and large instances separately because we expected the
role of parameters to change with scale. This turned out to be the right
choice. The small instances saturate quickly and mainly work as a
consistency check, while the large instances preserve enough difficulty
for alpha and tenure to have a visible and meaningful effect.

  -------------------------------------------------------------------
  **Experimental       **Calibration stage**  **Final comparison
  setting**                                   stage**
  -------------------- ---------------------- -----------------------
  Time budget per run  10 seconds             30 seconds

  Runs per             3                      5
  configuration or                            
  instance                                    

  Group treatment      Small and large        Group-specific
                       calibrated separately  calibrated parameters
                                              reused

  Statistical logic    Configuration ranking  Paired seeds plus
                       by average deviation   Wilcoxon signed-rank
                                              test
  -------------------------------------------------------------------

  --------------------------------------------------------------------------
  **Group**    **Algorithm**   **Selected   **Selected   **Best avg dev% in
                               alpha**      tenure**     calibration**
  ------------ --------------- ------------ ------------ -------------------
  Small        GRASP           0.1          \-           0.0000

  Small        GRASP+TS        0.25         15           0.0000

  Large        GRASP           0.1          \-           0.2536

  Large        GRASP+TS        0.9          10           0.0906
  --------------------------------------------------------------------------

Our most important calibration result is that the large instances push
the two algorithms toward opposite alpha values. Plain GRASP prefers
alpha = 0.1, while GRASP plus Tabu Search prefers alpha = 0.9 and tenure
= 10. We interpret this as a real structural effect rather than as
noise. When the improvement phase is weaker and purely improving, it is
better to start from a strong solution. When the improvement phase is
stronger and can escape worse regions, broader and more random starts
become more useful.

We are aware that a full joint calibration over alpha and tenure would
be more exhaustive in principle, but in practice it would also be much
more expensive. We therefore accepted the sequential strategy as a
compromise between thoroughness and runtime. Given the clarity of the
final trends, we think that choice was justified.

We find the small-instance calibration results interesting precisely
because they are almost flat. When nearly all parameter values produce
the same objective value and almost no variance, we should not pretend
that the selected setting encodes a deep truth about the algorithm. In
our case, the small-group parameters behave more like practical
defaults. The real story appears on the large instances.

When we look at the large group, we see that the baseline GRASP clearly
loses quality as alpha moves away from the greedy side of the spectrum.
We read this as evidence that our local search benefits from entering a
good basin quickly. In other words, once we use exhaustive
best-improvement local search, a strong construction matters a lot
because the algorithm has no deliberate mechanism to accept worsening
moves and escape a mediocre basin.

When we look at GRASP plus Tabu Search, the calibration moves in the
opposite direction, and for us this is one of the most interesting
results of the whole project. If both algorithms had preferred the same
alpha, calibration would still have been useful, but much less
revealing. The fact that the stronger improver prefers alpha 0.9
suggests that diversity in the starting solutions becomes valuable once
Tabu Search can intensify and repair them afterwards.

We also think the tenure result fits our observations. When tenure is
too short, the search can cycle too easily and memory loses value. When
tenure is too long, the search becomes too constrained and blocks moves
that could still be useful. The selected value of 10 on the large
instances seems to give the best balance between these two extremes.

# 6. Final Comparison: Did Tabu Search Improve GRASP?

Calibration alone could not answer the main question of the project.
After tuning the parameters, we still needed to test whether Tabu Search
actually improves the basic GRASP when both methods run under the same
time budget. For that reason, we carried out a separate final comparison
with equal runtime limits and paired seed indices.

We paired the seeds deliberately because stochastic algorithms can vary
a lot from run to run, and we wanted both methods to face comparable
random conditions. We then used the Wilcoxon signed-rank test because
the outcomes are paired and we did not want to rely on a normality
assumption that may not hold in this kind of experiment.

When we analyse the small instances, the answer is simple: Tabu Search
did not improve GRASP because GRASP already saturated the problem under
the available time budget. All 30 paired runs are exact ties. We
consider this an informative result rather than a disappointing one,
because it shows that once the instances are easy enough, the advanced
metaheuristic becomes redundant.

  ------------------------------------------------------------
  **Large-instance aggregate **GRASP**        **GRASP+TS**
  metric**                                    
  -------------------------- ---------------- ----------------
  Average deviation from the 0.5200%          0.8443%
  experiment best                             

  Mean within-instance       20.57            41.69
  standard deviation                          

  Instances reaching the     4/9              5/9
  experiment best at least                    
  once                                        

  Paired run wins            30               15

  Wilcoxon p-value           \-               0.002628
  ------------------------------------------------------------

When we analyse the large instances, our data show that Tabu Search did
not improve GRASP in average quality under the same 30-second budget.
The baseline GRASP achieves lower average deviation, lower variance, and
30 wins out of 45 paired runs. The Wilcoxon p-value of 0.002628 supports
that difference as statistically significant. So if the question is
whether the advanced metaheuristic improved the baseline in average
performance under equal time, our answer is no.

However, the answer is not simply that Tabu Search failed. What we saw
is more nuanced. GRASP plus Tabu Search reaches the experiment-best
value on more large instances than the baseline, which means that the
stronger improvement phase is capable of producing excellent peaks. The
problem is that it does so with much higher variance, and under a fixed
time budget that variance hurts the average result.

The instance MDG-a_5 shows the pattern clearly. In one run, GRASP plus
Tabu Search reaches the best observed value of 7755.23, but in several
other runs it falls far below that level, so the mean deteriorates
sharply. By contrast, on MDG-a_13 the Tabu Search variant can even beat
GRASP on average. We therefore do not think the correct interpretation
is a simplistic universal ranking. The result depends on whether we care
more about average quality or about occasional high peaks.

For us, this contrast between average quality and peak quality is one of
the most important results of the project. In practice, the preferred
algorithm depends on what kind of performance we value. If we care about
stable average results under a fixed budget, GRASP is better in our
experiments. If we care about the possibility of reaching especially
high values in some runs and we can tolerate instability, then GRASP
plus Tabu Search still has clear interest.

We also want to stress that the runtime budget is part of the
explanation, not just part of the protocol. Thirty seconds strongly
favors methods that can complete many competitive restarts. Under this
budget, the breadth of GRASP dominates. Under a longer budget, the
balance might shift because GRASP plus Tabu Search would have more
opportunities to combine deep exploitation with several independent
starts. Our conclusion is therefore specific to the time limits we
actually tested.

Using a paired nonparametric test was important for us because a few
spectacular runs can easily distort the intuitive reading of stochastic
results. By comparing matched runs with Wilcoxon, we checked whether the
direction of the differences was systematic. The significant result on
the large group confirms that the average advantage of GRASP is not just
an anecdotal impression.

# 7. Discussion: Our Breadth-versus-Depth Conjecture

The conjecture that best explains our results is what we call the
breadth-versus-depth trade-off. We use this expression because GRASP
spends less time on each restart and can therefore explore many more
construction-plus-local-search trajectories. That breadth stabilizes the
average quality and reduces sensitivity to unlucky starts. GRASP plus
Tabu Search does the opposite: it spends more time intensifying each
trajectory. That extra depth can produce better peaks, but it also
reduces the number of restarts completed under the same budget and
therefore increases variance.

The opposite alpha values we obtained during calibration fit this
conjecture very well. When the improvement phase is shallow and purely
improving, good starts matter more than diversification, so low alpha
works better. When the improvement phase is stronger and can recover
from weaker starts, diversified construction becomes valuable, so high
alpha works better. We see this as one of the strongest internal
consistencies of the project.

This also explains why we needed both calibration and final comparison.
Calibration prevents us from comparing poorly tuned versions of the
algorithms. Final comparison prevents us from treating isolated
successful runs as if they were enough to claim superiority. Together,
these two stages allowed us to defend a conclusion that is both
algorithmic and empirical.

We should also state the limitations of our study clearly. We only
worked with the benchmark instances available in the repository, we used
sequential calibration for Tabu Search instead of a full joint search
over alpha and tenure, and we defined the comparison reference
operationally as the best value observed in our own runs rather than as
an external literature optimum. These limitations do not cancel our
conclusions, but they do define their scope.

We also think a larger runtime budget could change the ranking. If GRASP
plus Tabu Search were allowed to complete more intensified restarts, its
stronger exploitation could eventually improve average quality as well.
For that reason, we do not present our conclusion as universal. We
present it as a conclusion tied to the time limits we actually tested.

We should add another limitation concerning the deviation measure
itself. In our experiments, the reference value is the best value
observed across the runs in the comparison, not an external best-known
value from the literature. We think this is acceptable for a controlled
internal comparison, but it is important to say it explicitly so that
the percentages are not overinterpreted.

We should also mention that the current implementation leaves several
natural extensions open. We could use the stored node frequencies for
long-term diversification, test a full joint calibration of alpha and
tenure, or try richer neighborhoods beyond the basic swap move. We
mention these options because they follow directly from the current
codebase. The project is complete enough to support a defended
conclusion, but it also leaves a clear path for future work.

# 8. Conclusion

We believe the repository supports a clear final conclusion. By
implementing both GRASP and GRASP plus Tabu Search in a modular way,
calibrating their parameters, and comparing them under the same time
limits, we were able to answer the main question of the project with
evidence instead of intuition. Under our 30-second budget, Tabu Search
did not improve basic GRASP in average quality on the large instances,
and on the small instances it was effectively redundant because GRASP
already reached the same results.

At the same time, we do not think the advanced metaheuristic was
useless. What our data suggest is that GRASP plus Tabu Search trades
average robustness for peak-seeking behavior. For short budgets and
stability-oriented use, we would choose the baseline GRASP. For settings
in which occasional very high values matter more than consistency, we
would still consider the Tabu Search variant a valuable option. That
breadth-versus-depth interpretation is, in our view, the most honest and
most interesting conclusion supported by our implementation and our
experiments.
