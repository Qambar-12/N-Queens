#DRIVER CODE
def run_interface():
    N_slider = widgets.IntSlider(value=8, min=4, max=64, step=1, description='N:')
    seed_box = widgets.IntText(value=42, description='Seed:')

    auto_ls_btn = widgets.Button(description='Auto-Solve (Local Search)', button_style='success')
    step_ls_btn = widgets.Button(description='Step-Mode (Local Search)', button_style='info')
    auto_csp_btn = widgets.Button(description='Auto-Solve (CSP)', button_style='success')
    step_csp_btn = widgets.Button(description='Step-Mode (CSP)', button_style='info')

    next_btn = widgets.Button(description='Next Step', button_style='primary')
    reset_btn = widgets.Button(description='Reset', button_style='warning')

    output = widgets.Output()
    next_btn.layout.display = 'none'
    state = {'iterator': None, 'board_obj': None, 'mode': None}

    def show_initial(N, seed):
        with output:
            clear_output(wait=True)
            bo = Board(N, seed)
            print(f"Initial configuration (N={N}, seed={seed}):")
            bo.display_board(bo.board, "Initial Board")
            state['board_obj'] = bo

    show_initial(N_slider.value, seed_box.value)

    def on_auto_ls(_):
        with output:
            clear_output(wait=True)
            N = N_slider.value
            seed = seed_box.value
            bo = Board(N, seed)
            ls = LocalSearch(bo)
            state['board_obj'] = bo
            print(f"Initial (N={N}, seed={seed}):")
            bo.display_board(bo.board, "Initial Board")
            print("Running Local Search (auto)...")
            sol, stats = ls.local_search_auto(seed=seed)
            if sol:
                print(f"✅ Solution found in {stats['steps']} steps, restarts: {stats['restarts']}, time: {stats['runtime']:.6f}s")
                bo.display_board(sol, "Local Search Final Solution")
            else:
                print(f"❌ No solution found. Time: {stats.get('runtime', 0):.6f}s")
                bo.display_board(bo.board, "Final Board")

    def on_step_ls(_):
        with output:
            clear_output(wait=True)
            N = N_slider.value
            seed = seed_box.value
            bo = Board(N, seed)
            ls = LocalSearch(bo)
            state.update({'board_obj': bo, 'mode': 'ls', 'iterator': ls.local_search_step(seed=seed)})
            next_btn.layout.display = ''
            print(f"Step mode (Local Search) initialized (N={N}, seed={seed}).")
            bo.display_board(bo.board, "Initial Board")

    def on_auto_csp(_):
        with output:
            clear_output(wait=True)
            N = N_slider.value
            seed = seed_box.value
            bo = Board(N, seed)
            csp_obj = CSP(bo)
            state['board_obj'] = bo
            print(f"Initial (N={N}, seed={seed}):")
            bo.display_board(bo.board, "Initial Board")
            print("Running CSP (auto)...")
            sol, stats = csp_obj.csp_auto(time_limit=30.0)
            if sol:
                print(f"✅ CSP solution found in {stats['steps']} steps, time: {stats['runtime']:.6f}s")
                bo.display_board(sol, "CSP Final Solution")
            else:
                print(f"❌ No CSP solution found. Steps: {stats.get('steps', '?')}, time: {stats.get('runtime', 0):.6f}s")
                bo.display_board(bo.board, "CSP Final Board")

    def on_step_csp(_):
        with output:
            clear_output(wait=True)
            N = N_slider.value
            seed = seed_box.value
            bo = Board(N, seed)
            csp_obj = CSP(bo)
            state.update({'board_obj': bo, 'mode': 'csp', 'iterator': csp_obj.csp_step(time_limit=1000)})
            next_btn.layout.display = ''
            print(f"Step mode (CSP) initialized (N={N}, seed={seed}).")
            bo.display_board(bo.board, "Initial Board")

    def on_next(_):
        with output:
            try:
                item = next(state['iterator'])
            except StopIteration:
                print("Generator exhausted.")
                next_btn.layout.display = 'none'
                return

            board, stats = item
            clear_output(wait=True)
            if board is None:
                print("Search finished without solution.")
                print(stats)
                next_btn.layout.display = 'none'
                return

            if stats.get('success'):
                print(f"✅ Solution found. Steps: {stats.get('steps', '?')}, time: {stats.get('runtime', 0):.6f}s")
                state['board_obj'].display_board(board, "Final Solution")
                next_btn.layout.display = 'none'
                return

            if state['mode'] == 'csp':
                print(f"Assigned: {stats.get('assigned', 0)}, Steps: {stats['steps']}, Time: {stats['runtime']:.6f}s")
                state['board_obj'].display_board(board, "CSP Step (Partial Assignment)")
                return

            if state['mode'] == 'ls':
                print(f"Step: {stats['steps']}, Conflicts: {stats['conflicts']}, Temp: {stats['temperature']:.12f}, Restarts: {stats['restarts']}")
                state['board_obj'].display_board(board, "Local Search Progress")

    def on_reset(_):
        next_btn.layout.display = 'none'
        with output:
            show_initial(N_slider.value, seed_box.value)

    # Button bindings
    auto_ls_btn.on_click(on_auto_ls)
    step_ls_btn.on_click(on_step_ls)
    auto_csp_btn.on_click(on_auto_csp)
    step_csp_btn.on_click(on_step_csp)
    next_btn.on_click(on_next)
    reset_btn.on_click(on_reset)

    controls = widgets.VBox([
        widgets.HBox([N_slider, seed_box]),
        widgets.HBox([auto_ls_btn, step_ls_btn, auto_csp_btn, step_csp_btn, next_btn, reset_btn])
    ])
    ui = widgets.VBox([controls, widgets.HTML('<hr/>'), output])
    display(ui)



run_interface()
