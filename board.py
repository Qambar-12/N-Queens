class Board:
    def __init__(self, N:int = 8, seed:Optional[int]=None):
        self.N = N
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.board = self.random_board()

    def random_board(self) -> List[int]:
        return [random.randint(0, self.N - 1) for _ in range(self.N)]

    #O(N)
    @staticmethod
    def count_conflicts(board: List[int]) -> int:
        N = len(board)
        col_counts = [0] * N
        #main diagonal ; no. of unique main diagonal lines = 2N-1
        main_diag_counts = [0] * (2 * N)
        #anti-diagonal ;  no. of unique anti diagonal lines = 2N-1
        anti_diag_counts = [0] * (2 * N)

        for c, r in enumerate(board):
            col_counts[r] += 1
            #shifted by +N to avoid negative indices
            main_diag_counts[r - c + N] += 1
            anti_diag_counts[r + c] += 1

        conflicts = 0
        for counts in (col_counts, main_diag_counts, anti_diag_counts):
            for cnt in counts:
                if cnt > 1:
                     # combinations of attacking queens = nC2
                    conflicts += cnt * (cnt - 1) // 2
        return conflicts

    def display_board(self, board: Optional[List[int]] = None, title: str = ""):
        if board is None:
            board = self.board
        N = self.N
        conflicts = self.count_conflicts(board)

        if 4 <= N < 8:
            size = 5
        elif 8 <= N < 16:
            size = 8
        elif 16 <= N < 32:
            size = 12
        else:
            size = 14

        plt.figure(figsize=(size, size))
        plt.imshow([[((r + c) % 2) for c in range(N)] for r in range(N)], cmap='gray')
        for c, r in enumerate(board):
            if 0 <= r < N:
                plt.text(c, r, "♛", ha='center', va='center', fontsize=24 if N <= 10 else 14, color='red')
        if str == "Local Search Progress":
          plt.title(f"{title}\nConflicts: {conflicts}")
        plt.axis('off')
        plt.show()

