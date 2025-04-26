# Compare theoretical and numerical amplitude over frequencies
freqs = [1.0, 1.5, 2.0, 2.25, 2.5, 3.0]  # Hz
results = []
for f in freqs:
    omega = 2*np.pi*f
    state = np.zeros(8)
    # simulate symmetric forcing at each freq
    for i in range(n_steps):
        state = rk4_step(derivatives, state, i*dt, dt, F0, omega)
    # take max displacement after 80% of simulation to approximate steady-state amplitude
    sol = np.zeros(n_steps+1)
    # (reuse sol array for brevity)
    state = np.zeros(8)
    for i in range(n_steps):
        state = rk4_step(derivatives, state, i*dt, dt, F0, omega)
        sol[i+1] = state[0]
    amp_num = np.max(np.abs(sol[int(n_steps*0.8):]))
    # theoretical amplitude (single-DOF formula)
    A_theo = F0/np.sqrt((k0 - m*omega**2)**2 + (c0*omega)**2)
    results.append((f, A_theo, amp_num))
# Print results
print("Freq (Hz)  A_theo (m)  A_num (m)  RelError")
for f, A_t, A_n in results:
    rel = (A_n - A_t)/A_t if A_t!=0 else 0
    print(f"{f:6.2f}   {A_t:7.3f}     {A_n:7.3f}   {rel:6.3%}")