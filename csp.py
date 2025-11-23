class CSP:
    def __init__(self, board):
        self.board = board

    @staticmethod
    def is_consistent(col, row, assignment_local):
        #This checks if placing a queen in column 'col' at row 'row' is valid, given the queens already placed in assignment_local
        for c, r in assignment_local.items():
            #row or diagonal conflict
            if r == row or abs(c - col) == abs(r - row):
                return False
        return True

    #Variable Selection (MRV heuristic)
    #Selects which variable (column) to assign next.
    @staticmethod
    def select_unassigned(domains_local, assignment_local):
        candidates = []
        for c in domains_local:
            if c not in assignment_local:
                candidates.append((len(domains_local[c]), c))
        #Sorts by domain size — columns with fewer possible rows come first
        candidates.sort()
        #Picks the column with smallest domain (most constrained variable).
        #Instead of degree heuristic it picks the first after sorting  ---> it makes no special difference for values of N from N=4 to N=64
        return candidates[0][1]

    #Value Ordering (LCV heuristic)
    @staticmethod
    def order_values(col, domains_local, assignment_local):
        def impact(row_val):
            removed = 0
            for c in domains_local:
                #continue if already assigned
                if c in assignment_local or c == col:
                    continue
                for other_row_val in list(domains_local[c]):
                    #Count how many would be eliminated to measure impact (same row or diagonal conflict).
                    if other_row_val == row_val or abs(c - col) == abs(other_row_val - row_val):
                        removed += 1
            return removed

        vals = list(domains_local[col])
        #Sort possible row values so the least restrictive (smallest impact) comes first.
        vals.sort(key=lambda x: impact(x))
        return vals

    #constraint propagation
    @staticmethod
    def forward_check(col, row, domains_local, N, assignment_local):
        #make a copy
        new_domains = {c: set(domains_local[c]) for c in domains_local}
        for c in new_domains:
            #For the current variable (col), fix its domain to {row}
            if c == col:
                new_domains[c] = {row}
                continue
            #prune the domain of other cols ---> propagate the constraint
            #row-constraint
            if row in new_domains[c]:
                new_domains[c].remove(row)

            #diagonal-constraint
            #for the current placed queen (col, row):
            #/ diagonal: all positions where r + c == row + col
            #\ diagonal: all positions where r - c == row - col
            #So the two possible diagonally attacked rows in column col are
            diag1 = row + (c - col)
            diag2 = row - (c - col)
            for dc in (diag1, diag2):
                #if in bounds and not already pruned
                if 0 <= dc < N and dc in new_domains[c]:
                    new_domains[c].remove(dc)
            #If any unassigned column loses all possible rows → contradiction.
            #Return None → signal backtrack needed.
            if len(new_domains[c]) == 0 and c not in assignment_local:
                return None
        return new_domains


    # --- Auto Solver ---
    def csp_auto(self, time_limit: Optional[float] = 10.0) -> Tuple[Optional[List[int]], dict]:
        N = self.board.N
        start_time = time.time()
        #Represents the possible positions of the queen in each column before pruning.
        domains = {c: set(range(N)) for c in range(N)}
        #Tracks current partial solution.
        assignment = {}
        steps = 0

        def backtrack(domains_local, assignment_local):
            #nonlocal allows modifying the steps variable defined outside in the parent function.
            nonlocal steps
            steps += 1
            if time_limit and (time.time() - start_time) > time_limit:
                raise TimeoutError('CSP time limit exceeded')
            #If all columns assigned, we found a valid complete solution
            if len(assignment_local) == N:
                return assignment_local

            col = self.select_unassigned(domains_local, assignment_local)
            for row_val in self.order_values(col, domains_local, assignment_local):
                if self.is_consistent(col, row_val, assignment_local):
                    new_domains = self.forward_check(col, row_val, domains_local, N, assignment_local)
                    if new_domains is not None:
                        assignment_local[col] = row_val
                        result = backtrack(new_domains, assignment_local)
                        if result is not None:
                            return result
                        #backtrack: try some other row_val
                        del assignment_local[col]
            #backrack: try some other variable
            return None

        try:
            sol = backtrack(domains, assignment)
        except TimeoutError:
            return None, {
                'success': False,
                'steps': steps,
                'runtime': time.time() - start_time,
                'timeout': True
            }

        runtime = time.time() - start_time
        if sol is None:
            return None, {'success': False, 'steps': steps, 'runtime': runtime}

        #converting to a simple list that represent the board
        state = [sol[c] for c in range(N)]
        return state, {'success': True, 'steps': steps, 'runtime': runtime}

    # --- Step Solver (Generator) ---
    def csp_step(self, time_limit: Optional[float] = float('inf')) -> Generator[Tuple[Optional[List[int]], dict], None, None]:
        N = self.board.N
        start_time = time.time()
        domains = {c: set(range(N)) for c in range(N)}
        assignment: Dict[int, int] = {}
        steps = 0

        def backtrack_gen(domains_local, assignment_local):
            nonlocal steps
            steps += 1
            if time_limit and (time.time() - start_time) > time_limit:
                raise TimeoutError('CSP time limit exceeded')

            if len(assignment_local) == N:
                state_full = [assignment_local[r] for r in range(N)]
                yield (state_full, {
                    'success': True,
                    'steps': steps,
                    'runtime': time.time() - start_time
                })
                return True

            col = self.select_unassigned(domains_local, assignment_local)
            for row_val in self.order_values(col, domains_local, assignment_local):
                if self.is_consistent(col, row_val, assignment_local):
                    new_domains = self.forward_check(col, row_val, domains_local, N, assignment_local)
                    if new_domains is not None:
                        assignment_local[col] = row_val
                        partial = [
                            assignment_local[c] if c in assignment_local else -1
                            for c in range(N)
                        ]
                        yield (partial, {
                            'success': False,
                            'steps': steps,
                            'runtime': time.time() - start_time,
                            'assigned': len(assignment_local)
                        })

                        done = False
                        try:
                            for res in backtrack_gen(new_domains, assignment_local):
                                yield res
                                if res[1].get('success'):
                                    done = True
                                    break
                        except TimeoutError:
                            raise

                        if done:
                            return True

                        del assignment_local[col]
                        partial_back = [
                            assignment_local[c] if c in assignment_local else -1
                            for c in range(N)
                        ]
                        yield (partial_back, {
                            'success': False,
                            'steps': steps,
                            'runtime': time.time() - start_time,
                            'backtracked': True,
                            'assigned': len(assignment_local)
                        })
            return False

        try:
            gen = backtrack_gen(domains, assignment)
            if gen is None:
                yield (None, {'success': False, 'steps': steps, 'runtime': time.time() - start_time})
                return
            for it in gen:
                yield it
            yield (None, {'success': False, 'steps': steps, 'runtime': time.time() - start_time})
        except TimeoutError:
            yield (None, {
                'success': False,
                'steps': steps,
                'runtime': time.time() - start_time,
                'timeout': True
            })
