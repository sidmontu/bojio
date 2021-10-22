/***********************************************************************************
 * MIT License
 *
 * Copyright (c) [2021] [Siddhartha (sidmontu@gmail.com)]
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
************************************************************************************/


#include "include/utils.h"

void _place_piece(bitboard_t bitboard, std::string name, std::string board[64]) {
    if (bitboard && _is_power_of_two(bitboard)) {
        unsigned idx = _lod(bitboard, 64);
        if (board[idx] != " ") {
            printf("Error: invalid board configuration, two pieces on same square.\n");
            printf("\tExisting piece = %s, new piece = %s, bitboard = ",
                    board[idx].c_str(), name.c_str());
            printf("0x%" PRIx64 "\n", bitboard);
            exit(EXIT_FAILURE);
        }
        board[idx] = name;
    } else {
        printf("Error: Invalid %s configuration, bitboard = ", name.c_str());
        printf("0x%" PRIx64 "\n", bitboard);
        exit(EXIT_FAILURE);
    }
}

/**
 * Prints chess board's state to stdout.
 *
 * @param board_state Pointer to board state of type BoardState.
 * @return void.
 */
void print_board_state(BoardState* board_state) {
    std::string board[64];

    // init the board
    for (int i = 0; i < 64; ++i) board[i] = ' ';

    // evaluate black king
    _place_piece(board_state->black.king, "B-K", board);

    // evaluate white king
    _place_piece(board_state->white.king, "W-K", board);

    // evaluate black queens
    for (bitboard_t queen : board_state->black.queens) {
        _place_piece(queen, "B-Q", board);
    }

    // evaluate white queens
    for (bitboard_t queen : board_state->white.queens) {
        _place_piece(queen, "W-Q", board);
    }

    // evaluate black pawns
    for (bitboard_t pawn : board_state->black.pawns) {
        _place_piece(pawn, "B-P", board);
    }

    // evaluate white pawns
    for (bitboard_t pawn : board_state->white.pawns) {
        _place_piece(pawn, "W-P", board);
    }

    // evaluate black rooks
    for (bitboard_t rook : board_state->black.rooks) {
        _place_piece(rook, "B-R", board);
    }

    // evaluate white rooks
    for (bitboard_t rook : board_state->white.rooks) {
        _place_piece(rook, "W-R", board);
    }

    // evaluate black knights
    for (bitboard_t knight : board_state->black.knights) {
        _place_piece(knight, "B-N", board);
    }

    // evaluate black knights
    for (bitboard_t knight : board_state->white.knights) {
        _place_piece(knight, "W-N", board);
    }

    // evaluate black bishops
    for (bitboard_t bishop : board_state->black.bishops) {
        _place_piece(bishop, "B-B", board);
    }

    // evaluate white bishops
    for (bitboard_t bishop : board_state->white.bishops) {
        _place_piece(bishop, "W-B", board);
    }

    // print the board to stdout
    _print_board_state_from_string_arr(board);
}

void _print_board_state_from_string_arr(std::string board[64]) {
    char cols[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'};

    printf("%-3c", ' ');
    for (int i = 0; i < 8; ++i) {
        printf("%-6s", "______");
    }
    printf("\n");
    for (int row = 7; row >= 0; --row) {
        // top empty row
        printf("  |");
        for (int col = 0; col < 8; ++col) {
            printf("%-5s|", " ");
        }
        printf("\n");

        printf("%-2s|", std::to_string(row+1).c_str());
        for (int col = 0; col < 8; ++col) {
            printf(" %-4s|", board[row*8+col].c_str());
        }
        printf("\n  |");
        for (int col = 0; col < 8; ++col) {
            printf("%-5s|", "_____");
        }
        printf("\n");
    }
    printf("%-5c", ' ');
    for (int i = 0; i < 8; ++i) {
        printf("%c     ", cols[i]);
    }
    printf("\n");
}

bool _is_power_of_two(bitboard_t x) {
    return (x != 0) && ((x & (x - 1)) == 0);
}

unsigned _lod(bitboard_t value, unsigned total_bits) {
    return (total_bits-1) - (unsigned)__builtin_clzl(value);
}

void benchmark() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> distrib(0, 63);

    const int NUM_VALS = 10000;
    const int ITERS = 1000;

    // make large array of values to log2 on
    bitboard_t vals[NUM_VALS];
    for (int i = 0; i < NUM_VALS; ++i)
        vals[i] = 1 << distrib(gen);

    unsigned results_0[NUM_VALS];

    using std::chrono::high_resolution_clock;
    using std::chrono::duration;

    auto t1 = high_resolution_clock::now();
    for (int j = 0; j < ITERS; ++j)
        for (int i = 0; i < NUM_VALS; ++i)
            results_0[i] = _lod(vals[i], 64);
    auto t2 = high_resolution_clock::now();

    duration<double, std::milli> ms_double = t2 - t1;

    printf("[_lod] Runtime = %.8fms\n", ms_double.count());
}

BoardState init_standard_game() {
    BoardState bs;

    // init black pieces
    bitboard_t black_pieces = 0;
    for (unsigned i = 63; i >= 48; --i) black_pieces += ((bitboard_t)1 << i);
    bs.black.pieces = black_pieces;
    bs.black.rooks.push_back((bitboard_t)1 << 63);
    bs.black.knights.push_back((bitboard_t)1 << 62);
    bs.black.bishops.push_back((bitboard_t)1 << 61);
    bs.black.king = (bitboard_t)1 << 60;
    bs.black.queens.push_back((bitboard_t)1 << 59);
    bs.black.bishops.push_back((bitboard_t)1 << 58);
    bs.black.knights.push_back((bitboard_t)1 << 57);
    bs.black.rooks.push_back((bitboard_t)1 << 56);
    for (int i = 55; i >= 48; --i) bs.black.pawns.push_back((bitboard_t)1 << i);

    // init white pieces
    bitboard_t white_pieces = 0;
    for (unsigned i = 0; i < 16; ++i) white_pieces += ((bitboard_t)1 << i);
    bs.white.pieces = white_pieces;
    bs.white.rooks.push_back((bitboard_t)1 << 0);
    bs.white.knights.push_back((bitboard_t)1 << 1);
    bs.white.bishops.push_back((bitboard_t)1 << 2);
    bs.white.queens.push_back((bitboard_t)1 << 3);
    bs.white.king = (bitboard_t)1 << 4;
    bs.white.bishops.push_back((bitboard_t)1 << 5);
    bs.white.knights.push_back((bitboard_t)1 << 6);
    bs.white.rooks.push_back((bitboard_t)1 << 7);
    for (int i = 8; i < 16; ++i) bs.white.pawns.push_back((bitboard_t)1 << i);

    return bs;
}
