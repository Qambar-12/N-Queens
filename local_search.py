class LocalSearch:
    def __init__(self, board: Board):
        self.board = board

    def _local_search_core(
        self,
        max_steps:int=100000,
        restart_limit:int=25,
        initial_temp:float=1000.0,
        stagnation_limit:int=1000,
        seed:Optional[int]=None
    ) -> Generator[Tuple[Optional[List[int]], dict], None, None]:

        if seed is not None:
            random.seed(seed)
        N = self.board.N
        restarts = 0
        cooling_rate = 1 - 1 / max(1, N)
        start_time = time.time()

        if 4 <= N < 8:
            stagnation_limit = 500
        elif 8 <= N < 16:
            stagnation_limit = 1000
        elif 16 <= N < 32:
            stagnation_limit = 2250
        else:
            stagnation_limit = 5000

        while restarts <= restart_limit:
            steps = 0
            temperature = initial_temp
            current_board = self.board.random_board()
            current_conflicts = Board.count_conflicts(current_board)
            best_conflicts = current_conflicts
            no_improve = 0

            while steps < max_steps:
                # yield current state
                yield current_board, {
                    'success': current_conflicts == 0,
                    'conflicts': current_conflicts,
                    'steps': steps,
                    'restarts': restarts,
                    'temperature': temperature,
                    'runtime': time.time() - start_time
                }

                if current_conflicts == 0:
                    return  # stop generator if solution found

                # pick a random column and row
                col = random.randint(0, N-1)
                new_row = random.randint(0, N-1)
                while new_row == current_board[col]:
                    new_row = random.randint(0, N-1)
                new_board = list(current_board)
                new_board[col] = new_row
                new_conflicts = Board.count_conflicts(new_board)

                delta_e = current_conflicts - new_conflicts
                if delta_e > 0 or math.exp(delta_e / max(1e-12, temperature)) > random.random():
                    current_board = new_board
                    current_conflicts = new_conflicts

                if current_conflicts >= best_conflicts:
                    if temperature < 1e-6:
                        no_improve += 1
                        if no_improve >= stagnation_limit:
                            break
                else:
                    best_conflicts = current_conflicts
                    no_improve = 0

                temperature *= cooling_rate
                steps += 1

            restarts += 1
            yield current_board, {'success': False, 'conflicts': current_conflicts, 'steps': steps, 'restarts': restarts, 'restarted': True}


        yield None, {
            'success': False,
            'conflicts': current_conflicts,
            'steps': steps,
            'restarts': restarts,
            'runtime': time.time() - start_time
        }

    def local_search_auto(self, **kwargs) -> Tuple[Optional[List[int]], dict]:
        result = None
        for board_state, info in self._local_search_core(**kwargs):
            result = (board_state, info)
            if info.get('success'):
                return result
        return result

    def local_search_step(self, **kwargs) -> Generator[Tuple[Optional[List[int]], dict], None, None]:
        return self._local_search_core(**kwargs)

