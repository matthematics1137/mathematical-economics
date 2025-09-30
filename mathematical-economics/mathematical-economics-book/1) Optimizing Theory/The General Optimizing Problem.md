# terms 
- some concepts we should cover before getting into the meat of the subject
- generally we have some kind of **social objective** like growth we want to **optimize** by maximizing its value, under certain real world **constraints** or limitations. 
	- we consider this optimization under different **growth paths** trying to find the most efficient ones which allow us to maximize a given variable without too negatively effecting others that are at odds (growth v welfare etc)
		- this is done through different kind of economic models which could be **active** where agents respond to data or **passive** where we let the system run

## optimization
- **optimization** - catch all term for maximizing, minimizing, or finding a saddle point 
	- a **decision maker** (individual, firm, gvt) chooses values of some variables to maximize / minimize an *objective function*, subject to some constraint(s)
		- **objective function** - what we are optimizing for 
		- **choice variables** - what can be adjusted 
		- **constraints** - what we cant adjust (limits imposed by reality)
- mathematically:
	- $max_{x \in X}$, $f(x)$ $s.t.$ $g(x) \leq b$ 

## passive vs active economic models 
- **passive model** - the system evolves automatically according to constraints once conditions are set (ex solow growth model)
- **active model** - system with *agents* that make *choices* in order to optimize
	- policy instruments or control variables are actively adjusted to steer outputs 
	- ex ramsey growth model

## efficient growth paths 
- **path** - a time sequence of variables (consumption $c_t$, capital $k_t$)
	- an **efficient** growth path is one where you cannot reallocate resources to make one agent better off without making another worse off 
		- *dynamic extension of pareto efficiency* 

## optimal policy models 
- generally here we have a **social objective (welfare, stability, growth)** trying to be optimized by an agent (government, planner, etc)
	- *control variables* = policy instruments (taxes)
	- *state variables* = economic stocks (capital, debt)
	- *problem* = maximize social welfare given constraints
	- leads into **optimal control theory** ⭐

# the general structure
- to skip to the end we would say:
	- find $x^* \in k$ $s.t.$ $f(x^*) \geq f(x)$ for all $x \in k$ 
	- $k$ = **feasible set**
	- $f(x)$ = **objective function**
- basically this means we have some variable (growth, employment, etc) that we want to find the maximum value of, and to ground things in reality we use a feasible set because it means we are limiting ourselves to things we can actually do, otherwise the function is unbounded and we could get mathematically correct answers that have no meaning in the real world 
	- our value here is called **weakly global** because we use $\geq$, we entertain the possibility that there are multiple *highest points* on this optimization curve 
		- **weak** - not unique
		- **global** - true for all $x \in k$ 
	- a stronger condition $>$ would imply both global (true for all) and that it is unique
	- generally we call $x$ which satisfies this optimization problem the **optimal solution**


- now, most calculus techniques cannot actually find a solution to this problem:
	- **local v global optima**
		- in first order we set derivatives = 0 to find *stationary points* to tell us where the slops is flat (candidates for minima/maxima)
		- the problem is this gives us only *local information*
			- not guaranteed to find the *global optimum* over the whole feasible set 
	- ⭐ now you may realize we could take all the local minima / maxima found and then order them to find the optimal solution, however, we will run into a few more problems:
		- **curse of dimensionality** - for a $n-dimensional$ system with $n-unknowns$ we have *infinitely many solutions*
		- **boundaries complicate things** - many optima lie *on the boundary* of the feasible set $k$, where derivative conditions will fail us (keep in mind for later❗)

