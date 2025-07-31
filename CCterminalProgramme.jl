using JuMP
using Cbc

m = Model(Cbc.Optimizer)

@variable(m, 0 <= x[1:7])


@constraint(m, 5000 == sum(x[i] for i in 1:7))
@constraint(m, 10000 <= 2.5*x[1] + 3*x[2])
@constraint(m, 2000 <= 0.3*x[3] + 90*x[4] + 96*x[5] + 0.4*x[6] + 0.6*x[7] <= 3000)
@constraint(m, 6000 <= 1.3*x[1] + 0.8*x[2] + 4*x[5] + 1.2*x[6] <= 8250)

optimize!(m)
status = termination_status(m)

value.(x)
