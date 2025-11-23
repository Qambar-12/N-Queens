tests = [
    {'N':8, 'seed': 1, 'name': '8_seed1'},
    {'N':16, 'seed': 1, 'name': '16_seed1'},
    {'N':32, 'seed': 1, 'name': '32_seed1'},
    {'N':8, 'seed': 5, 'name': '8_seed5'},
    {'N':16, 'seed': 5, 'name': '16_seed5'},
    {'N':32, 'seed': 5, 'name': '32_seed5'},
    {'N':8, 'seed': 12, 'name': '8_seed12'},
    {'N':16, 'seed': 12, 'name': '16_seed12'},
    {'N':32, 'seed': 12, 'name': '32_seed12'},
    {'N':8, 'seed': 14, 'name': '8_seed14'},
    {'N':16, 'seed': 14, 'name': '16_seed14'},
    {'N':32, 'seed': 14, 'name': '32_seed14'},
]
results = []
for test in tests:
    N = test['N']
    seed = test['seed']
    bo = Board(N, seed)
    ls = LocalSearch(bo)
    ls_sol, ls_stats = ls.local_search_auto(seed=seed)
    csp = CSP(bo)
    csp_sol, csp_stats = csp.csp_auto(time_limit=30.0)
    results.append({
    'test': test['name'],
    'N': N,
    'seed': seed,
    'ls_success': ls_stats['success'],
    'ls_steps': ls_stats['steps'],
    'ls_runtime': ls_stats['runtime'],
    'csp_success': csp_stats['success'],
    'csp_steps': csp_stats['steps'],
    'csp_runtime': csp_stats['runtime'],
     })



results_df = pd.DataFrame(results)
results_df

